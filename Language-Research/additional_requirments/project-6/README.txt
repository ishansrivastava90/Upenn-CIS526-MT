Description of the contents in project-6

tweets/
Contains the tweets in CSV format from different sources. The tweet is in native Bhojpuri(Devangiri) script 
* tweets_geobased.csv - Tweets extracted from Bhojpuri speaking regions in India and Nepal. 
* tweets_data350.csv - Random sample of 350 tweets from tweets_geobased.csv
* tweets_label350.csv - 1 and 0 label for every tweet in tweets_data350.csv depending if it's a Bhojpuri tweet or not
* tweets_X_Id.csv - All the other files with names of this form contains tweets from specific twitter handle where X is
the twitter handle and Id is the twitter from_id for that handle

twitter-streamer/
Contains the provided twitter streaming API wrappers for tweet extraction based on geo locations and alongwith multiple
filtering and formatting options

extract_Tweets.py :
Extracts Tweets and metadata using twitter APIs using twitter handle or twitter from_id. The scripts stores the actual
tweet and the metadata in csv format 
