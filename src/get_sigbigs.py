from os import listdir
from os.path import isfile, join

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import *


in_path = 'data/interim/lemmatized_entities'
txt_files = [f for f in listdir(in_path) if isfile(join(in_path, f))]
tokens = []
for f in txt_files:
    with open(join(in_path, f), 'r') as f:
        txt = f.read().strip().split()
        tokens.extend(txt)


def get_bigrams(tokens):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    trigram_measures = nltk.collocations.TrigramAssocMeasures()

    bigram_finder = BigramCollocationFinder.from_words(tokens)
    bigram_finder.apply_freq_filter(3)
    bigrams = bigram_finder.nbest(bigram_measures.chi_sq, 500)

    trigram_finder = TrigramCollocationFinder.from_words(tokens)
    trigram_finder.apply_freq_filter(3)
    trigrams = trigram_finder.nbest(trigram_measures.chi_sq, 500)

    return bigrams, trigrams


two, three = get_bigrams(tokens)

with open('data/interim/signigicant_bigrams/bigrams.txt', 'w') as f:
    for e in two:
        f.write(' '.join(e) + '\n')


with open('data/interim/signigicant_bigrams/trigrams.txt', 'w') as f:
    for e in three:
        f.write(' '.join(e) + '\n')

