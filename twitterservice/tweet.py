import tweepy

api = None


def init(twitter_auth_data):
    global api
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(twitter_auth_data["consumerAPIkey"],
                               twitter_auth_data["consumerAPIsecretKey"])
    auth.set_access_token(twitter_auth_data["accessToken"],
                          twitter_auth_data["accessTokenSecret"])

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)


def check_twitter_auth():
    print("Authenticating to twitter")
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")


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
