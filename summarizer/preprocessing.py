#Copyright 2011, Adrian Nackov
#Released under BSD licence (3 clause): 
#http://www.opensource.org/licenses/bsd-license.php

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.data import load
import re

WORDS_RE = re.compile("[^A-Za-z]+")
STOP_WORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()
TOKENIZER = load('tokenizers/punkt/english.pickle')
SENTENCE_SHORTENING = 150 #characters

class Sentence(object):
    def __init__(self, sent):
        self._sent = sent # a holder of the original sentence string
        self.sci_data = None # words/lower/stemmed/without stopwords.

    def shorten(self):
        return self._sent[0:SENTENCE_SHORTENING].rstrip(".?!") + "..."

    def words(self):
        # cache the splitting to words:
        if not hasattr(self, "_words"):
            self._words = [w for w in re.split(WORDS_RE, self._sent) if w]
        return self._words

    def stem(self):
        return [STEMMER.stem(w.lower()) for w in self.words()]

    def preprocess(self):
        """
        Returns an instance pointer to self, with the property
        'sci_data' holding the stemmed, lowercase words of the sentence 
        with removed STOP_WORDS.
        """
        self.sci_data = [w for w in self.stem() 
                         if w and w not in STOP_WORDS]
        return self

def sentences(text):
    """
    Splits the text into sentences.
    """
    return [Sentence(s) for s in TOKENIZER.tokenize(text) if s]

def prepare(text):
    """
    Returns the text split into preprocessed Sentence objects.
    """
    return [s.preprocess() for s in sentences(text)]
