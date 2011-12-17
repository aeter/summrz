#Copyright 2011, Adrian Nackov
#Released under BSD licence (3 clause):
#http://www.opensource.org/licenses/bsd-license.php
import unittest
from summarizer.similarity import *

class TestWordSimilarity(unittest.TestCase):
    def test_word_similarity(self):
        dog_cat_similarity = word_similarity('dog', 'cat')
        dog_hog_similarity = word_similarity('dog', 'hog')
        self.assertTrue(dog_cat_similarity > dog_hog_similarity)

        apple_orange_similarity = word_similarity('apple', 'orange')
        apple_lamp_similarity = word_similarity('apple', 'lamp')
        self.assertTrue(apple_orange_similarity > apple_lamp_similarity)

        bad_word_similarity = word_similarity("asdfghj", "cat")
        self.assertEqual(bad_word_similarity, 0)

        bad_word_similarity_2 = word_similarity("cat", "qwzjlkcn")
        self.assertEqual(bad_word_similarity_2, 0)

        # In theory only non-empty words will be provided to the
        # word_similarity function. Yeah, but...
        empty_word_similarity = word_similarity("", "cat")
        self.assertEqual(empty_word_similarity, 0)

class TestBrownCorpus(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
