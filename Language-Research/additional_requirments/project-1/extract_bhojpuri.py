#/usr/bin/env python

###################################################################
### Extracts Bhojpuri Data from crawled html pages  


import os,re
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import json
from nltk import word_tokenize, sent_tokenize
from string import punctuation

# Checks if the given string is in ascii
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# Checks if the given string is written in devanagari script
def is_devanagari(s, thresh = 0.7):
    if len(s) == 0 :
        return False
    per = sum([1 if u'\u0900' <= c <= u'\u097f' else 0 for c in s ])*1.0/len(s);
    if per >= thresh :
	return True;
    return False

# Replaces the extra whitspaces
def preprocess(data) :
    return re.sub(r'\s+', ' ', data).strip()

# Extracts all the filenames from a directory
def get_files(root="/home/moumaddela/LanguageResearch/WebPages") :
    dir_list = os.listdir(root)
    file_list = [];
    for d in dir_list :
        dir_path = root + "/" + d 
        files = os.listdir(dir_path) 
        for f in files :
	    file_list.append( dir_path + "/" + f )
    return file_list

def check_content(content) :
    return content is not None and len(content) > 0 and is_devanagari(content)


'''
## 1. Extract JSON Format file from crawled Webpages 
count = 0;
file_list = get_files();
docs = [];
for f in file_list :

    if count%50 == 0 :
	print count

    # Read bhojpuri html files
    fp =  open(f,'r')
    url = fp.readline().strip()
    content = fp.read()
    fp.close()

    # Extract Bhojpuri Content from html file 
    soup = BeautifulSoup(content)
    data = "";

    for link in soup.find_all('p'):
        content = link.text;
        if check_content(content) :
            data += content.strip() + u"\n";
   
    for link in soup.find_all('meta'):
        if link.has_attr('content') :
	    content = link.get('content')
            if check_content(content) :   
	    	data += content.strip() + u"\n";

    for link in soup.find_all('a') :
        content = link.text;
        if check_content(content) :
            data += content.strip() + u"\n";
 
    data = data.strip();
    if len(data) > 0 :
    	doc_dict = {};
    	doc_dict["url"] = url ;
    	doc_dict["content"] = data.strip();
    	doc_dict["doc_id"] = count;
    	doc_dict["raw_htmlfile"] = f;
	docs.append(doc_dict);
        count += 1

data = repr(docs);
data_string = json.dumps(docs); 
fp = open('bhojpuri_data.json','w')
fp.write(data_string)
fp.close()
'''


'''
## 2. Extract Bhojpuri Sentences
import codecs
fp = codecs.open('bhojpuri_data_new.json','r','utf8')
data_string = fp.read()
fp.close();
decoded = json.loads(data_string)
fp = codecs.open('bhojpuri_sentences_new.txt','w','utf8')
for (ind,d) in enumerate(decoded) :
    if ind%100 == 0 :
        print ind
    content =  d["content"]
    sents = content.split("\n") 
    for sent in sents :
        sent = sent.strip()
        for s in sent.split( u"\u0964" ) :
	    if len(s.strip())  :
	    	fp.write( s.strip() + "\n" ) 
fp.close()
'''

'''
## 3. Extract Bhojpuri unigrams/words 
import codecs
fp = codecs.open('bhojpuri_sentences.txt','r','utf-8')
bhojpuri_unigrams = set();
count = 0
for line in fp :
    if count%1000==0 :
        print count
        
    tokens = [ t.strip() for t in word_tokenize(line) if len(t.strip()) > 0 ];
    bhojpuri_unigrams.update(tokens)
    count += 1
fp.close()

fp = codecs.open("bhojpuri_words.txt","w", 'utf-8')
for unigram in list(bhojpuri_unigrams) :
    unigram = unigram.strip();
    if not is_ascii(unigram) :
        unigram = ''.join( [ c for c in unigram if u'\u0900' <= c <= u'\u097f' ] )    
        fp.write(unigram + u"\n") 
fp.close()
'''
