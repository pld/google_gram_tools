#!/usr/bin/python

from collections import defaultdict
import os
import pickle
import pprint

def dd():
    return defaultdict(dict)

def parse(pickle_file):
    # directory with parsed gram files
    dirs = ["google_2grams_parsed"]
    grams_to_years_to_counts = defaultdict(dd)
    total_num_grams = 0
    for _dir in dirs:
        for file in os.listdir(_dir):
            print("processing file %s...", file)
            with open(_dir + "/" + file) as f:
                for l in f:
                    total_num_grams += 1
                    t, year, occurences, pages, books = [
                        x.strip() for x in l.split("\t")
                    ]
                    occurences, pages, books = [
                        int(x) for x in [occurences, pages, books]
                    ]
                    t = t.lower()
                    if grams_to_years_to_counts[t][year]:
                        grams_to_years_to_counts[t][year][0] += occurences
                        grams_to_years_to_counts[t][year][1] += pages
                        grams_to_years_to_counts[t][year][2] += books
                    else:
                        grams_to_years_to_counts[t][year] = [occurences, pages,
                            books]
    res = [grams_to_years_to_counts, float(total_num_grams)]
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

grams_to_years_to_counts, total_num_grams = res

pp = pprint.PrettyPrinter()
pp = pp.pprint

phrase_groups = {
    "Black/Negro ghetto(s)": [
        "negro ghetto",
        "negro ghettos",
        "black ghetto",
        "black ghettos"
    ],
    "Nazi ghetto(s)": [
        "Nazi ghetto",
        "Nazi ghettos",
    ]
}

def csv(start_year, end_year, percents=False):
    # output as CSV
    output = "phrase_counts.csv"
    with open(output, "w") as f:
        for name, phrases in phrase_groups.items():
            for key in range(start_year, end_year):
                tcounts = [0, 0, 0]
                for phrase in phrases:
                    years_to_counts = grams_to_years_to_counts[phrase.lower()]
                    counts = years_to_counts[str(key)]
                    if counts:
                        tcounts = map(sum, zip(tcounts, counts))
                if percents:
                  tcounts = [x/total_num_grams for x in tcounts]
                f.write("%s,%s,%f,%f,%f\n" % tuple([name, key] + tcounts))

csv(1900, 2008, True)
