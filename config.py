import os
import json
from datetime import timedelta, datetime

img_download_loc = 'ops/media'
config_file_loc = 'creds/config.json'
log_loc = 'ops'

# Twitter_Auth
ConsumerAPIkey = ""
ConsumerAPIsecretKey = ""
AccessToken = ""
AccessTokenSecret = ""

# GSheet_Auth

# Core
CoreServiceName = ""
Version = (0, 0, 1)
Refresh_time = 10  # seconds
ContentSheet = ""
CurrentTweet = 7
LastTweetTime: datetime = datetime(1995, )

# Time:
# Timedelta:
# All arguments are optional and default to 0.
# Arguments may be integers or floats, and may be positive or negative.
refresh_time: timedelta = timedelta(
    days=0, seconds=10, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
timedelta_between_tweets: timedelta = timedelta(
    days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=12, weeks=0)


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

    inputData = LoadJsonFromFile(config_file_loc)
    
    # inputData = inputData["data"]

    # CurrentTweet = inputData["currentTweet"]
    # CurrentTweet = inputData["lastTweetTime"]
    # CurrentTweet = inputData["coreSerivceName"]
    # CurrentTweet = inputData["contentSheet"]
