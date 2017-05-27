#Programmer: Ryan Fogarty
#This program takes a keyword entered by the user on the command line and finds
#tweets using Tweepy API that match the search. Then these tweets are sent to the
#Tweet Sentiment API which determines whether or not each tweet is likely positive 
#or negative tweets in nature. These tweets are then displayed. 


#Imports
import sys
import pprint
import json
import urllib
import requests
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "2164289674-VrADphpZFHlRkhlKadEo7gUTHaoQhlNDefIw7Ly"
access_token_secret = "3gI5AXBQzOI3lx3A0PbgtRAHJ5ZraJ2mSlR56uKmHhIfg"
consumer_key = "0S4ONRveHc48YmTs4rCHvj6LF"
consumer_secret = "hem7ndc4MZBb63KeDqEF36iSfzgCUB5953iLZ8Avq2ZREGogmS"


class aTweet:
#This class holds the text of a specific tweet, and the username of the user
#that tweeted
    def __init__(self, tweet, username):
        self.tweet = tweet
        self.username = username

def get_tweets(search_term):
    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    tweets = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    results = tweets.search(q=search_term,  show_user = True)
    
    #with open('tweets.json', 'w') as fp:   #save tweets data, if needed
        #json.dump(results, fp)  
     
    all_tweets = []  #array to hold all tweet objects
    for result in (results["statuses"]):
        try:
            tweet = result["text"].encode("utf-8")
            user_name = result["user"]["screen_name"].encode("utf-8")
            tweetObj = aTweet(tweet, user_name)   #create object of text and username for given tweet
            all_tweets.append(tweetObj)    #append to all_tweets array
        except KeyError:
            print("key error")
   
    return all_tweets  #return array of tweet objects

    
def get_positive_tweets(all_tweets):   
    positive_tweets = []  #array to store tweets that return from API as positive
    for tweets in all_tweets:
        response = requests.get("https://jamiembrown-tweet-sentiment-analysis.p.mashape.com/api/?text=%s" % tweets.tweet,
          headers={
            "X-Mashape-Key": "s5uOK6NDnvmshuAXx45ksN51AzXLp1QeIqNjsnCeM9VynLTEbP",
            "Accept": "application/json" 
          } 
        )   
        jsonData = json.loads(response.text)   #load json response from tweet sentiment API call
        if (jsonData["sentiment"] == "positiive"):
            positive_tweets.append(tweets)   #append positive tweets to array
    for positive in positive_tweets:
        print("@", str(positive.username)[2:-1],": ", str(positive.tweet)[2:-1],"\n", sep = '')  #print such tweets to user


def main():
    print("Analyzing positive tweets...")
    arg_count= len(sys.argv)
    key_word = ""
    #following handles command line arguments 
    if (len(sys.argv)<2):
        print("No keywords entered, can't fetch positive tweets")
    else:
        for i in range(arg_count):
            if (i>0):
                key_word += (sys.argv[i])
                key_word += " "      
    all_tweets = get_tweets(key_word)
    get_positive_tweets(all_tweets)
    
main()