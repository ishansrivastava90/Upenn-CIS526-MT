#/usr/bin/env python

import os,re
from nltk import word_tokenize, sent_tokenize
from string import punctuation
import optparse

###########################################################################################
###  Bhojpuri Language Identification System

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="final_test_sentences.txt", help="Sample Test sentences")
optparser.add_option("-d", "--dict", dest="dictionary", default="bhojpuri_words.txt", help="Path to list of bhojpuri words")
opts = optparser.parse_args()[0]

threshold_unicode = 0.7
threshold_bhojpuri = 0.8
# Checks if the given string is in ascii
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# Checks if the given string is written in devanagari script
def is_devanagari(s):
    if len(s) == 0 :
        return False
    per = sum([1 if u'\u0900' <= c <= u'\u097f' else 0 for c in s ])*1.0/len(s);
    if per > threshold_unicode :
	return True;
    return False

# Replaces the extra whitspaces
def preprocess(data) :
    return re.sub(r'\s+', ' ', data).strip()

def check_content(content) :
    return content is not None and len(content) > 0 and is_devanagari(content)

import codecs
def load_words( f="bhojpuri_words.txt" ) :
    fp = codecs.open( f,'r', 'utf8' )
    dictionary = [];
    for line in fp :
        l = line.strip() ;
        dictionary.append(l)
    fp.close()
    return dictionary

def get_lang_id(data, word_dict) :
    data =  preprocess(data)
    tokens = [ t.strip() for t in word_tokenize(line) if len(t.strip()) > 0 ]
    if len(tokens) > 0 :
        per = len(set(word_dict).intersection(set(tokens)))*1.0/len(tokens)
        if per > threshold_bhojpuri :
	    return True
    return False
  

fp = codecs.open(opts.input, 'r', 'utf8')
word_dict = load_words(opts.dictionary)
count = 0
tcount = 0
for line in fp :
     
    line = line.strip();
    print line  
    label = "False"
    if check_content(line) and get_lang_id(line, word_dict) :
        label = "True"
    print label

