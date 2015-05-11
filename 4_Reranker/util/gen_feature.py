#!/usr/bin/env python

import sys

from collections import defaultdict
import pickle
from pickle import PickleError

"""
Computes relative len diff of hypotheses and src sen as a
feature
"""
def compute_len_diff(src, hyp):
    return -1 + float(abs(len(src) - len(hyp)))/len(src)

def compute_len_diff2(src, hyp):
        return -1*float(abs(len(src) - len(hyp)))/len(src)


"""
Computes # of untranslated words for the specified hypotheses
as a feature
"""
def compute_untranslated(hyp, src_tokens):
    cnt = 0
    for t in hyp.strip().split():
        if t in src_tokens:
            cnt  +=1

    return cnt

"""
Computes difference of hypothesis length and the avg length
"""
def compute_avg_diff(hyp, avg_len):
    return -1 * abs(len(hyp.split()) - avg_len)



"""
Computes a 2000 len feature vector of top 2000 words from the 100best
translations for training
"""
def compute_unigram_feat_vec(top_list, hyp):

    unigram_vec = [0]*2000
    for ind,word in enumerate(top_list):
        if word in hyp.split():
            unigram_vec[ind] = 1

    return unigram_vec



#######################################################################
# Utilities
#######################################################################

"""
Util for computing # of untranslated words for all the hypotheses.
Used compute_untranslated above.
"""
def compute_untranslated_all(all_hyps, src_tokens, div_factor= 200):

    cnt_untranslated =defaultdict()

    # Iterating for all sentences
    num_sents = len(all_hyps) / div_factor
    for s_no in xrange(0,num_sents):
        hyps_for_one_sent = all_hyps[s_no * 100:s_no * 100 + 100]

        for (num, hyp, feats) in hyps_for_one_sent:
            cnt = compute_untranslated(hyp, src_tokens)
            cnt_untranslated[hyp] = cnt

    return cnt_untranslated



"""
Util to compute avg len for all hypotheses for
a sentence
"""
def compute_avg_len(hyps):
    if hyps is None:
        return 0
    return float(sum(len(hyp.split()) for (_,hyp,_) in hyps))/len(hyps)


"""
Util for loading and verifying the top 2000 pickled tunigram
feature vector
"""
def load_top2000_unigrams():
    try:
        unigram_vec = pickle.load(open("../data/unigram-feat-vec.p","rb"))
    except PickleError as e:
        print e
        sys.exit(0)

    return unigram_vec
