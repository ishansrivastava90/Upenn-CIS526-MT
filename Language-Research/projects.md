# Additional Language Research Requirements

## 1. Harvest monolingual data
We crawled the following bhojpuri news websites to harvest monolingual data.

* http://tatkakhabar.com/ 
* http://bhojpurimedia.com/ 
* http://www.bhojpuria.com/v2/ 
* http://khabarlahariya.org/ 
* http://bhojpurika.com/ 
* http://www.anjoria.com/  
* http://www.thebhojpuri.com/ 

We collected bhojpuri data from 8605 webpages. From each webpage, we extracted the data within the unicode ranges of Devnagari script. The data is saved in the bhojpuri_data.json file. It has three fields

* docId : Document Id
* url : Url of the webpage
* content : Bhojpuri  Content of the webpage (in unicode)



## 2. Bilingual data for Bhojpuri Language

We looked up for potential sources of bilingual data on the web. We came across websites, newspaper journals, personal blogs etc with content in both the languages. Some of the websites are the same as the ones mentioned above. We cralwed these websites using a script. We were also able to find The Universal Declaration of Human Rights in both the languages. After extracting all the content, we aligned them sentence wise to generate a parallel corpus of ~280 sentences including some very long sentences from UDHR.

Some of the other sources for bilingual data -

* http://anjoria.com/v1/bhasha/bhojpuri-proverbs1.htm
* http://anjoria.com/v1/bhasha/bhojpuri-proverbs2.htm
* http://anjoria.com/v1/bhasha/bhojpuri-proverbs3.htm
* http://tatoeba.org/eng/sentences/show_all_in/bho/none/none/
* http://www.udhri.be/BHOJPURI%20Universal%20Declaration%20Of%20Human%20Rights.html


## 5. Language Identification System
Our Bhojpuri Language Identification System invloves a 2-step process to identify Bhojpuri language. Initially, we check if the given sentence is in unicode range of Devanagari script. Then, we check the proportion of bhojpuri words in the sentence using a dictionary. If the ratio of bhojpuri words in the sentence exceeds 0.8, we identify the sentence as Bhojpuri. The dictionary is a list of 96300 bhojpuri words extracted from the harvested monolingual data. 


We evaluated the system using sentences from other languages and dialects written in Devanagari script like Hindi, Bundeli, Awadhi and Bajjika. Our test set consisted 291 sentences(100 Bhojpuri sentences and 191 sentences in Hindi, Bundeli, Awadhi and Bajjika.)

	| Language 	| Number of sentences 	| Correct Predictions 	|
	|----------	|---------------------	|---------------------	|
	| Bhojpuri 	| 100                 	| 66                  	|
	| Hindi    	| 88                  	| 59                  	|
	| Awadhi   	| 35                  	| 32                  	|
	| Bajjika  	| 32                  	| 30                  	|
	| Bundeli  	| 36                  	| 31                  	|


The accuarcy on the test set is 74.9 %


 
## 6.Twitter Presence
For evaluating the presence of Bhojpuri, we employed 2 methods -

1. Geo-based tweets
2. Targeting specific public/popular twitter handles

For the 1st method, we used the bounding box tool provided to get specfic co-ordinates of the potential regions where the language is spoken. We then used the twitter streaming APIs to extract tweets from that region. The extraction was expanded to include tweets in all languages. We collected around 6926 tweets in total. I took a random sample of 350 tweets and labeled them as Bhojpuri or Not Bhojpuri. Out of 350, 51 were Bhojpuri tweets.

For the 2nd method, we searched for some popular twitter handles that had tweets in Bhojpuri. It included Bhojpuri celebrities, e-magazines handles, newpaper handles etc. We wrote a tweet extraction script using tweepy wrapper over twitter APIs to extract using twitter handles. We collected 5520 tweets with over 95 per cent of Bhojpuri tweets.

We also extracted metadata like creation_time and message_id for both the above methods.


## 9. Language Informant
In order to find informants, we posted on the Facebook page of Rangoli, the Indian Student Association, asking people who could help us with translating English sentence to Bhojpuri. 

We heard back from 3 volunteers: Aryaa Gautam, Pranav Sahay, Sanket Shukla.
We have included their facebook contacts in our submission.

We started off by creating three sets of 20 English sentences each. These sentences consisted of both long and short sentences. We made sure that all the sets had some sentences in common. This helped us to compare results.

Each informant translated, transliterated and aligned the Bhojpuri words to English words in his/her set to the best of their capabilities. Each informant provided us with a .txt file with 3 sentences for each target sentence.We collected all data and organized it in a single file. We labled the English sentence as "E", the syntactically correct translation with a label "T" and the aligned counter part of it as "A". The transliterated sentences in Devanagari script were labeled as "B".


	| Informant     | Translated    |Transliterated|Aligned  |No. of Translations/Sentence|
	|---------------|---------------|--------------|----------|----------------------------|
	| Aryaa Gautam  | 19            |       19     |   19     |  1
	| Pranav Sahay  |  8            |       0      |    8     |  1
    | Sanket Shukla |  7            |       7      |    7     |  1
    |Aayushi Dwivedi|  13		   |       0      |   26     |  1-3
    
    
  
