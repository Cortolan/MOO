"""
conner_twitter_scraper.py
This was initially used to gain experience working with APIs.
"""

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
import nltk
import pprint

with open("keys.json") as f:
    keys = json.load(f)

"""## Example - Get some Tweets
These next few lines load some tweets by '@packers'. 
"""

ds_tweets_save_path = "Packers_recent_tweets.pkl"

# Guarding against attempts to download the data multiple times: 
if not Path(ds_tweets_save_path).is_file():
    # use keys loaded in above by Method 1 or 2 

    # Authenticating: 
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    api = tweepy.API(auth)

    # Getting as many recent tweets by @packers as Twitter will let us have 
    example_tweets = list(tweepy.Cursor(api.user_timeline, id="packers").items())

    # Saving the tweets to a file as "pickled" objects: 
    with open(ds_tweets_save_path, "wb") as f:
        import pickle 
        pickle.dump(example_tweets, f)

# Re-loading the results
with open(ds_tweets_save_path, "rb") as f:
    import pickle 
    example_tweets = pickle.load(f)

# Looking at one tweet object, which has type Status: 
print(example_tweets[0])

import pprint
pprint.pprint(vars(example_tweets[0]))

##########################################################
quit()
##########################################################

"""## Q2 - (15 pts)
This downloads all recent tweets by a Twitter account of your choosing.
"""

def download_recent_tweets_by_user(user_account_name, keys): 
    """
    Input Args: 
        user_account_name (str): The name of hte Twitter account whose tweets will be downloaded. 
        keys (dict): A Python dictionary with Twitter authentication keys. See keys_blank.json for the proper format.
        
    Returns: 
        list of Status objects, each representing one tweet.
    """
    ### BEGIN SOLUTION
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    api = tweepy.API(auth)

    # Getting as many recent tweets by @packers as Twitter will let us have 
    example_tweets = list(tweepy.Cursor(api.user_timeline, id=user_account_name).items())

    
    return example_tweets
    ### END SOLUTION

def save_tweets(tweets, path):
    """Saves a list of tweets to a file in the local filesystem. 

    This function makes no guarantee about the format of the saved
    tweets, **except** that calling load_tweets(path) after
    save_tweets(tweets, path) will produce the same list of tweets
    and that only the file at the given path is used to store the
    tweets.  (That means you can implement this function however
    you want, as long as saving and loading works!)

    Input Args: 
      tweets (list): A list of tweet objects (of type Status) to be saved. 
      path (str): The place where the tweets will be saved. 

    Returns: 
       None.
    """
    ### BEGIN SOLUTION
    '''
    if not Path(path).is_file():
      # use keys loaded in above by Method 1 or 2 
    '''

      # Saving the tweets to a file as "pickled" objects: 
    with open(path, "wb") as f:
      import pickle 
      pickle.dump(tweets, f)

    ### END SOLUTION

def load_tweets(path): 
    """Loads tweets that have previously been saved. 

    Calling load_tweets(path) after save_tweets(tweets, path) will produce 
    the same list of tweets. 

    Input Args: 
      path (str): The place where the tweets were to be saved. 

    Returns: 
      list: A list of tweet objects (of type Status), each representing one tweet 
    """
    ### BEGIN SOLUTION
    with open(path, 'rb') as f:
      import pickle
      tweets = pickle.load(f)
    
    return tweets
    ### END SOLUTION

# When you are done writing the functions above, run this cell to load 
#  @Dodgers tweets.  Note the function "get_tweets_with_cache".  You may find it
#  useful later. 

def get_tweets_with_cache(user_account_name, keys): 
    """Get recent tweets from one user, loading from a disk cache if available.
    
    The first time you call this function, it will download tweets by
    a user.  Subsequent calls will not re-download the tweets; instead
    they'll load the tweets from a save file in your local filesystem.
    All this is done using the functions you defined in the previous cell.
    This has benefits and drawbacks that often appear when you cache data:
    
    +: Using this function will prevent extraneous usage of the Twitter API.
    +: You will get your data much faster after the first time it's called.
    -: If you really want to re-download the tweets (say, to get newer ones,
       or because you screwed up something in the previous cell and your
       tweets aren't what you wanted), you'll have to find the save file
       (which will look like <something>_recent_tweets.pkl) and delete it.
    
    Args:
        user_account_name (str): The Twitter handle of a user, without the @.
        keys (dict): A Python dictionary with Twitter authentication keys 
    """
    save_path = "{}_recent_tweets.pkl".format(user_account_name)
    from pathlib import Path 
    if not Path(save_path).is_file():
        tweets = download_recent_tweets_by_user(user_account_name, keys)
        save_tweets(tweets, save_path)
    return load_tweets(save_path)

# Test your code with the LA Dodgers account
dodgers_tweets = get_tweets_with_cache("Dodgers", keys)

# If everything is working properly you can look at the tweets 
dodgers_tweets[0]

pprint.pprint(vars(dodgers_tweets[0]))

"""Check the @Dodgers tweets to make sure everything is working then load up the tweets from the account of your choosing."""

cr_tweets = get_tweets_with_cache('CriticalRole', keys)
cr_tweets[0]

"""## Exploring the dataset 

Twitter gives us a lot of information about each tweet, not just the tweet itself.  You can read the full documentation [here](https://dev.twitter.com/overview/api/tweets).  Look at the one tweet aboe to get a sense of the information we have available.

### Q3 - (15 pts) 

Which fields contain: 

1. the actual text of a tweet, 
2. the time when the tweet was posted, 
3. the source (device and app) from which the tweet was posted, 
4. the number of times the tweet was favorited, 
5. the number of times a tweet is retweeted?

To answer the question, write functions that extract each field from a tweet.  Each function should take a single tweet (Status object) as its argument.
"""

def extract_text(tweet): 
    # BEGIN SOLUTION 
    return tweet.text
    #END SOLUTION 

def extract_time(tweet): 
    # BEGIN SOLUTION 
    return tweet.created_at
    #END SOLUTION

def extract_source(tweet):
    # BEGIN SOLUTION 
    return tweet.source
    #END SOLUTION

def extract_fav_num(tweet):
    # BEGIN SOLUTION 
    return tweet.favorite_count
    #END SOLUTION

def extract_retweet_num(tweet):
    # BEGIN SOLUTION 
    return tweet.retweet_count
    #END SOLUTION

"""### Q4 - (10 pts)

Write a function called `make_dataframe`.  It should take as its argument a list of tweets like `dodgers_tweets` and return a `pandas` DataFrame.  The DataFrame should contain columns for all the fields in question 3.  The column names should be `text`, `time`, `source`, `favNum`, `retweetNum`. 
"""

def make_dataframe(tweets): 
    """Make a DataFrame from a list of tweets, with 5 requested fields. 

    Input Args: 
      tweets (list): a list of tweets, each one a Status object 

    Returns: 
      DataFrame: a pandas DataFrame containing one row for each element 
        of tweets and one column for each relevant field. 
    """
    ### BEGIN SOLUTION 
    
    text = []
    time = []
    source = []
    favNum = []
    retweetNum = []
    
    for tweet in tweets:
      text += [extract_text(tweet)]
      time += [extract_time(tweet)]
      source += [extract_source(tweet)]
      favNum += [extract_fav_num(tweet)]
      retweetNum += [extract_retweet_num(tweet)]
    
    df = pd.DataFrame({'text':text, 'time':time, 'source':source, 'favNum':favNum, 'retweetNum':retweetNum})
    return df 
    ### END SOLUTION

dodgers_df = make_dataframe(dodgers_tweets)
dodgers_df.head()

"""Now run this for your chosen Twitter account."""

cr_df = make_dataframe(cr_tweets)
cr_df.head()

"""### Q5 - (10 pts) 

Create a plot showing how many tweets came from each kind of source for the account you chose. 
"""

### BEGIN SOLUTION 
cr_df['source'].value_counts().plot.bar(figsize=(12,7), title='Count of the Tweet Source in Critical Role Tweets', rot=0)
### END SOLUTION

"""## Examining Text

The following questions comes from [https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/calculate-tweet-word-frequencies-in-python/](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/calculate-tweet-word-frequencies-in-python/)

Here is a function that removes the URLs (links) and emojis from the tweet text. By running the code that follows this function you should have then "cleanish" text.  *Note, it may not eliminate all emojis*
"""

import re

def remove_url(txt): 
    """Replace URLs found in a text string with nothing 
    (i.e. it will remove the URL from the string).
    Also, replaces the emoji with nothing. 

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """
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

"""This gets the text for the @Dodgers tweets."""

dodTweets = [tweet.text for tweet in dodgers_tweets]
dodTweets_no_urls = [remove_url(tweet) for tweet in dodTweets]
dodTweets_no_urls[0:4]

"""Now do the same thing for the account of your choosing."""

cr_tweets_text = [tweet.text for tweet in cr_tweets]
cr_tweets_no_urls = [remove_url(tweet) for tweet in cr_tweets_text]
cr_tweets_no_urls[:4]

"""### Q6 - (10 pts) 

Write code that will take your list of tweet text (`dodTweets_no_urls` for the @Dodgers tweets) and creates a list of lists containing the lower case words for each tweet. 

*Hint:* you may want to think about performing the operations on a single tweet text `dodTweets_no_urls[0]` - convert it to all lower case, break it into individual words.  Think about String methods [https://docs.python.org/3.7/library/stdtypes.html#string-methods](https://docs.python.org/3.7/library/stdtypes.html#string-methods)

*Hint:* Once you get the list of words from a single tweet text, collect all the tweet's texts in another list. 

```
[['test', 
  'string', 
  'text'],
 ['hello', 
  'world']]
```

Show `words_in_tweets` for your chosen account.
"""

words_in_tweets = []
for tweet in cr_tweets_no_urls:
  words = tweet.lower().split()
  words_in_tweets += words
words_in_tweets[:3]

"""### Q7 - (10 pts) 

Write code to take your list of lists of words and count the number of times each word appears.

You may want to look at using `itertools` to flatten the list. Also, look at the built-in Python library `collections`, which helps create a special type of a Python dictonary. The `collection.Counter` object has a useful built-in method `most_common` that will return the most commonly used words and the number of times that they are used.
"""

import itertools 
import collections 

word_count = pd.Series(words_in_tweets).value_counts()
word_count.head()

"""Reference:
1. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html

### Q8 - (10 pts) 

Plot the top 30 most frequently used words with their word counts. 

*Hint:* You may want to import the information from above into a Dataframe and use your normal plotting tools
"""

word_count.head(30).plot.bar(figsize=(12,7), title='Count of the Top 30 Words in Critical Role Tweets')

"""## Bonus - (5 pts) 

You may see a number of very common words as the most common, e.g., the, in, to, of, etc. You may want to remove those common words, these are typically referred to as "stop words" in the text analysis communities.

The python package `nltk` is used for text analysis. It provides a list of "stop words". Re-analyze the tweet text by removing stop words from consideration, and plot the 30 most popular words with their frequencies.
"""

import nltk

nltk.download('stopwords')

new_word_count = word_count[~word_count.index.isin(stopwords.words('english'))]
new_word_count.head()

new_word_count.head(30).plot.bar(figsize=(12,7), title='Count of the Top 30 Words in Critical Role Tweets Excluding Stop Words')

"""References:
1. https://stackoverflow.com/questions/19960077/how-to-filter-pandas-dataframe-using-in-and-not-in-like-in-sql
2. https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.isin.html
3. https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
"""
