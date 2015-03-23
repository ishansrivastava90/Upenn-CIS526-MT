#!/usr/bin/env python

import subprocess


def br_srch_on_prob_features():
    lm=-0.1
    tm=-0.1
    tm_lex=-0.1

    max_bleu = 0.0
    for i in xrange(1,11):
        for j in xrange(1,11):
            for k in xrange(1,11):
                ppy = subprocess.Popen(['python', '../src/rerank', '-l', str(i*lm), '-t', str(j*tm),  '-s',
                                    str(k*tm_lex)],stdout=subprocess.PIPE)
                outp= subprocess.check_output(['python','compute-bleu'],stdin=ppy.stdout)
                if outp > max_bleu:
                    print "lm = "+str(i*lm)+" tm = "+str(j*tm)+" tm_lex = "+str(k*tm_lex)+" gives bleu "+str(outp)
                    max_bleu = outp


def br_srch_on_len_weight():
    # Using the tuned prob features
    lm=-0.7
    tm=-0.4
    tm_lex=-0.9
    ln_wt = -0.1

    max_bleu = 0.0
    for i in xrange(-11,21):
        ppy = subprocess.Popen(['python', '../src/rerank2', '-l', str(lm), '-t', str(tm),  '-s',str(tm_lex),'-L', str(i*ln_wt)],stdout=subprocess.PIPE)
        outp= subprocess.check_output(['python','compute-bleu'],stdin=ppy.stdout)
        if outp > max_bleu:
            print "ln_wt = "+str(i*ln_wt)+" gives bleu "+str(outp)
            max_bleu = outp


if __name__=="__main__":
    br_srch_on_len_weight()

