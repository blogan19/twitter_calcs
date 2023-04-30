import sys
from os import environ
import tweepy
from main import Calculation
import credentials

client = tweepy.Client(bearer_token=BEARER, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_KEY, access_token_secret=ACCESS_SECRET)

#client.create_tweet(text="test")
try:
    calculation = Calculation('random')
    question = calculation.generate_question()
    client.create_tweet(text=question["question"])
except: 
    pass
    print(question)


#https://funsizeathlete.medium.com/my-first-twitter-bot-using-python-and-heroku-e3ef83578f58