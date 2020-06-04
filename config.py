import os
import sys
import json
from datetime import timedelta, datetime

img_download_loc = 'ops/media'
config_file_loc = 'creds/config.json'
twitter_cred_loc = 'creds/twitterCred.json'
log_loc = 'ops'
str_datetime_format = r'%Y-%m-%dT%H:%M:%S.%fZ'

# Twitter_Auth
ConsumerAPIkey: str
ConsumerAPIsecretKey: str
AccessToken: str
AccessTokenSecret: str

# GSheet_Auth
token_pickle = "creds/token.pickle"
sheet_credentials = "creds/credentials.json"

# Core
CoreServiceName: str
Version = (0, 0, 2)
Refresh_time = 10  # seconds
ContentSheet: str
CurrentTweet: int

last_tweet_time: datetime = datetime.max
refresh_time: timedelta = timedelta(
    days=0, seconds=10, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
timedelta_between_tweets: timedelta = timedelta(
    days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=12, weeks=0)


sys.stderr = open(os.path.join(log_loc, 'log_err.txt'), 'w', 1)
sys.stdout = open(os.path.join(log_loc, 'log_out.txt'), 'w', 1)

def LoadJsonFromFile(filepath: str):
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


def init():
    global CurrentTweet, last_tweet_time, CoreServiceName, ContentSheet

    inputData = LoadJsonFromFile(config_file_loc)

    CurrentTweet = inputData["currentTweet"]
    last_tweet_time = datetime.strptime(
        inputData["lastTweetTime"], str_datetime_format)
    CoreServiceName = inputData["coreSerivceName"]
    ContentSheet = inputData["contentSheet"]

    setup_twitter()


def setup_twitter():
    global ConsumerAPIkey, ConsumerAPIsecretKey, AccessToken, AccessTokenSecret
    
    inputData = LoadJsonFromFile(twitter_cred_loc)

    ConsumerAPIkey = inputData["consumerAPIkey"]
    ConsumerAPIsecretKey = inputData["consumerAPIsecretKey"]
    AccessToken = inputData["accessToken"]
    AccessTokenSecret = inputData["accessTokenSecret"]


init()