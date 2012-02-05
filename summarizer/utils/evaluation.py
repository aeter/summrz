#Copyright 2011, Adrian Nackov
#Released under BSD licence (3 clause):
#http://www.opensource.org/licenses/bsd-license.php

from nltk.util import ngrams

def rouge(n, auto_summary_words, original_summary_words):
    auto_summary_ngrams = ngrams(auto_summary_words, n)
    original_summary_ngrams = ngrams(original_summary_words, n)
    denominator = len(original_summary_ngrams)
    numerator = len([_ for _ in auto_summary_ngrams
                     if _ in original_summary_ngrams])
    return foat(numerator) / foat(denominator)
