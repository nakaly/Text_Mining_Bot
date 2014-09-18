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

#if __name__ == "__main__":

@route('/')
def index():
    twitter = TwitterAPI().api
    #twitter.tweet("Hello world!") #You probably want to remove this line
    public_tweets = twitter.home_timeline(count=200, page=1)
    wordcount = {}
    words = []
    for tweet in public_tweets:
        ret = str(tweet.text.encode('ascii', 'ignore'))
	words.extend(ret.lower().split())

    for word in words:
        if word in wordcount:
            wordcount[word] += 1
        else:
            wordcount[word] = 1

    public_tweets_old = twitter.home_timeline(count=200, page=2)
    wordcount_old = {}
    words_old = []
    for tweet in public_tweets_old:
        ret = str(tweet.text.encode('ascii', 'ignore'))
        words_old.extend(ret.lower().split())

    for word in words_old:
        if word in wordcount_old:
            wordcount_old[word] += 1
        else:
            wordcount_old[word] = 1

    return wordcount_old

bottle.run(host='0.0.0.0', port=argv[1])
