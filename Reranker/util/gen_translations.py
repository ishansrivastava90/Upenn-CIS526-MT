#!/usr/bin/env python
#__author__ = 'ishan'
import sys
from gen_feature import compute_len_diff

"""
gen_best_translations:
Finds the top ranked translation for every src sentences from
n-best list of hypothesis using the specified parameters(lambdas)
"""
def gen_best_translations_by_lambda(all_hyps, src_sen, lambdas, inc_lambdas,  cnt_untranslated):
    num_sents = len(all_hyps) / 100

    best_translations = []
    for s_no in xrange(0,num_sents):
        hyps_for_one_sent = all_hyps[s_no * 100:s_no * 100 + 100]
        (best_score, best) = (-1e300, '')

        for (num, hyp, feats) in hyps_for_one_sent:
            score = 0.0
            for feat in feats.split(' '):
                (k, v) = feat.split('=')
                score += lambdas[k] * float(v)

            if inc_lambdas['len_d']:
                # Adding rel length diff as a feature
                r_len_diff = compute_len_diff(src_sen[s_no][1].split(), hyp.split())
                score += lambdas['len_d'] * r_len_diff

            if inc_lambdas['trans_w']:
                # Adding num of untranslated features as a feature
                score += lambdas['trans_w'] *(-1 * cnt_untranslated[hyp])


            if score > best_score:
                (best_score, best) = (score, hyp)
        try:
            best_translations.append( best)
        except Exception:
            sys.exit(1)

    return best_translations

