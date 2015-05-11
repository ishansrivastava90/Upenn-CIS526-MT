#!/usr/bin/env python
import optparse
from string import punctuation

def is_num(st):
    return any(i.isdigit() for i in st)


def gen_dict_tokens(file_in, file_out):
    f_in = open(file_in)

    print "Generating tokens ..."
    tokens = []
    for l in f_in.readlines():
        l_split = l.split(" ||| ")
        for token in l_split[1].strip().split():
            if token not in tokens and token not in punctuation and not is_num(token):
                tokens.append(token)
    f_in.close()

    print "Writing to the file"
    f_out = open(file_out, "w")
    f_out.write("\n".join(tokens))
    f_out.close()

    return


def load_src_tokens(file_in):
    tokens = []

    f = open(file_in)
    for token in f.readlines():
        tokens.append(token.strip())

    return tokens


if __name__=="__main__":
    optparser = optparse.OptionParser()
    optparser.add_option("-r", "--source-sen", dest="source", default="../data/dev+test.src", help="Source language sen data")
    (opts, _) = optparser.parse_args()

    gen_dict_tokens(opts.source,"dev+test.dict")

