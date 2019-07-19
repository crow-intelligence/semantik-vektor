import operator
from collections import Counter
from os import listdir
from os.path import isfile, join

vocab = []
with open('data/interim/word_frequency.tsv', 'r') as f:
    for l in f:
        wd, freq = l.strip().split('\t')
        if int(freq) > 10:
            vocab.append(wd)


out_path = 'data/processed'
in_path = 'data/interim/sigbig'
txt_files = [f for f in listdir(in_path) if isfile(join(in_path, f))]

for txt in txt_files:
    with open(join(in_path, txt), 'r') as f, open(join(out_path, txt), 'w') as outfile:
        text = f.read().strip().split()
        common_wds = set(vocab).intersection(set(text))
        text = [wd for wd in text if wd in common_wds]
        text = ' '.join(text)
        outfile.write(text)

