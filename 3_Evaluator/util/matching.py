#!/usr/bin/env python
import stemming
import synonyms
from collections import OrderedDict
from collections import namedtuple

"""
Matches against all non-empty n-grams in all-grams tupleof the Reference

Returns the normalized of count of partially matched n-grams
"""
def match_partial(h, all_grams):
    #sys.stderr.write("Calculating score partial for sen - %s\n" %h)
    partial_score = 0
    tot_ngrams = 0

    for i, n_grams in enumerate(all_grams):
        #print n_grams
        for gram in n_grams:
            for k in range(0,i+1):
                if gram[k] in h:
                    partial_score += 1
                    break
        #sys.stderr.write("i=%s\n" %i)
        #l = len(n_grams)
        #sys.stderr.write("len=%s\n" %l)

        tot_ngrams += len(n_grams)
        #print n_grams

    if tot_ngrams == 0:
        return 0

    return float(partial_score)/tot_ngrams



"""
Matches against all non-empty n-grams in all-grams tuple of the Reference

Returns the normalized of count of fully matched n-grams
but not-necessarily in order
"""
def match_full(h, all_grams):
    #sys.stderr.write("Calculating score full for sen - %s\n" %h)
    full_score = 0
    tot_ngrams = 0

    for i, n_grams in enumerate(all_grams):
        #print n_grams
        for gram in n_grams:
            isMatched = True
            for k in range(0,i+1):
                if gram[k] not in h:
                    isMatched = False
                    break
            if isMatched:
                full_score += 1

        tot_ngrams += len(n_grams)

    if tot_ngrams == 0:
        return 0

    return float(full_score)/tot_ngrams


"""
Matches against all non-empty n-grams in all-grams tuple of the Reference

Returns the normalized of count of fully matched n-grams in order
"""
def match_ordered(h, all_grams):
    #sys.stderr.write("Calculating score Ordered for sen - %s\n" %h)
    ord_score = 0
    tot_ngrams = 0

    for i, n_grams in enumerate(all_grams):
        #print n_grams
        for gram in n_grams:
            isMatched = True
            ind = 0
            for k in range(0,i+1):
                if gram[k] not in h or h.index(gram[k]) < ind:
                    isMatched = False
                    break
                ind = h.index(gram[k])
            if isMatched:
                ord_score += 1
        tot_ngrams += len(n_grams)

    if tot_ngrams == 0:
        return 0

    return float(ord_score)/tot_ngrams

"""
Matches against all non-empty n-grams in all-grams tuple of the Reference

Returns the normalized of count of exactly matched n-grams (Order + Adjacency)
"""

def match_exact(h, all_grams):

    exact_score = 0
    tot_ngrams = 0


    for i, n_grams in enumerate(all_grams):
        marked_h = [0]*len(h)

        for gram in n_grams:
            isMatched = True
            if gram[0] not in h:
                continue

            indices = []
            prev_ind = h.index(gram[0])
            indices.append(prev_ind)
            for k in range(1,i+1):
                if gram[k] not in h or prev_ind + 1 != h.index(gram[k]):
                    isMatched = False
                    break
                prev_ind = h.index(gram[k])
                indices.append(prev_ind)

            if isMatched:
                marked = True
                for ind in indices:
                    if marked_h[ind] == 0:
                        marked = False
                        marked_h[ind] = 1
                if not marked:
                    exact_score += 1

        tot_ngrams += len(n_grams)

    if tot_ngrams == 0:
        return 0

    return float(exact_score)/tot_ngrams


"""
Matches unigrams in lists and return counts - Exact match
"""
def unigram_matches(h, ref_set):
    return sum(1 for word in h if word in ref_set )


"""
Matches unigrams in lists and return counts - Exact + Stem + Synonyms Match
Assumes both h and ref to be sets without duplicates. Allowes multiple words
in h to match to same word in ref
"""
def unigram_matches_extended_set(h, ref, filterOnPOS=False):
    #Exact Match
    exact_cnt = 0
    marked = [0]*len(h)
    for i,word in enumerate(h):
        if word in ref:
            exact_cnt += 1
            marked[i] = 1

    # Stemming
    ref_stemmed = stemming.stem_lists(ref)
    h_stemmed = stemming.stem_lists(h)

    #Match after stemming
    stem_cnt = 0
    for i,word in enumerate(h_stemmed):
        if word in ref_stemmed and marked[i] == 0:
            stem_cnt += 1
            marked[i]=1

    ref_fil = ref[:]

    # Finding POS tags
    if filterOnPOS:
        ref_fil = []
        for word in ref:
            pos = synonyms.find_pos(word)
            if pos != 'NN' and pos[0] != 'V' and pos != 'JJ' :
                continue
            r_pos = 'v' if pos[0] == 'V' else 'n' if pos == 'NN' else 'a'
            ref_fil.append((word, r_pos))

    syn_ref = synonyms.synonymify_list(ref_fil)

    #Match after synonymy
    syn_cnt = 0
    for i,word in enumerate(h):
        if marked[i] == 1:
            continue

        if filterOnPOS:
            pos = synonyms.find_pos(word)
            if pos != 'NN' and pos[0] != 'V' and pos != 'JJ' :
                continue

        syn_words = synonyms.synonymify(word)
        for syn_word in syn_words:
            if syn_word in syn_ref:
                marked[i] = 1
                syn_cnt += 1
                break



    return exact_cnt + stem_cnt + syn_cnt


"""
Matches unigrams in lists and return counts - Exact + Stem + Synonyms Match
Takes into consideration same words in sentences
"""
def unigram_matches_extended(h, ref_t, filterOnPOS=False):
    #Exact Match
    exact_cnt = 0
    marked = [0]*len(h)
    ref = ref_t[:]

    for i,word in enumerate(h):
        if len(ref) == 0:
            break
        if word in ref:
            exact_cnt += 1
            marked[i] = 1
            ref.remove(word)

    # Stemming
    ref_stemmed = stemming.stem_lists(ref)
    h_stemmed = stemming.stem_lists(h)

    #Match after stemming.py
    stem_cnt = 0
    for i,word in enumerate(h_stemmed):
        if word in ref_stemmed and marked[i] == 0:
            stem_cnt += 1
            marked[i]=1
            ind = ref_stemmed.index(word)
            ref_stemmed.remove(ref_stemmed[ind])
            ref.remove(ref[ind])

    ref_fil = ref[:]

    # Finding POS tags
    if filterOnPOS:
        ref_fil = []
        for word in ref:
            pos = synonyms.find_pos(word)
            if pos != 'NN' and pos[0] != 'V' and pos != 'JJ' :
                continue
            r_pos = 'v' if pos[0] == 'V' else 'n' if pos == 'NN' else 'a'
            ref_fil.append((word, r_pos))

    syn_ref = synonyms.synonymify_dict(ref_fil)

    #Match after synonymy
    syn_cnt = 0
    list_with_count = namedtuple("list_with_count","syn, count")
    for i,word in enumerate(h):
        if marked[i] == 1:
            continue

        if filterOnPOS:
            pos = synonyms.find_pos(word)
            if pos != 'NN' and pos[0] != 'V' and pos != 'JJ' :
                continue

        syn_words = list(OrderedDict.fromkeys([word] + synonyms.synonymify(word)))
        for syn_word in syn_words:
            if syn_word in syn_ref:
                marked[i] = 1
                syn_cnt += 1
                if syn_ref[syn_word].count -1 == 0:
                    del syn_ref[syn_word]
                else:
                    syn_ref[syn_word] = list_with_count(syn_ref[syn_word].syn, syn_ref[syn_word].count -1)
                break
            else:
                breakFromOuter = False
                for syn_key in syn_ref.keys():
                    if syn_word in syn_ref[syn_key].syn:
                        marked[i] = 1
                        syn_cnt += 1
                        if syn_ref[syn_key].count -1 == 0:
                            del syn_ref[syn_key]
                        else:
                            syn_ref[syn_key] = list_with_count(syn_ref[syn_key].syn, syn_ref[syn_key].count -1)
                        breakFromOuter = True
                        break
                if breakFromOuter:
                    break


    return exact_cnt + stem_cnt + syn_cnt


