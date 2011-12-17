#Copyright 2011, Adrian Nackov
#Released under BSD licence (3 clause): 
#http://www.opensource.org/licenses/bsd-license.php

import unittest
from summarizer.clustering import similarity_matrix, cluster
from summarizer.preprocessing import prepare

SENTS1 = prepare(str("The first sentence. "
                     "The second sentence. "
                     "This is a different dog. "
                     "The fifth sentence. "))
SENTS2 = prepare(str("A sentence I like. "
                     "A sentence I dislike. "
                     "A sentence I will delete. "
                     "Fourth one for separating groups, also some more words added. "
                     "The last one to go, but a bit longer now. "))

class TestClustering(unittest.TestCase):
 
    def test_cluster_groups(self):
        matrix = similarity_matrix(SENTS1)
        clusters = cluster(2, matrix)
        self.assertTrue(clusters[0] == clusters[1] == clusters[3])

        matrix2 = similarity_matrix(SENTS2)
        clusters2 = cluster(3, matrix2)
        self.assertTrue(clusters2[0] == clusters2[1] == clusters2[2])
           
if __name__=='__main__':
    unittest.main()
