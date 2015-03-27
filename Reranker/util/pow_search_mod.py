#!/usr/bin/env python
import sys
import optparse
from collections import namedtuple

from gen_feature import compute_untranslated_all
from gen_feature import compute_avg_len
from gen_src_tokens import load_src_tokens
from gen_translations import gen_best_translations_by_lambda
from line_util import find_intersecting_line
from line_util import compute_line
from compute_bleu import compute_bleu

"""
Analysis -

1)
Starting with default values - 30 intersection sen + untranslated words as features
{'len_d': 0.5578249999996943, 'p(e)': -0.5732724526118395, 'p_lex(f|e)': -0.7963052574906557, 'p(e|f)': -0.823073912001155, 'trans_w': -0.9751794059140622}
0.290249639103

2)
{'len_d': -2.1509299000320934, 'p(e)': -0.5754389141990681, 'p_lex(f|e)': -0.5045099983958405, 'p(e|f)': -0.5914897157604302, 'trans_w': -0.8820829876451199}
0.291278703446

3)
-L 17.247330000000005 -l -0.5679431356242544 -s -0.5431890291489 -t -0.6134804052066087 -u -0.9583950432881909
??

4)
-L 17.247330000000005 -l -0.5679431356242544 -s -0.5431890291489 -t -0.6134804052066087 -u -0.9583950432881909  -a 0.602609547391371
0.28762839658 [2nd best on leaderboard]

5)
-L 17.247330000000005 -l -0.5754389141990681 -s -0.5045099983958405 -t -0.5914897157604302 -u -0.882082987645119 -a 0.602609547391371
0.286288050299 [3rd best on leaderboard]
"""


def length_check(ref, best_translations):
    # Length Check
    if len(ref) != len(best_translations):
        sys.stderr.write("Ref statements are not equal to best_translations")
        sys.exit(0)
    return



"""
Modified Powell Search - Search for optimum lambda parameters
Modular code. Uses scoring function. Flexibility to encode more features
"""
def powell_search_mod(opts):

    sys.stdout.write("Setting up src sentence, hyp, ref lists for processing.....\n\n")

    ref = [line.strip().split() for line in open(opts.reference)]
    src_sen = [line.split(' ||| ') for line in open(opts.source)]
    all_hyps = [pair.split(' ||| ') for pair in open(opts.input)]
    src_tokens = load_src_tokens(opts.token_file)
    num_sents = len(all_hyps) / 200

    # Initial values for lambdas
    lambdas = {'len_d'      : float(opts.ld),
               'p(e)'       : float(opts.lm),
               'p(e|f)'     : float(opts.tm1),
               'p_lex(f|e)' : float(opts.tm2),
               'trans_w'    : float(opts.tr),
               'avg_len_d'  : float(opts.av)}

    inc_lambdas = {'len_d'      : True,
                   'p(e)'       : True,
                   'p(e|f)'     : True,
                   'p_lex(f|e)' : True,
                   'trans_w'    : True,
                   'avg_len_d'  : True}


    # lambdas_order = ['p(e)', 'p(e|f)', 'p_lex(f|e)', 'len_d']


    # Declaring line with following fields
    line_t = namedtuple('line',['lambda_t', 'lambda_v','incline','offset'])

    # Pre-processing - Find the count for untranslated word for every sen
    cnt_untranslated = compute_untranslated_all(all_hyps, src_tokens)

    # Initialising total_max_bleu_score
    best_translations = gen_best_translations_by_lambda(all_hyps, src_sen, lambdas, inc_lambdas,  cnt_untranslated)
    best_translations_split = [line.strip().split() for line in best_translations]
    total_max_bleu_score = compute_bleu(ref, best_translations_split)

    sys.stdout.write("Initial bleu score with initial lambda values: %s\n" % str(total_max_bleu_score))

    converged = False
    num_iter = 0
    while not converged and num_iter <= 3:
        sys.stdout.write("\nRunning iteration: %s ....\n" % num_iter)
        num_iter += 1

        # Assuming that this iteration will converge
        converged = True

        # Iterating over every parameter
        for param in lambdas.keys():

            # Running for selected parameters
            if not inc_lambdas[param]:
                continue

            sys.stdout.write("Optimizing for param: %s\n" % param)

            thresh_points = list()

            # Iterating for all sentences
            for s_no in xrange(0,num_sents):
                hyps_for_one_sent = all_hyps[s_no * 100:s_no * 100 + 100]

                lines = list()
                lines_done = list()

                avg_len = compute_avg_len(hyps_for_one_sent)
                for (num, hyp, feats) in hyps_for_one_sent:
                    (incline, offset) = compute_line(hyp, feats, src_sen[s_no][1], lambdas, param, src_tokens, avg_len)
                    lines.append(line_t(param, lambdas[param], incline, offset))

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

                #   print "%s All intersection points found" % s_no

            # Sorting thershold points by param value
            thresh_points.sort()
            print len(thresh_points)

            # Deep copy the lambdas/params
            lambdas_t = dict(lambdas)

            # Generating the best translations
            initial_fuzz = 1
            lambdas_t[param] = thresh_points[0] - initial_fuzz
            best_translations = gen_best_translations_by_lambda(all_hyps, src_sen, lambdas_t, inc_lambdas,  cnt_untranslated)
            print "Computing best translations......"

            # Computing the initial bleu score
            length_check(ref, best_translations)
            argmax_lambda_v = lambdas_t[param]
            best_translations_split = [line.strip().split() for line in best_translations]
            max_bleu_score = compute_bleu(ref, best_translations_split)

            #print max_bleu_score

            # Finding the optimal lambda_v using the best bleu score
            for t_ind in xrange(1,len(thresh_points)):
                lambdas_t[param] = float(thresh_points[t_ind-1] + thresh_points[t_ind])/2
                best_translations = gen_best_translations_by_lambda(all_hyps, src_sen, lambdas_t, inc_lambdas,  cnt_untranslated)

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


if __name__=="__main__":

    optparser = optparse.OptionParser()
    optparser.add_option("-k", "--kbest-list", dest="input", default="../data/dev+test.100best", help="100-best translation lists")
    optparser.add_option("-z", "--source-sen", dest="source", default="../data/dev+test.src", help="Source language sen data")

    optparser.add_option("-l", "--lm", dest="lm", default=-0.5679431356242544, type="float", help="Language model weight")
    optparser.add_option("-t", "--tm1", dest="tm1", default=-0.6134804052066087, type="float", help="Translation model p(e|f) weight")
    optparser.add_option("-s", "--tm2", dest="tm2", default=-0.5431890291489, type="float", help="Lexical translation model p_lex(f|e) weight")
    optparser.add_option("-L", "--ld", dest="ld", default=-1.0, type="float", help="Relative len difference weight")
    optparser.add_option("-u", "--tr", dest="tr", default=-1.0, type="float", help="Untranslated words weight")
    optparser.add_option("-a", "--avg", dest="av", default=-1.0, type="float", help="Avg len difference in hypothesis weight")

    optparser.add_option("-r", "--ref", dest="reference", default="../data/dev.ref", help="Target language reference statements")
    optparser.add_option("-f", "--token-file", dest="token_file", default="../data/dev+test.dict", help="Src language word tokens")

    (opts, _) = optparser.parse_args()


    print powell_search_mod(opts)

