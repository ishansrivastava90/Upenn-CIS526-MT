#!/usr/bin/env python
# encoding: utf-8

import os
#import urllib3
#import certifi
 
import tweepy #https://github.com/tweepy/tweepy
#from tweepy import TweepError
import csv
import time
import json

#Twitter API credentials
consumer_key = "KbfYFTH2sEb5dcQrXnAdtCdo5"
consumer_secret = "cQRenKOJjUaHOXICDGrQt4wqglM6JstD3uyWcowWNorQpup6AN"
access_key = "2577377185-6ch5YLqVcVNwcCYHSYWiXLZ4vhqQetdP2MB72Mi"
access_secret = "vit3l2SofIBR2HtOuQXr0cJTm5oNSeVF7weMCwsa1BB65"

testApp_ishan_consumer_key = "I93rBcAJA58QYzO5PAfc61XTW"
testApp_ishan_consumer_secret = "UDbFtdC2rdaCw9uSD3ueh8kfshjQFcJucmwink2oEirTBB8N0g"
testApp_ishan_consumer_access_token = "97230209-4dN5Ec9IW2A8PkimaOjqvRZyQvwgktpw8I9bNFmLw"
testApp_ishan_consumer_access_token_secret = "hw8iVSO0K13KbmEByHEGWwZ7YINyo0v0zgseNVakWJEDv"


def print_self_tweets():
    
    #Authorize Twitter using application-only authentication
    auth = tweepy.OAuthHandler(testApp_ishan_consumer_key, testApp_ishan_consumer_secret)
    auth.set_access_token(testApp_ishan_consumer_access_token, testApp_ishan_consumer_access_token_secret)

    #Initiazlize Tweepy
    api = tweepy.API(auth)

    my_info = api.get_user("ishanarya90")
    print my_info.description

    my_tweets = api.home_timeline()
    #print my_tweets
    
    for tweet in my_tweets:
        print tweet.text



def get_all_tweets_by_handle(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
	
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
	
    #initialize a list to hold all the tweepy Tweets
    alltweets = []	
	
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = "artj97",count=200)
	
    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
	
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
	print "getting tweets before %s" % (oldest)
		
	#all subsiquent requests use the max_id param to prevent duplicates
	new_tweets = api.user_timeline(screen_name = "artj97",count=200,max_id=oldest)
		
	#save most recent tweets
	alltweets.extend(new_tweets)
		
	#update the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
		
	print "...%s tweets downloaded so far" % (len(alltweets))
	
    #transform the tweepy tweets into a 2D array that will populate the csv	
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
    #write the csv	
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
	writer = csv.writer(f)
	writer.writerow(["id","created_at","text"])
	writer.writerows(outtweets)
	
    pass


def get_all_tweets_by_user_ids(user_ids, user_id_dict):
    #Twitter only allows access to a users most recent 3240 tweets with this method
	
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
	
    cnt = 1
    for user_id in user_ids:
        print "Count %s. Extracting for User id %s ..." %(cnt, user_id)
        cnt+= 1    
        try:
            #initialize a list to hold all the tweepy Tweets
            alltweets = []	
	
            #make initial request for most recent tweets (200 is the maximum allowed count)
            new_tweets = api.user_timeline(user_id = user_id, count=200)
	
            #save most recent tweets
            alltweets.extend(new_tweets)
	
            # Checking if there are any tweets at all for the user
            if len(alltweets) == 0:
                print "No tweets found for id: "+user_id+"\n"
                f = open("User_Ids_w_no_tweets","a")
                f.write("No tweets found for id: "+user_id+"\n")
                f.close()
                continue
            
            #save the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
	
            #keep grabbing tweets until there are no tweets left to grab
            while len(new_tweets) > 0:
	        print "getting tweets before %s" % (oldest)
		
    	        #all subsiquent requests use the max_id param to prevent duplicates
	        new_tweets = api.user_timeline(user_id = user_id ,count=200,max_id=oldest)
	
    	        #save most recent tweets
	        alltweets.extend(new_tweets)
	
                #update the id of the oldest tweet less one
	        oldest = alltweets[-1].id - 1
	
	        print "...%s tweets downloaded so far" % (len(alltweets))

            #transform the tweepy tweets into a 2D array that will populate the csv	
            outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

        except tweepy.TweepError as e:
            print e
            f = open("User_Ids_with_errors","a")
            f.write("Caught a TweepError for id: "+user_id+"\n")
            f.close()
            continue

	
        #write the csv	
        #with open('tweets_by_user/%s_tweets.csv' % (user_id+user_id_dict[user_id]), 'wb') as f:
        with open('%s.csv' % (user_id_dict[user_id]), 'wb') as f:
	    writer = csv.writer(f)
	    writer.writerow(["id","created_at","text"])
	    writer.writerows(outtweets)
	
        pass
        
        print "Sleeping for 4 mins....."
        time.sleep(4*60)



def get_tweets_using_search_API(screen_handle, since_date, until_date):

    # Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    all_tweets = []
    since_date = "2011-01-01"
    until_date = "2014-12-31"
    search_q = "from%3Atheglamaz0n_"
#    search_q += screen_handle+" since%3A"+since_date+" until%3A"+until_date+"&src=typd"

    try:
        sp_tweets = api.search(search_q, rpp = 100)
    except tweepy.TweepError as e:
        print e
    
    for tw in sp_tweets:
        print tw.text
    #print sp_tweets[1].text
    



 
if __name__ == '__main__':
    #pass in the username of the account you want to download
    #get_all_tweets("artj97")

    # Getting tweets using Twitter Search API
    #get_tweets_using_search_API("theglamaz0n_","1313","32442")
    
    # Reading all the user_ids to be worked on    
    """
    f = open("../data/User_Ids/User_Ids_with_grad_date_2ndPass.csv","r")
    user_id_dict = dict()
    user_ids = []
    for line in f.readlines():
        if "from_id" in line:
            continue;
        line_split = line.strip().split(",")

        if line_split[0] not in user_id_dict.keys():
            date_s = line_split[1].split('/')
            if len(date_s[1]) < 2:
                date_s[1] = "0"+date_s[1]
            if len(date_s[0]) < 2:
                date_s[0] = "0"+date_s[0]
            #print "_"+date_s[2]+"_"+date_s[0]+"_"+date_s[1]
            user_id_dict[line_split[0]] = "_"+date_s[2]+"_"+date_s[0]+"_"+date_s[1]
            user_ids.append(line_split[0])
    f.close()
    #print user_ids
    """
    user_id_dict = dict()
    user_id_dict['1901042880'] = 'tweets_bhojpuri_panchayat_1901042880'
    get_all_tweets_by_user_ids(['1901042880'], user_id_dict)

    #Getting all the ids that were completed successfully
    """
    lst_files = os.listdir("../gen_data/tweets_by_user")
    user_ids_comp = []
    for file_n in lst_files:
        user_ids_comp.append(file_n.split('_')[0])
    #print user_ids_comp
    fw = open("../data/User_Ids/User_Ids_comp_successfully","w")
    fw.write("\n".join(['"User_id"']+user_ids_comp))
    fw.close()
    """

    # Getting all the ids that threw exceptions
    """
    f = open("../data/User_Ids/User_Ids_comp_failure","r")
    user_ids_w_err = []
    for ln in f.readlines():
        user_ids_w_err.append(ln.split()[5])
    f.close()
    #get_all_tweets_by_user_ids(user_ids_w_err, user_id_dict)
    """
    
    # Writing all tweets fow which extraction failed
    """
    user_ids_incomp = []
    for u_id in user_ids:
        if u_id not in user_ids_comp:
            user_ids_incomp.append(u_id)
    fw = open("../data/User_Ids/User_Ids_comp_failure","w")
    fw.write("\n".join(['"User_id"']+user_ids_incomp))
    fw.close()
    """

    # 2nd Pass over all ids not seen in case any for extraction
    """
    user_ids_seen = user_ids_w_err + user_ids_comp
    user_ids_2ndpass = []    
    for user_id in user_ids:
        if user_id not in user_ids_seen:
            user_ids_2ndpass.append(user_id)
    """

    #get_all_tweets_by_user_ids(user_ids_2ndpass[:50], user_id_dict)
    
