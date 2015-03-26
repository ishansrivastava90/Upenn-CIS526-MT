#!/usr/bin/env python

from collections import defaultdict

"""
Computes relative len diff of hypotheses and src sen as a
feature
"""
def compute_len_diff(src, hyp):
    return -1 + float(abs(len(src) - len(hyp)))/len(src)


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
