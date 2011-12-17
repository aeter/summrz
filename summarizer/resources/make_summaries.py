#Copyright 2011, Adrian Nackov
#Released under BSD licence (3 clause): 
#http://www.opensource.org/licenses/bsd-license.php

#!/usr/bin/env python
"""
A script for cutting only the article resume, after the
wikipedia XML file has been processed by xml2files.py. It
creates new filenames: <article>__summary.txt
"""

import sys
import os
import re
import urllib2
import json

def walk(_dir):
    for root, dirs, files in os.walk(_dir):
        for _file in files:
            if _file.endswith(".txt"):
                filepath = os.path.join(root, _file)
                make_summary(filepath)

def make_summary(filepath):
    summary_file = "%s__summary.txt" % filepath.split(".txt")[0]
    with open(filepath, 'r') as wiki_article:
        with open(summary_file, 'w') as wiki_summary:
            for line in wiki_article:
                if line.strip().startswith("=="):
                    break
                wiki_summary.write(line)
                
def write_corpus_to_json(articles_dir):
    """
    Traverses the directory containing "<article>__summary", "<article>__text"
    files and creates a corpus in format:
    [{article:"<article_text>", summary:"<summary_text>", title:"<title_text>"
     {article:"<article_text>", summary:"<summary_text>", title:"<title_text>"]
    I'm sorry, I'm encoding it with iso-8859-1 as otherwise it prints errors for    utf encodings.
    """
    corpus = []
    trim = lambda s: re.split("__summary|__text", s)[0]
    titles = set(trim(title) for title in os.listdir(articles_dir))
    for title in titles:
        try:
            with open(os.path.join(articles_dir, title+"__summary"), "r") as f:
                summary = "".join(f.readlines())
            with open(os.path.join(articles_dir, title+"__text"), "r") as f:
                # split by the last 20 characters of the summary
                # TODO - refactor the code here and above
                article = "".join(f.readlines()).split(summary[-20:].strip())[1]
            title = urllib2.unquote(title) # remove URL encoding characters, ugh
            corpus.append({"article":article, "title":title, "summary":summary})
        # yet there are still some messed up articles (about 100 of them)
        except Exception, e:
            continue
    with open("wiki-corpus.json", "w") as corpus_file:
        json.dump(corpus, corpus_file, encoding="iso-8859-1") 

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: %s <articles_dir>" % sys.argv[0]
        sys.exit(-1)

    walk(sys.argv[1])
