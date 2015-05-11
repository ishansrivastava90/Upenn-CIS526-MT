#! /usr/bin/env python

from gen_feature import compute_untranslated
from gen_feature import compute_len_diff
from gen_feature import compute_avg_diff
from gen_feature import compute_avg_len

"""
Computes the best score among the hypotheses for a specified sen
Also returns the best translation( hypothesis )along with the best
score
"""
def compute_score(hyps_per_sen, src_sen, weights, src_tokens, cnt_untranslated_dict, inc_lambdas):

    (best_score, best) = (-1e300, '')

    # Compute avg len of all the sentences
    if inc_lambdas['avg_len_d']:
        avg_len = compute_avg_len(hyps_per_sen)

    for (num, hyp, feats) in hyps_per_sen:
        score = 0.0

        # Adding lm and tm prob features to the score
        for feat in feats.split(' '):
            (k, v) = feat.split('=')
            score += weights[k] * float(v)

        # Adding rel len feature to the score
        if inc_lambdas['len_d']:
            r_len_diff = compute_len_diff(src_sen.split(), hyp.split())
            score += weights['len_d'] * r_len_diff

        # Adding num of untranslated features as a feature
        if inc_lambdas['trans_w']:
            if cnt_untranslated_dict is None:
                cnt_untranslated = compute_untranslated(hyp, src_tokens)
            else:
                cnt_untranslated = cnt_untranslated_dict[hyp]
            score += weights['trans_w'] *(-1 * cnt_untranslated)

        # Adding avg diff in len as a feature
        if inc_lambdas['avg_len_d']:
            score += weights['avg_len_d'] * compute_avg_diff(hyp, avg_len)

        if score > best_score:
            (best_score, best) = (score, hyp)

    return best_score, best














