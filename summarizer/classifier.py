#Copyright 2011, Adrian Nackov
#Released under BSD licence (3 clause):
#http://www.opensource.org/licenses/bsd-license.php

from preprocessing import prepare, Sentence
from nltk.util import bigrams
from nltk.corpus import gutenberg
import random
import re

class Article(object):

    def __init__(self, title, text):
        _title = title.replace("_", " ")
        self.title = Sentence(_title).preprocess() #stem, lowercase, stop-words
        self.text = text

    def get_unigrams(self):
        """
        For caching the retrieval of article unigrams
        """
        if not hasattr(self, "_unigrams"):
            # join the unigrams from all sentences:
            self._unigrams = flatten([s.sci_data for s in self.text])
        return self._unigrams

    def get_bigrams(self):
        """
        For caching the retrieval of article bigrams
        """
        if not getattr(self, "_bigrams", []):
            self._bigrams = bigrams(self.get_unigrams())
        return self._bigrams

def features(sentence, article):
    """
    input:
        sentence: a Sentence object from the article's summary
        article: an Article object
        _features: a dictionary object for deciding which features to use
    """

    _features = {}

    #-----------------------------------------------------------
    # number of stemmed unigrams in the sentence to be seen in the title:
    _features["uni_title"] = len(
            [u for u in sentence.sci_data if u in article.title.sci_data])

    #-----------------------------------------------------------
    # number of stemmed bigrams in the sentence occuring in text
    _features["bi_text"] = len([b for b in bigrams(sentence.sci_data)
                                if b in article.get_bigrams()])

    #-----------------------------------------------------------
    # number of stemmed unigrams in the sentence occuring in text
    _features["uni_text"] = len(
        set(sentence.sci_data).union(set(article.get_unigrams())))

    #-----------------------------------------------------------
    # sentence length
    _features["sent_length"] = len(sentence.words())

    #----------------------------------------------------------
    # presence of uppercase words
    _features["uppercased"] = len([w for w in sentence.words()
                                   if w == w.upper()])
    return _features

def featuresets(corpus):
    """
    corpus must have a format of:
    [{"article":article,"summary":summary,"title":title},
     {"article":article,"summary":summary,"title":title},]

    returns the featuresets ready for training a classifier
    """
    featuresets = []
    gutenberg_sents = gutenberg.sents()

    for item in corpus:
        article = prepare(item["article"])
        summary = prepare(item["summary"])

        # define good summary sentencefe
        for sentence in summary:
            sent_features = features(sentence, Article(item["title"], article))
            featuresets.append((sent_features, True))

        # define bad summary sentences
        # Take 2 random sentences from the gutenberg corpus. They just can't be
        # good summary sentences for this article. They represent a rubbish
        # summary for this article. The number is kept low for performance
        # reasons.
        bad_summary = random.sample(gutenberg_sents, 2)
        bad_summary_sents = prepare(" ".join(flatten(bad_summary)))
        for sentence in bad_summary_sents:
            sent_features = features(sentence, Article(item["title"], article))
            featuresets.append((sent_features, False))
    return featuresets

def train(featuresets):
    """
    input: a list of tuples - featuresets
    returns: a trained on the featuresets classifier
    """
    import nltk
    classifier = nltk.NaiveBayesClassifier.train(featuresets)
    return classifier

def flatten(list_of_lists):
    """A helper function"""
    return sum(list_of_lists, [])

def get_titles_words(corpus):
    # By the preprocessing, the titles have "_" instead of
    # spaces between their words.
    titles = [item["title"].split("_") for item in corpus]
    return set(flatten(titles))

if __name__ == '__main__':
    import json
    with open("wiki-corpus.json") as f:
        CORPUS = json.load(f)
