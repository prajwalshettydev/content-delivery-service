from twitterservice import tweet
from googleservice import gsheet
import urllib.request
import config
import os

def tick():
    current_row = initial_row = 8 - 1

    main_tweet_data = gsheet.get_particular_row_from_sheet(current_row)
    tweet.check_twitter_auth()
    pass


def upload_media(cell_data):
    # clean url
    image_url = str(cell_data.get('formulaValue')).replace(
        '=IMAGE(\"', '').replace('\")', '')
    print("Fetching image: " + image_url)
    filename = image_url.split('/')[-1]
    filepath = os.path.join(config.img_download_loc, filename)
    urllib.request.urlretrieve(image_url, filename)

    # Upload Image
    print("Upload image to twitter: " + filename)
    return tweet.upload_media(filename)


def tweet_tweet(tweet_data, parent_tweet_id=''):
    media_ids = []

    if tweet_data[2] != None:
        media_id = upload_media(tweet_data[2])
        media_ids.append(media_id)
    if tweet_data[3] != None:
        media_id = upload_media(tweet_data[3])
        media_ids.append(media_id)
    if tweet_data[4] != None:
        media_id = upload_media(tweet_data[4])
        media_ids.append(media_id)
    if tweet_data[5] != None:
        media_id = upload_media(tweet_data[5])
        media_ids.append(media_id)

    print("Tweeting: " + str(tweet_data[0].get('stringValue')))
    tweet_id = tweet.tweet_to_twitter(str(tweet_data[0].get('stringValue')),
                                      media_ids,
                                      str(tweet_data[6].get(
                                          'stringValue') if tweet_data[6] else ''),
                                      parent_id=parent_tweet_id)
    return tweet_id

# current_row = initial_row = 8 - 1

# main_tweet_data = gsheet.get_particular_row_from_sheet(current_row)
# last_tweet_id = tweet_tweet(main_tweet_data)
# print(str(current_row) + "th tweet complete")

# if main_tweet_data[1] and int(main_tweet_data[1].get('numberValue')) > 0:
#     while current_row < initial_row + int(main_tweet_data[1].get('numberValue')):
#         current_row += 1
#         subtweet_data = gsheet.get_particular_row_from_sheet(current_row)
#         last_tweet_id = tweet_tweet(
#             subtweet_data, parent_tweet_id=last_tweet_id)
#         print(str(current_row) + "th tweet complete")
