#! /usr/bin/env python

from collections import namedtuple

import sys
import optparse

from compute_bleu import compute_bleu
from gen_feature import compute_len_diff
from line_util import find_intersecting_line
from gen_translations import gen_best_translations_by_lambda

"""
Analysis -

Starting with default values - 30 intersection sen
{'len_d': 17.247330000000005, 'p(e)': -0.6548433300854343, 'p_lex(f|e)': -1.8438869077669446, 'p(e|f)': -0.5076955944831827}
0.277715086669

Starting with default values - 70 intersection sen
{'len_d': 17.247330000000005, 'p(e)': -0.6562940989238049, 'p_lex(f|e)': -1.8487510567805798, 'p(e|f)': -0.5171258477375932}
0.277811827755

"""

def length_check(ref, best_translations):
    # Length Check
    if len(ref) != len(best_translations):
        sys.stderr.write("Ref statements are not equal to best_translations")
        sys.exit(0)
    return


"""
Powell Search - Search for optimum lambda parameters
"""
def powell_search(opts):

    sys.stdout.write("Setting up src sentence, hyp, ref lists for processing.....\n\n")

    ref = [line.strip().split() for line in open(opts.reference)]
    src_sen = [line.split(' ||| ') for line in open(opts.source)]
    all_hyps = [pair.split(' ||| ') for pair in open(opts.input)]
    num_sents = len(all_hyps) / 200

    # Initial values for lambdas
    lambdas = {'len_d'      : float(opts.ld),
               'p(e)'       : float(opts.lm),
               'p(e|f)'     : float(opts.tm1),
               'p_lex(f|e)' : float(opts.tm2)}

    inc_lambdas = {'len_d'      : True,
                   'p(e)'       : True,
                   'p(e|f)'     : True,
                   'p_lex(f|e)' : True,
                   'trans_w'    : False }


    # lambdas_order = ['p(e)', 'p(e|f)', 'p_lex(f|e)', 'len_d']


    # Declaring line with following fields
    line_t = namedtuple('line',['lambda_t', 'lambda_v','incline','offset'])

    # Initialising total_max_bleu_score
    best_translations = gen_best_translations_by_lambda(all_hyps, src_sen, lambdas, inc_lambdas, None)
    best_translations_split = [line.strip().split() for line in best_translations]
    total_max_bleu_score = compute_bleu(ref, best_translations_split)

    sys.stdout.write("Initial bleu score with initial lambda values: %s\n" % str(total_max_bleu_score))

    converged = False
    num_iter = 1
    while not converged and num_iter <=3:
        sys.stdout.write("\nRunning iteration: %s ....\n" % num_iter)
        num_iter += 1

        # Assuming that this iteration will converge
        converged = True

        # Iterating over every parameter
        for param in lambdas.keys():
            sys.stdout.write("Optimizing for param: %s\n" % param)

            thresh_points = list()

            # Iterating for all sentences
            for s_no in xrange(0,num_sents):
                hyps_for_one_sent = all_hyps[s_no * 100:s_no * 100 + 100]

                lines = list()
                lines_done = list()

                for (num, hyp, feats) in hyps_for_one_sent:
                    # Computing Total score => sum(lambda_i * h(x_i))
                    tot_score = 0.0
                    for feat in feats.split(' '):
                        (k, v) = feat.split('=')
                        tot_score += lambdas[k] * float(v)
                    r_len_diff = compute_len_diff(src_sen[s_no][1].split(), hyp.split())
                    tot_score += lambdas['len_d'] * r_len_diff

                    # Finding the incline for the current param
                    incline = r_len_diff
                    for feat in feats.split(' '):
                        (k, v) = feat.split('=')
                        if k == param:
                            incline = float(v)
                            break

                    # TODO: Check the score logic.
                    #Computing Line l: param -> score
                    lines.append(line_t(param, lambdas[param], incline, tot_score - lambdas[param]*incline ))

                # Computing the line with the steepest incline
                lines = sorted(lines, key=lambda x: (x.incline, -x.offset))
                line_steep = lines[0]
                lines_done.append(line_steep)

                # Finding all intersection points
                line_found = True
                curr_max_thresh =-1 * sys.maxint
                while line_found:
                    (intersect_line, min_lambda_v, line_found) = find_intersecting_line(line_steep, lines, lines_done, curr_max_thresh, 70)
                    curr_max_thresh = min_lambda_v
                    thresh_points.append(min_lambda_v)
                    lines_done.append(intersect_line)

                    line_steep = intersect_line

                #print "%s All intersection points found" % s_no

            # Sorting thershold points by param value
            thresh_points.sort()
            print len(thresh_points)

            # Deep copy the lambdas/params
            lambdas_t = dict(lambdas)
            # Generating the best translations
            initial_fuzz = 1

            lambdas_t[param] = thresh_points[0] - initial_fuzz
            best_translations = gen_best_translations_by_lambda(all_hyps, src_sen, lambdas_t, inc_lambdas, None)

            # Computing the initial bleu score
            length_check(ref, best_translations)
            argmax_lambda_v = lambdas_t[param]
            best_translations_split = [line.strip().split() for line in best_translations]
            max_bleu_score = compute_bleu(ref, best_translations_split)

            #print max_bleu_score

            # Finding the optimal lambda_v using the best bleu score
            for t_ind in xrange(1,len(thresh_points)):
                lambdas_t[param] = float(thresh_points[t_ind-1] + thresh_points[t_ind])/2
                best_translations = gen_best_translations_by_lambda(all_hyps, src_sen, lambdas_t, inc_lambdas, None)

                length_check(ref, best_translations)
                best_translations_split = [line.strip().split() for line in best_translations]
                bleu_score = compute_bleu(ref, best_translations_split)
                if bleu_score > max_bleu_score:
                    max_bleu_score = bleu_score
                    argmax_lambda_v = lambdas_t[param]

                #print "%s t_ind max_bleu_Score %s" %(t_ind, max_bleu_score)

            # Take the param value if the best bleu score is greater
            if max_bleu_score > total_max_bleu_score:
                lambdas[param] = argmax_lambda_v
                total_max_bleu_score = max_bleu_score
                converged = False

                sys.stdout.write("New max bleu score is: %s\n" % total_max_bleu_score)
                print lambdas

    return lambdas

###################################################################################################################
###################################################################################################################


if __name__=="__main__":

    optparser = optparse.OptionParser()
    optparser.add_option("-k", "--kbest-list", dest="input", default="../data/dev+test.100best", help="100-best translation lists")
    optparser.add_option("-z", "--source-sen", dest="source", default="../data/dev+test.src", help="Source language sen data")
    optparser.add_option("-l", "--lm", dest="lm", default=-1.0, type="float", help="Language model weight")
    optparser.add_option("-t", "--tm1", dest="tm1", default=-0.5, type="float", help="Translation model p(e|f) weight")
    optparser.add_option("-s", "--tm2", dest="tm2", default=-0.5, type="float", help="Lexical translation model p_lex(f|e) weight")
    optparser.add_option("-L", "--ld", dest="ld", default=-1.0, type="float", help="Relative len difference weight")
    optparser.add_option("-u", "--tr", dest="tr", default=-1.0, type="float", help="Untranslated words weight")
    optparser.add_option("-r", "--ref", dest="reference", default="../data/dev.ref", help="Target language reference statements")
    optparser.add_option("-a", "--avg", dest="av", default=-1.0, type="float", help="Avg len difference in hypothesis weight")
    optparser.add_option("-f", "--token-file", dest="token_file", default="../data/dev+test.dict", help="Src language word tokens")

    (opts, _) = optparser.parse_args()


    print powell_search(opts)




















