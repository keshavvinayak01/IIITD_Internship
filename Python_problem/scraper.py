#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import pandas as pd
#Twitter API credentials
consumer_key = "ta45DA7krxeJmWwBUmATugbL2"
consumer_secret = "q4tJtgjnQZtN44XfuyuOxhoYWJRseTjGq9dbRpBmJyWfM3yMQv"
access_key = "877213647243591680-pSCmzYWgpIH9HmCHXcSbmk4CFSo8wtR"
access_secret = "EARoGre9DXaH2nj5cVGOcnycwjtkeCNmAVbRoLmv15Qq7"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print( "...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv
	urls = []
	for i,tweet in enumerate(alltweets):
		url = []
		if 'media' in tweet.entities:
			for media in tweet.extended_entities['media']:
				url.append(media['media_url'])
		urls.append(url)
	outtweets = [[i, tweet.text	,tweet.created_at ,tweet.user.favourites_count,tweet.retweet_count,len(urls[i])] for i,tweet in enumerate(alltweets)]
	#write the csv	
	df = pd.DataFrame(columns=["id","text","created_at","favourites_count","retweet_count","no_images"])
	for tw in outtweets:
		df.loc[len(df)] = [tw[0],tw[1], tw[2],tw[3],tw[4],tw[5]]

	df.to_csv('midas-task.csv')
if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("midasIIITD")