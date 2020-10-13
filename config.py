import os
import logging
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logger = logging.getLogger()

def create_api():
    # init auth variables
    consumer_key = os.environ['TW_API_TOKEN']
    consumer_key_secret = os.environ['TW_API_TOKEN_SECRET']
    access_token = os.environ['TW_ACCESS_TOKEN']
    access_token_secret = os.environ['TW_ACCESS_TOKEN_SECRET']

    # init api
    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
    except:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
