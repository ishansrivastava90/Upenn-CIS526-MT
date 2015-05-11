#!/usr/bin/env python

from nltk.corpus import wordnet as wn
from collections import defaultdict
from collections import namedtuple
from collections import OrderedDict

#from nltk.tag.hunpos import HunposTagger

def synonymify(word, pos="n", filterOnPOS=False):
    synonym_l = []
    for sset in wn.synsets(word):
        if filterOnPOS and str(sset.pos) != pos and pos != "a" :
            continue
        if filterOnPOS and pos == "a" and str(sset.pos) != 's' and str(sset.pos) != 'a' :
            continue

        for syn in wn.synset(str(sset.name)).lemmas:
            synonym_l.append(str(syn.name))

    return synonym_l

def synonymify_list(list, filterOnPOS=False):
    synonym_list = []
    for word_pos_pair in list:
        if filterOnPOS:
            synonym_list.extend(synonymify(word_pos_pair[0], word_pos_pair[1], filterOnPOS))
        else:
            synonym_list.extend(synonymify(word_pos_pair, "", filterOnPOS))

    return synonym_list

def synonymify_dict(lst, filterOnPOS=False):
    synonym_dict = defaultdict()
    list_with_count = namedtuple("list_with_count","syn, count")
    for word_pos_pair in lst:
        if filterOnPOS:
            if word_pos_pair not in synonym_dict:
                word_syns = synonymify(word_pos_pair[0], word_pos_pair[1], filterOnPOS)
                unique_syn = list(OrderedDict.fromkeys(word_syns))
                t = list_with_count(unique_syn, 1)
            else:
                t = list_with_count(synonym_dict[word_pos_pair].syn, synonym_dict[word_pos_pair].count+1)
            synonym_dict[word_pos_pair] = t
        else:
            if word_pos_pair not in synonym_dict:
                word_syns = synonymify(word_pos_pair,"", filterOnPOS)
                unique_syn = list(OrderedDict.fromkeys(word_syns))
                t = list_with_count(unique_syn, 1)
            else:
                t = list_with_count(synonym_dict[word_pos_pair].syn, synonym_dict[word_pos_pair].count+1)
            synonym_dict[word_pos_pair] = t

    return synonym_dict


def find_pos(word):
 #   ht = HunposTagger('../res/hunpos-1.0-linux/en_wsj.model','../res/hunpos-1.0-linux/hunpos-tag')
 #   tag_list = ht.tag([word])
 #   return tag_list[0][1]
    return word

def find_pos_list(list):
    #ht = HunposTagger('../res/hunpos-1.0-linux/en_wsj.model','../res/hunpos-1.0-linux/hunpos-tag')
    #tag_list = ht.tag(list)

    return list
