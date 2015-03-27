#!/usr/bin/env python
#__author__ = 'ishan'
import sys
from gen_feature import compute_len_diff
from gen_feature import compute_avg_diff
from gen_feature import compute_avg_len


"""
gen_best_translations:
Finds the top ranked translation for every src sentences from
n-best list of hypothesis using the specified parameters(lambdas)
"""
def gen_best_translations_by_lambda(all_hyps, src_sen, lambdas, inc_lambdas,  cnt_untranslated):
    num_sents = len(all_hyps) / 200

    best_translations = []
    for s_no in xrange(0,num_sents):
        hyps_for_one_sent = all_hyps[s_no * 100:s_no * 100 + 100]
        (best_score, best) = (-1e300, '')

        # Compute avg len of all the sentences
        if inc_lambdas['avg_len_d']:
            avg_len = compute_avg_len(hyps_for_one_sent)

        for (num, hyp, feats) in hyps_for_one_sent:
            score = 0.0
            for feat in feats.split(' '):
                (k, v) = feat.split('=')
                score += lambdas[k] * float(v)

            # Adding rel length diff as a feature
            if inc_lambdas['len_d']:
                r_len_diff = compute_len_diff(src_sen[s_no][1].split(), hyp.split())
                score += lambdas['len_d'] * r_len_diff

            # Adding num of untranslated features as a feature
            if inc_lambdas['trans_w']:
                score += lambdas['trans_w'] *(-1 * cnt_untranslated[hyp])

            # Adding avg len diff in hypotheses as a feature
            if inc_lambdas['avg_len_d']:
                score += lambdas['avg_len_d'] * compute_avg_diff(hyp, avg_len)


            if score > best_score:
                (best_score, best) = (score, hyp)
        try:
            best_translations.append( best)
        except Exception:
            sys.exit(1)

    return best_translations

