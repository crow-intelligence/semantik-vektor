from os import listdir
from os.path import isfile, join

in_path = 'data/interim/lemmatized_entities'
out_path = 'data/interim/sigbig'
txt_files = [f for f in listdir(in_path) if isfile(join(in_path, f))]

with open('data/interim/signigicant_bigrams/bigrams.txt', 'r') as f:
    bigrams = f.read().strip().split('\n')

for txt in txt_files:
    with open(join(in_path, txt), 'r') as f:
        text = f.read()
        for b in bigrams:
            if b in text:
                text = text.replace(b, '|'.join(b))
        with open(join(out_path, txt), 'w') as outfile:
            outfile.write(text)
