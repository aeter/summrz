#!/usr/bin/env python

'''
A module for creating summaries from larger texts. Using semantics considerably
slows the module. It may run slow on larger texts even if not using semantics.
The code is prototypal.
'''

import argparse
import json
import os
import pickle
import sys

from clustering import similarity_matrix, cluster
from preprocessing import prepare
from classifier import Article, features


def get_classifier():
    with open("naive-bayes.pkl", "r") as f:
        return pickle.load(f)

def get_summary(title, article, num_sentences=5, use_semantics=False):
    '''
    Article and title are plaintext. Sentences is the number of sentences in the
    summary.
    '''
    article_sents = prepare(article)

    # remember the index of each sentence as they appear in the text
    # in order to be able to show the sentences in the order they appear
    # in the text
    for i,sent in enumerate(article_sents):
        sent.index_in_text = i

    # separate the text into groups
    matrix = similarity_matrix(article_sents, use_semantics=use_semantics)
    clusters = cluster(num_sentences, matrix)

    assert len(clusters) == len(article_sents), "Wrong number of clusters"
    for i,sent in enumerate(article_sents):
        sent.cluster_num = clusters[i]

    # for each group, select the sentence which has the highest
    # probability to be a summary sentence.
    result = {}
    summary_classifier = get_classifier()
    for i,sent in enumerate(article_sents):
        sent_features = features(sent, Article(title, article_sents))
        # get the probability this is a good summary sentence
        sent.prob_good_summary = \
            summary_classifier.prob_classify(sent_features).prob(True)
        key = sent.cluster_num
        if key in result:
            if sent.prob_good_summary > result[key].prob_good_summary:
                result[key] = sent
        else:
            result[key] = sent

    assert (all(key in result for key in set(clusters)))

    sorted_sents = sorted(result.values(), key = lambda s: s.index_in_text)
    return ''.join([sent.shorten() for sent in sorted_sents])

def main(*args):
    # setup corpus stuff, if it exists
    ARTICLE_TO_SUMMARIZE = 128
    corpus_exists = os.path.exists("resources/wiki-corpus.json")
    if corpus_exists:
        with open("resources/wiki-corpus.json", "r") as f:
            corpus = json.load(f)
        _article = corpus[ARTICLE_TO_SUMMARIZE]['article']
        _title = corpus[ARTICLE_TO_SUMMARIZE]['title']
    else:
        _article = ""
        _title = ""

    _num_sentences = 3
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", "-t",
                         help="The title of the text to be summarized")
    parser.add_argument("--article", "-a",
                         help="The text to be summarized")
    parser.add_argument("--num-sentences", "-n",
                        default=_num_sentences, type=int,
                         help=str("Determines how many sentences should "
                                  "comprise the summary. The default is 3."))
    parser.add_argument("--corpus-article", "-c", type=int,
                         default=ARTICLE_TO_SUMMARIZE,
                         help="Use on one of the over 2000 articles in the corpus.")

    args = parser.parse_args(*args)
    if ((args.title and not args.article) or
        (args.article and not args.title)):
        print ("\nError: if providing --article or --title arguments, both "
               "should be provided. These 2 agruments go together.\n")
        sys.exit(-1)

    if args.article:
        with open(args.article) as f:
            text = '\n'.join(f.readlines())
            args.article = text
    elif args.corpus_article and corpus_exists:
        args.title = corpus[args.corpus_article]['title']
        args.article = corpus[args.corpus_article]['article']

    print "\nTitle: %s\n" % args.title
    print get_summary(args.title, args.article, args.num_sentences,
                      use_semantics=False)

if __name__ == '__main__':
    main(sys.argv[1:])
