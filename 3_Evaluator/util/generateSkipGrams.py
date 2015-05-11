#!/usr/bin/env python

def gen_k_skip_ngrams(sentence,k,n):

    # Assumes the sentence is already tokenized into a list
    if n == 0 or len(sentence) == 0:
        return None

    grams = []
    for i in range(len(sentence)-n+1):
        grams.extend(gen_recursively(sentence[i:],k,n))
    return grams


def gen_recursively(sentence, k, n):
    if n == 1:
        return [[sentence[0]]]
    grams = []
    for j in range(min(k+1,len(sentence)-1)):
        skipped_ngrams = gen_recursively(sentence[j+1:],k-j,n-1)
        if skipped_ngrams is not None:
            for gram in skipped_ngrams:
                grams.append([sentence[0]]+gram)
    return grams

if __name__=="__main__":
    sen = ['a','b','c','d','e']#,'f','g','h','i','j','k','l','m','n','o','p']
    print gen_k_skip_ngrams(sen, 2, 2)