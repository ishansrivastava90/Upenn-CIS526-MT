#!/usr/bin/env python

from nltk.stem.porter import *

def stem_lists(l):
    l_stemmed = list()
    for x in l:
        l_stemmed.append(stem_with_exception(x))
    return l_stemmed

def stem_with_exception(word):
    stemmer = PorterStemmer()
    try:
        return stemmer.stem(word)
    except UnicodeDecodeError:
        return word
