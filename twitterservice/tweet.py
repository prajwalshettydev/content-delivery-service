import tweepy
import config

def init():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config.ConsumerAPIkey,
                            config.ConsumerAPIsecretKey)
    auth.set_access_token(config.AccessToken,
                        config.AccessTokenSecret)

    # Create API object
    return tweepy.API(auth, wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True)

api = init()

# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")


def post_simple_tweet(tweet: str):
    # Create a tweet
    resp = api.update_status(tweet)

    return resp.id_str


def tweet_to_twitter(tweet: str, media_ids: [], annotation: str, parent_id=str,):

    if annotation:
        resp = api.update_status(tweet, in_reply_to_status_id=parent_id,
                                 auto_populate_reply_metadata=True, attachment_url=annotation, media_ids=media_ids)
        return resp.id_str
    else:
        resp = api.update_status(tweet, in_reply_to_status_id=parent_id,
                                 auto_populate_reply_metadata=True, media_ids=media_ids)
        return resp.id_str

    # if parent_id:
    #     resp = api.update_status(tweet, in_reply_to_status_id=parent_id,
    #                              auto_populate_reply_metadata=True, attachment_url=annotation, media_ids=media_ids)
    #     return resp.id_str
    # else:
    #     resp = api.update_status(tweet, attachment_url=annotation, media_ids=media_ids)
    #     return resp.id_str


def upload_media(file_path):
    media_upload_resp = api.media_upload(file_path)
    return media_upload_resp.media_id_string


# Delete Tweet
# api.destroy_status()

