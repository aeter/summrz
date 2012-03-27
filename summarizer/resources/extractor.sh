#!/bin/bash
ROOT=/home/anackov/Desktop/wikipedia2text/articles/out
PROGRAM=/home/anackov/Desktop/wikipedia2text/wikiextract.py
for _dir in `ls $ROOT`
  do
    echo "In dir: $ROOT/$_dir"
    for _filedir in `ls $ROOT/$_dir`
    do
      _file=`ls $ROOT/$_dir/$_filedir | grep -v .xml`
      $PROGRAM $ROOT/$_dir/$_filedir $ROOT/$_dir/$_filedir/$_file"__text"
    done
    echo "Sleeping for 10"
    sleep 10
 done
