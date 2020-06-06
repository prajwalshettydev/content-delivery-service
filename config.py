import os
import sys
import json
import typing
from datetime import timedelta, datetime
from googleservice import gsheet
from twitterservice import tweet
from utils import sync_ops

# file
img_download_loc = 'ops/media'
config_file_loc = 'creds/config.json'
analytics_file_loc = 'creds/analytics.json'
twitter_cred_loc = 'creds/twitterCred.json'
token_pickle = "creds/token.pickle"
sheet_credentials = "creds/credentials.json"
log_loc = 'ops'

# GSheet
content_sheet_id: str = '' 
settings_sheet_id: str = ''
settings_range: str = ''
analytics_range: str = ''
sheet_auth_scope: str = ''

# Core
core_service_name: str = ''
version = (0, 1, 1)
last_tweet_row_index: int = -1
debug_mode = False
str_datetime_format = r'%Y-%m-%dT%H:%M:%S.%fZ'

# Time
last_tweet_time: datetime = datetime.max
last_active_time: datetime = datetime.now()
tick_frequency: timedelta = timedelta(seconds=10, minutes=0, hours=0)
time_between_tweets: timedelta = timedelta(days=0, hours=12)

if not debug_mode:
    sys.stderr = open(os.path.join(log_loc, 'log_err.txt'), 'w', 1)
    sys.stdout = open(os.path.join(log_loc, 'log_out.txt'), 'w', 1)


def datetime_str(date_time: datetime):
    return date_time.strftime(str_datetime_format)


def load_json_from_file(filepath: str):
    """Loads json data from the file, Note: file should be a valid .json file

    Arguments:
        filepath {str} -- A valid json file

    Returns:
        Dict -- Returns a Dict serialized from a json file
    """
    if not os.path.isfile(filepath):
        print("File doesn't exist " + filepath)
        return '{}'

    with open(filepath, encoding='utf-8') as f:
        return json.load(f)


def save_json(json_data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.truncate(0)  # need '0' when using r+
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def load_data_from_json(json_file_loc):
    config = load_json_from_file(json_file_loc)
    for k in config.keys():
        if k in globals():
            if type(globals()[k]) is datetime:
                globals()[k] = datetime.strptime(config[k], str_datetime_format)
            elif type(globals()[k]) is timedelta:
                t = datetime.strptime(config[k], "%H:%M:%S")
                globals()[k] = timedelta(hours=t.hour,
                                         minutes=t.minute, seconds=t.second)
            else:
                globals()[k] = config[k]
        # else:
        #     print("Skipping: "+ k)


def init():
    load_data_from_json(config_file_loc)
    load_data_from_json(analytics_file_loc)

    # setup
    gsheet.init(token_pickle, sheet_credentials, sheet_auth_scope)
    twitter_auth_data = load_json_from_file(twitter_cred_loc)
    tweet.init(twitter_auth_data)


def sync():
    print("\nSyncing Service Config with cloud..")
    global last_active_time
    last_active_time = datetime.now()
    sync_analytics()
    sync_settings()


def sync_settings():
    # get settings
    resp: [[]] = gsheet.get_range_from_sheet(settings_sheet_id, settings_range)

    value_dict = {x[0]: x[1] for x in resp}
    save_json(value_dict, config_file_loc)
    load_data_from_json(config_file_loc)


def sync_analytics():
    values: [[]] = [
        ['version', str(version)],
        ['last_active_time', datetime_str(last_active_time)],
        ['total_hours_online', "NA"],
        ['total_tweets_sent', "NA"],
        ['operation_timezone', "IST"],
        ['last_tweet_row_index', last_tweet_row_index],
        ['last_tweet_time', datetime_str(last_tweet_time)],
    ]

    value_dict = {x[0]: x[1] for x in values}
    save_json(value_dict, analytics_file_loc)

    body = {'values': values}
    resp = gsheet.set_range_of_sheet(settings_sheet_id, analytics_range, body)
    return resp
