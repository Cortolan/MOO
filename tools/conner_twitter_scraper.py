# conner_twitter_scraper.py

import pandas as pd 
import requests 
import re 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import json
import tweepy

from getpass import getpass
from pathlib import Path
import pickle
import itertools
import collections

import nltk
import pprint

with open("keys.json") as f:
    keys = json.load(f)

#########################################################################################################
# Getting some example tweets
twitter_username = "elonmusk"

ds_tweets_save_path = "{}_recent_tweets.pkl".format(twitter_username)

if not Path(ds_tweets_save_path).is_file():
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    api = tweepy.API(auth)
    example_tweets = list(tweepy.Cursor(api.user_timeline, id=twitter_username).items())
    with open(ds_tweets_save_path, "wb") as f:
        import pickle 
        pickle.dump(example_tweets, f)

with open(ds_tweets_save_path, "rb") as f:
    import pickle 
    example_tweets = pickle.load(f)

#print(example_tweets[0].text)

#########################################################################################################
def download_recent_tweets_by_user(user_account_name, keys): 
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    api = tweepy.API(auth)
    example_tweets = list(tweepy.Cursor(api.user_timeline, id=user_account_name).items())
    return example_tweets

def save_tweets(tweets, path):
    with open(path, "wb") as f:
      import pickle 
      pickle.dump(tweets, f)

def load_tweets(path): 
    with open(path, 'rb') as f:
      import pickle
      tweets = pickle.load(f)
    return tweets

def get_tweets_with_cache(user_account_name, keys): 
    save_path = "{}_recent_tweets.pkl".format(user_account_name)
    from pathlib import Path 
    if not Path(save_path).is_file():
        tweets = download_recent_tweets_by_user(user_account_name, keys)
        save_tweets(tweets, save_path)
    return load_tweets(save_path)

cr_tweets = get_tweets_with_cache('CriticalRole', keys)
#print(cr_tweets[0].text)

#########################################################################################################

def make_dataframe(tweets): 
    text = []
    
    for tweet in tweets:
      text += [tweet.text]
    
    df = pd.DataFrame({'text':text})
    return df 

cr_df = make_dataframe(cr_tweets)
#print(cr_df.head())

#########################################################################################################

def remove_url(txt): 
    txt2 = re.sub('http[s]?://\S+', '', txt)
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    txt2 = re.sub(emoji_pattern, '', txt2)
    return txt2

cr_tweets_text = [tweet.text for tweet in cr_tweets]
cr_tweets_no_urls = [remove_url(tweet) for tweet in cr_tweets_text]
#print(cr_tweets_no_urls[:4])

#########################################################################################################

words_in_tweets = []
for tweet in cr_tweets_no_urls:
  words = tweet.lower().split()
  words_in_tweets += words
#print(words_in_tweets[:20])

