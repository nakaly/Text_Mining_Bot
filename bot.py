import os
import time

import sys
from sys import argv

import bottle
from bottle import default_app, request, route, response, get


import tweepy

class TwitterAPI:
    """
    Class for accessing the Twitter API.

    Requires API credentials to be available in environment
    variables. These will be set appropriately if the bot was created
    with init.sh included with the heroku-twitterbot-starter
    """
    def __init__(self):
        consumer_key = ""
        consumer_secret = ""
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = ""
        access_token_secret = ""
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        """Send a tweet"""
        self.api.update_status(message)

#if __name__ == "__main__":

@route('/')
def index():
    twitter = TwitterAPI().api
    #twitter.tweet("Hello world!") #You probably want to remove this line
    public_tweets = twitter.home_timeline()
    for tweet in public_tweets:
        ret += str(tweet)
    return ret
#     return "test"

bottle.run(host='0.0.0.0', port=argv[1])
