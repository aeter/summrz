#Copyright 2011, Adrian Nackov
#Released under BSD licence (3 clause): 
#http://www.opensource.org/licenses/bsd-license.php

from nltk.cluster import KMeansClusterer
from nltk.cluster.util import euclidean_distance

from similarity import sentence_similarity

from numpy import array, set_printoptions

def similarity_matrix(sentences, use_semantics=False):
    """ 
    input: A list of preprocessing.Sentence objects.
    """
    #TODO - profile and if slow, compute only above the main matrix
    # diagonal, and just lookup for values below it.
    return [[sentence_similarity(sentences[i].words(),
                                 sentences[j].words(),
                                 use_semantics=use_semantics)
            for i in range(len(sentences))]
            for j in range(len(sentences))]

def cluster(k, matrix):
    """
    Returns a list of numbers - e.g., for k=3 and 4 sentences, the return value
    may be something like [1, 2, 2, 0]
    """
    set_printoptions(threshold=10)
    nvectors = array([array(s) for s in matrix])
    # dummy initial means - usually they will be as far from each other as possible.
    # In this case though, they are just the coordinates for the first k sentences.
    initial_means = [nvectors[_] for _ in range(k)]
    clusterer = KMeansClusterer(k, euclidean_distance, initial_means=initial_means)
    clusters = clusterer.cluster(nvectors, True)
    return clusters
