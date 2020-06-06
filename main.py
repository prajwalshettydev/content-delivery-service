from twitterservice import tweet
from googleservice import gsheet
import urllib.request
import config
import os


def tick():
    next_scheduled_tweet_time = config.last_tweet_time + config.time_between_tweets
    if(next_scheduled_tweet_time < config.datetime.now()):
        print("We are due to tweet by:" +
              str(config.datetime.now() - next_scheduled_tweet_time))
        do_next_scheduled_tweet()
    else:
        print("Next tweet will trigger after: " +
              str(next_scheduled_tweet_time - config.datetime.now()))


    config.sync()


def do_next_scheduled_tweet():
    # -1 and +1 are representation purposes only
    # -1 to fix the start index, 0 in our python list vs 1 in the google sheet
    # +1 to increment to the next row
    current_row = initial_row = (config.last_tweet_row_index) + 1

    main_tweet_data = gsheet.get_particular_row_from_sheet(config.content_sheet_id,current_row)

    if not main_tweet_data[0]:
        print("Starving of content, nothing to tweet for now. please add something at row: "+str(current_row))
        return

    last_tweet_id = tweet_tweet(main_tweet_data)
    print("Tweeted from row: " + str(current_row))

    if main_tweet_data[1] and int(main_tweet_data[1].get('numberValue')) > 0:
        while current_row < initial_row + int(main_tweet_data[1].get('numberValue')):
            current_row += 1
            subtweet_data = gsheet.get_particular_row_from_sheet(current_row)
            last_tweet_id = tweet_tweet(
                subtweet_data, parent_tweet_id=last_tweet_id)
            print("Sub-Tweeted from row: " + str(current_row))

    config.last_tweet_time = config.datetime.now()
    config.last_tweet_row_index = current_row


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