#Copyright 2011, Adrian Nackov
#Released under BSD licence (3 clause):
#http://www.opensource.org/licenses/bsd-license.php

CORPUS = "resources/wiki-corpus.json"
TEST_ARTICLES_TITLES = [
    "Zion National Park",
    "Wonder Stories",
    "Tropic Thunder",
    "Buckingham Palace",
    "Under the Bridge",
]

from nltk.util import ngrams

def rouge(n, auto_summary_words, original_summary_words):
    auto_summary_ngrams = ngrams(auto_summary_words, n)
    original_summary_ngrams = ngrams(original_summary_words, n)
    denominator = len(original_summary_ngrams)
    numerator = len([_ for _ in auto_summary_ngrams
                     if _ in original_summary_ngrams])
    return float(numerator) / float(denominator)

def get_article_info(corpus, article_title):
    """
    Gets the article info from the JSON corpus.

    throws:
       KeyError on missing article

    input:
        corpus: (list of dicts)
            the json loaded corpus of Wikipedia articles

        article_title: (string)
            the title, such as "Zion National Park"

    output:
        a tuple of strings
    """
    # in the json corpus, the titles use underscores
    corpus_title = "_".join(article_title.split())
    data = [x for x in corpus if x['title'] == corpus_title][0]
    # This gives the full Wikipedia article, including the first
    # paragraph
    article = data['summary'] + data['article']
    # This actually is the first paragraph - the example summary
    example_summary = data['summary']
    return article, example_summary, article_title

if __name__ == '__main__':
    import json
    from main import get_summary
    with open(CORPUS, "r") as f:
        corpus = json.load(f)
    article_infos = [get_article_info(corpus, t) for t in TEST_ARTICLES_TITLES]
    print "Getting summaries; this may take a few (5+) minutes)..."
    summaries = [
      (get_summary(title, article, use_clusters=True, shortened_sents=False),
       get_summary(title, article, use_clusters=False, shortened_sents=False))
      for (article, _, title) in article_infos
    ]
    assert len(summaries) == len(article_infos)
    print "Preparing evaluation..."
    for (i, (article, example_summary, title)) in enumerate(article_infos):
        clusters_summary, no_clusters_summary = summaries[i]
        print "Title: %s" % title
        print "Rouge 1 without clusters: %f" % rouge(
            1, no_clusters_summary.split(), example_summary.split())
        print "Rouge 1 with clusters: %f" % rouge(
            1, clusters_summary.split(), example_summary.split())
        print "Rouge 2 without clusters: %f" % rouge(
            2, no_clusters_summary.split(), example_summary.split())
        print "Rouge 2 with clusters: %f" % rouge(
            2, clusters_summary.split(), example_summary.split())
        print "Summary without clusters: %s" % no_clusters_summary
        print "Summary with clusters: %s" % clusters_summary


