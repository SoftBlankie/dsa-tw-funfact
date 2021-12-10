import tweepy
from config import create_api

tw = create_api()

post_text = open("./utility/post_text.txt", "r") 
post_tags = open("./utility/post_tags.txt", "r") 

if post_text and post_tags:
    text = post_text.read()
    tags = post_tags.read()
    # place status in tweet
    tweet = tw.update_status(text)

    # place tags in comment
    tweetId = tweet.id_str
    tw.update_status(status = tags, in_reply_to_status_id = tweetId, auto_populate_reply_metadata=True)
