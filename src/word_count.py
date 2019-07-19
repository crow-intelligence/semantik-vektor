import operator
from collections import Counter
from os import listdir
from os.path import isfile, join

out_path = 'data/processed'
in_path = 'data/interim/sigbig'
txt_files = [f for f in listdir(in_path) if isfile(join(in_path, f))]

words = []
for txt in txt_files:
    with open(join(in_path, txt), 'r') as f:
        text = f.read().strip().split()
        words.extend(text)

words = Counter(words)
sorted_wds = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
with open('data/interim/word_frequency.tsv', 'w') as f:
    for e in sorted_wds:
        wd, freq = e[0], str(e[1])
        o = wd + '\t' + freq + '\n'
        f.write(o)

