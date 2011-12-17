#Copyright 2011, Adrian Nackov
#Released under BSD licence (3 clause): 
#http://www.opensource.org/licenses/bsd-license.php
import unittest
from summarizer.preprocessing import Sentence, sentences, prepare

EMPTY_SENTENCE = ""
BASIC_SENTENCE = "This is it."
ODD_SENTENCE = "This, my* friend, is _the_ end - I &^(+=%>$)%#!@ mean that!"
DASH_SENTENCE = "Non-working code is not fun..."

# There should be correct sentences, i.e. with spaces separating them, 
# with correct punctuation, etc.
SOME_TEXT = str("The quick brown fox jumps over the lazy dog. "
                "And it does again? "
                "And a third sentence...")

class TestSentence(unittest.TestCase):

    def test_words(self):
        s1 = Sentence(BASIC_SENTENCE)
        self.assertEqual(s1.words(), ["This", "is", "it"])
        self.assertTrue(hasattr(s1, "_words"))

        s2 = Sentence(EMPTY_SENTENCE)
        self.assertEqual(s2.words(), [])
        self.assertTrue(hasattr(s2, "_words"))

        s3 = Sentence(ODD_SENTENCE)
        # Underscored words are "stripped" of underscores...
        self.assertEqual(s3.words(), 
                         ['This', 'my', 'friend', 'is', 'the',
                          'end', 'I', 'mean', 'that'])
        self.assertTrue(hasattr(s3, "_words"))

        s4 = Sentence(DASH_SENTENCE)
        self.assertEqual(s4.words(),
                ["Non", "working", "code", "is", "not", "fun"])

    def test_stem(self):
        s1 = Sentence(BASIC_SENTENCE)
        stemmed1 = s1.stem()
        self.assertEqual(stemmed1, ['thi', 'is', 'it'])
        self.assertTrue(hasattr(s1, "_words"))

        s2 = Sentence(EMPTY_SENTENCE)
        stemmed2 = s2.stem()
        self.assertEqual(stemmed2, [])
        self.assertTrue(hasattr(s2, "_words"))

        s3 = Sentence(ODD_SENTENCE)
        stemmed3 = s3.stem()
        self.assertEqual(stemmed3, 
                        ['thi', 'my', 'friend', 'is', 'the', 'end',
                         'i', 'mean', 'that'])
        self.assertTrue(hasattr(s3, "_words"))

        s4 = Sentence(DASH_SENTENCE)
        stemmed4 = s4.stem()
        self.assertEqual(stemmed4, ['non', 'work', 'code', 'is', 'not', 'fun'])
        self.assertTrue(hasattr(s4, "_words"))

    def test_preprocess(self):
        s1 = Sentence(BASIC_SENTENCE).preprocess()
        self.assertEqual(s1.sci_data, ['thi'])
        self.assertTrue(hasattr(s1, "_words"))

        s2 = Sentence(EMPTY_SENTENCE).preprocess()
        self.assertEqual(s2.sci_data, [])
        self.assertTrue(hasattr(s2, "_words"))

        s3 = Sentence(ODD_SENTENCE).preprocess()
        self.assertEqual(s3.sci_data, ['thi', 'friend', 'end', 'mean'])
        self.assertTrue(hasattr(s3, "_words"))

        s4 = Sentence(DASH_SENTENCE).preprocess()
        self.assertEqual(s4.sci_data, ['non', 'work', 'code', 'fun'])
        self.assertTrue(hasattr(s4, "_words"))

class TestPreprocessingFunctions(unittest.TestCase):

    def test_sentences(self):
        sents1 = sentences(EMPTY_SENTENCE)
        self.assertEqual(sents1, [])

        sents2 = sentences(SOME_TEXT)
        self.assertEqual(sents2[0]._sent,
                "The quick brown fox jumps over the lazy dog.")
        self.assertEqual(sents2[0].sci_data, None)
        self.assertEqual(sents2[1]._sent,
                "And it does again?")
        self.assertEqual(sents2[1].sci_data, None)
        self.assertEqual(sents2[2]._sent,
                "And a third sentence...")
        self.assertEqual(sents2[2].sci_data, None)

    def test_prepare(self):
        sents1 = prepare(EMPTY_SENTENCE)
        self.assertEqual(sents1, [])

        sents2 = prepare(SOME_TEXT)
        self.assertEqual(len(sents2), 3)
        self.assertFalse(sents2[0].sci_data is None)
        self.assertFalse(sents2[1].sci_data is None)
        self.assertFalse(sents2[2].sci_data is None)

if __name__ == '__main__':
    unittest.main()
