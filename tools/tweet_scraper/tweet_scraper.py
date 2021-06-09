# tweet_scraper.py

import pandas as pd 
import json
import tweepy
from pathlib import Path
import pickle

with open("keys.json") as f:
    keys = json.load(f)

def get_hashtags():
    hashtag_txt = open('hashtags.txt', 'r')
    hashtag_list = hashtag_txt.readlines()
    for entry, tag in enumerate(hashtag_list):
        if tag[0] == '#':
            hashtag_list[entry] =  tag[:-1].lower()
        else:
            hashtag_list[entry] = '#' + tag[:-1].lower()
    return hashtag_list
        
def write_tweets(NUM_TWEETS):
    for hashtag in get_hashtags():
        tweets_save_path = 'tweets/{}_recent_tweets.pkl'.format(hashtag)
        if not Path(tweets_save_path).is_file():
            auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
            auth.set_access_token(keys['access_token'], keys['access_token_secret'])
            api = tweepy.API(auth)
            tweets = list(tweepy.Cursor(api.search, q=hashtag, rpp=100).items(NUM_TWEETS))

            with open(tweets_save_path, 'wb') as f:
                pickle.dump(tweets, f)

def read_tweets():
    for hashtag in get_hashtags():
        tweets_save_path = 'tweets/{}_recent_tweets.pkl'.format(hashtag)

        with open(tweets_save_path, 'rb') as f:
            tweets = pickle.load(f)
        
        for i,tweet in enumerate(tweets):
            print(i,'#'*40)
            print(tweet.text)

write_tweets(10)
read_tweets()
