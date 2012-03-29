#!/usr/bin/python

from collections import defaultdict
import os
import pickle
import pprint

def dd():
    return defaultdict(dict)

n_to_dir = {
  1: "google_1grams_parsed",
  2: "google_2grams_parsed",
}

def parse(pickle_file, case_insensitive=True):
    # directory with parsed gram files
    grams_to_years_to_counts = defaultdict(dd)
    n_to_year_to_total = defaultdict(dd)
    for n, _dir in n_to_dir.items():
        for file in os.listdir(_dir):
            print("processing file %s...", file)
            with open(_dir + "/" + file) as f:
                for l in f:
                    t, year, occurences, pages, books = [
                        x.strip() for x in l.split("\t")
                    ]
                    occurences, pages, books = [
                        int(x) for x in [occurences, pages, books]
                    ]
                    # make case insensitive?
                    if case_insensitive:
                        t = t.lower()
                    if grams_to_years_to_counts[t][year]:
                        grams_to_years_to_counts[t][year][0] += occurences
                        grams_to_years_to_counts[t][year][1] += pages
                        grams_to_years_to_counts[t][year][2] += books
                    else:
                        grams_to_years_to_counts[t][year] = [occurences, pages,
                              books]
                    if n_to_year_to_total[n][year]:
                        n_to_year_to_total[n][year][0] += occurences
                        n_to_year_to_total[n][year][1] += pages
                        n_to_year_to_total[n][year][2] += books
                    else:
                        n_to_year_to_total[n][year] = [occurences, pages,
                              books]
    res = [grams_to_years_to_counts, n_to_year_to_total]
    with open(pickle_file, "wb") as f:
        pickle.dump(res, f)
    return res

# load from a pickle cache?
cached = True
pickle_file = "grams.pkl"

if cached:
    with open(pickle_file, "rb") as f:
        res = pickle.load(f)
else:
    res = parse(pickle_file)

grams_to_years_to_counts, n_to_year_to_total = res

phrase_groups = {
    "Black/Negro ghetto(s)": [
        "negro ghetto",
        "negro ghettos",
        "black ghetto",
        "black ghettos"
    ],
#    "Nazi ghetto(s)": [
#        "Nazi ghetto",
#        "Nazi ghettos",
#    ],
    "Warsaw ghetto(s)": [
      "Warsaw ghetto",
      "Warsaw ghettos",
    ],
#    "Ghetto(s)": [
#      "ghetto",
#      "ghettos",
#    ],
}

def csv(start_year, end_year, percents=False):
    # output as CSV
    output = "phrase_counts.csv"
    with open(output, "w") as f:
        for name, phrases in phrase_groups.items():
            for year in range(start_year, end_year):
                tcounts = [0, 0, 0]
                year = str(year)
                for phrase in phrases:
                    years_to_counts = grams_to_years_to_counts[phrase.lower()]
                    counts = years_to_counts[year]
                    if counts:
                        tcounts = map(sum, zip(tcounts, counts))
                if percents:
                  n = n_to_year_to_total[len(name.split(' '))][year]
                  tcounts = [x / float(n[i]) for i, x in enumerate(tcounts)]
                f.write("%s,%s,%f,%f,%f\n" % tuple([name, year] + tcounts))

csv(1900, 2008, False)
