#!/bin/bash

if [ ! -n "$1" ] && [ ! -n "$2" ]
then
  echo "Usage: `basename $0` n-gram-number max-file-number"
  exit 65
fi

FOLDER="google_$1grams"
mkdir -p $FOLDER

for i in $(seq 0 $2)
do
  wget -P $FOLDER http://commondatastorage.googleapis.com/books/ngrams/books/googlebooks-eng-all-$1gram-20090715-$i.csv.zip
done
