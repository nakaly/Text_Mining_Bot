import os
import time

import tweepy

class TwitterAPI:
    """
    Class for accessing the Twitter API.

    Requires API credentials to be available in environment
    variables. These will be set appropriately if the bot was created
    with init.sh included with the heroku-twitterbot-starter
    """
    def __init__(self):
        consumer_key = "zrkudNdWxMBZUWSlLeTn9uwoZ"
        consumer_secret = "kMMSckasyrKmtV55uhNziLXHzMVcfblNGA2PbcRla30uW4C1GF"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = "2814523249-fqhwgB3fhfagLgYHqEM8WkvJ2ol9bSoYDUPlV4j"
        access_token_secret = "AwbHGdztNDm5nsX3kepQXSIJb96EpMZYcB5waBO7EbVCi"
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        """Send a tweet"""
        self.api.update_status(message)

if __name__ == "__main__":
    twitter = TwitterAPI()
    #twitter.tweet("Hello world!") #You probably want to remove this line
    #public_tweets = twitter.home_timeline()
    while True:
    	twitter.tweet("Hello world!")
	sleep(60)
    

        time.sleep(60)
