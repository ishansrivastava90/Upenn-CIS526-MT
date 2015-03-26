#!/usr/bin/env python

import sys
from gen_feature import compute_untranslated
from gen_feature import compute_len_diff

"""
find_intersecting_line:
Finding the next intersecting line with the current steepest line
"""
def find_intersecting_line(line_steep, lines, lines_done, curr_max_lambda, iter=sys.maxint):

    min_lambda_v = 1e300
    intersect_line = None

    num_iter = 0
    for l in lines:
        if l in lines_done or l.incline == line_steep.incline:
            continue

        if num_iter == iter:
            break

        lambda_v = float(l.offset - line_steep.offset)/(line_steep.incline - l.incline)
        if  curr_max_lambda < lambda_v < min_lambda_v:
            min_lambda_v = lambda_v
            intersect_line = l

        num_iter += 1

    if intersect_line is None:
        return intersect_line, min_lambda_v, False

    return intersect_line, min_lambda_v, True


"""
Computes the incline and the offset of a hypothesis
using features and required things
"""
def compute_line(hyp, feats, src_sen, lambdas, param, src_tokens):
    # Computing Total score => sum(lambda_i * h(x_i))
    tot_score = 0.0
    for feat in feats.split(' '):
        (k, v) = feat.split('=')
        tot_score += lambdas[k] * float(v)

    # Adding rel len feature to the score
    r_len_diff = compute_len_diff(src_sen.split(), hyp.split())
    tot_score += lambdas['len_d'] * r_len_diff

    # Adding num of untranslated features as a feature
    cnt_untranslated = compute_untranslated(hyp, src_tokens)
    tot_score += lambdas['trans_w'] *(-1 * cnt_untranslated)

    # Finding the incline for the current param
    incline = r_len_diff
    for feat in feats.split(' '):
        (k, v) = feat.split('=')
        if k == param:
            incline = float(v)
            break
    if param == "trans_w":
        incline = -1 * cnt_untranslated

    #Computing Line l: param -> score
    return incline, tot_score - lambdas[param]*incline


