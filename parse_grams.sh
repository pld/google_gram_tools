#!/bin/sh

if [ ! -n "$1" ]
then
  echo "Usage: `basename $0` n-gram-number"
  exit 65
fi

cd google_$1grams

CSV_DIR="csv_files"
mkdir -p $CSV_DIR
unzip \*.zip -d $CSV_DIR
cd $CSV_DIR

FOLDER="../../google_$1grams_parsed"
mkdir -p $FOLDER

for f in *
do
  echo $f
  cat $f | awk -f ../../parse_grams.awk > $FOLDER/$f
done

