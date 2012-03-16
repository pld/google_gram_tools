## google gram tools

1.  Download the ngram sets you want
    $ ngrams_downloader

2.  Parse the terms you are interested in
    [modify parse_grams.awk]
    $ parse_rgams.sh

3.  Generate phrase counts for the term groups you are interested in
    [modify process.py]
    $ python process.py

4.  Graph it
    $ R < plot_ngrams.R --no-save
