import os
import time

import operator
from operator import itemgetter

import sys
from sys import argv

import bottle
from bottle import default_app, request, route, response, get, static_file, redirect

import redis

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


@get('/info/prep')
def preparation_freq_words():
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

    public_tweets_old = twitter.home_timeline(count=200, page=12)
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

    wordcount_diff = {}
    for k, v in wordcount.iteritems():
        print k, v
        found = False
        for k_old, v_old in wordcount_old.iteritems():
            if k == k_old:
                diff = abs(v - v_old)
                wordcount_diff[k] = diff
                found = True
        if not found:
            wordcount_diff[k] = v

    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    redis_db = redis.from_url(redis_url)

    for k, v in wordcount_diff.iteritems():
    	redis_db.zadd("freq_word", k, int(v))
#    ret_str = ""
#    for k, v in sorted(wordcount_diff.iteritems(), key=itemgetter(1), reverse=True):
#        temp = k + ":" + str(v) + "###"
#        ret_str += temp

@get('/info/freq_words')
def freq_words():
	response.content_type = 'application/json'
	dict_freq_words = {}
	wordID = int(request.query.id)
	wordCount = int(request.query.count)
	redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
	redis_db = redis.from_url(redis_url)
	freq_words = redis_db.zrange("freq_word", 0, -1, withscores=True)
	dict_freq_words = dict(freq_words[wordID:wordID + wordCount])
	return dict_freq_words

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/') 

@route('/')
def index():
    preparation_freq_words()
    redirect("/static/index.html")

bottle.run(host='0.0.0.0', port=argv[1])
