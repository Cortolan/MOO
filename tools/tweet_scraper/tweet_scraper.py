# tweet_scraper.py

import json
import tweepy
from pathlib import Path
import os
from datetime import datetime
import pickle

print('dmyHMS = ',datetime.now().strftime('%d-%m-%y_%H-%M-%S'))

with open("keys.json") as f:
    keys = json.load(f)

def get_hashtags():
    hashtag_txt = open('hashtags.txt', 'r')
    hashtag_list = hashtag_txt.readlines()
    for entry, tag in enumerate(hashtag_list):
        hashtag_list[entry] = tag[:-1].lower()
    return hashtag_list
        
def write_tweets(NUM_TWEETS):
    current_time = datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    for hashtag in get_hashtags():
        tweets_save_path = 'tweets/{}_recent_tweets/{}_{}.pkl'.format(hashtag[1:], hashtag[1:],  current_time)
        
        os.makedirs(os.path.dirname(tweets_save_path), exist_ok=True)
        auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
        auth.set_access_token(keys['access_token'], keys['access_token_secret'])
        api = tweepy.API(auth)
        tweets = list(tweepy.Cursor(api.search, q=hashtag, rpp=100, tweet_mode='extended').items(NUM_TWEETS))
        print('API accessed successfully')

        with open(tweets_save_path, 'wb') as f:
            pickle.dump(tweets, f)
            print('Tweets serialized successfully')

def read_tweets():
    for root, dir, file, in os.walk('tweets'):
        for filename in file:
            tweets_save_path = os.path.join(root, filename)
            with open(tweets_save_path, 'rb') as f:
                tweets = pickle.load(f)
        
                for i,tweet in enumerate(tweets):
                    print(i,'#'*40)
                    print(tweet.full_text)

#write_tweets(100)
#read_tweets()
