#!/usr/bin/env python

# written by Adam Lopez

import optparse
import sys

import bleu

def compute_bleu(ref_list, hyp_list):
    stats = [0 for i in xrange(10)]
    for (r,h) in zip(ref_list, hyp_list):
        stats = [sum(scores) for scores in zip(stats, bleu.bleu_stats(h,r))]
    return bleu.bleu(stats)


if __name__=="__main__":
    optparser = optparse.OptionParser()
    optparser.add_option("-r", "--reference", dest="reference", default="../data/dev.ref", help="Target language reference sentences")
    (opts,_) = optparser.parse_args()

    ref = [line.strip().split() for line in open(opts.reference)]
    hyp = [line.strip().split() for line in sys.stdin]

    print compute_bleu(ref, hyp)


