import itertools
from os import listdir
from os.path import isfile, join

import nltk

in_path = 'data/raw/ml'
ner_path = 'data/raw/ner'
out_path = 'data/interim/lemmatized_entities'
txts = [f for f in listdir(in_path) if isfile(join(in_path, f))]
ners = [f for f in listdir(ner_path) if isfile(join(ner_path, f))]

patterns = r"""
KT: {<I-ORG>+}
{<I-MISC>+}
{<I-LOC>+}
{<I-PER>+}
"""
person_pattern = r"""KT: {<I-PER>+}"""
location_patterns = r"""KT: {<I-LOC>+}"""
organization_pattern = r"""KT: {<I-ORG>+}"""
misc_pattern = r"""KT: {<I-MISC>+}"""

for txt in txts:
    fname = txt[:-3] + 'out'
    outname = txt[:-3] + '.txt'
    wd_lemma = {}
    with open(join(in_path, txt), 'r') as f:
        text = []
        for l in f:
            l = l.strip().split('\t')
            if len(l) == 4:
                wd, lemma, _, _ = l
                wd_lemma[wd.lower()] = lemma.lower()
                if lemma.isalnum():
                    text.append(lemma.lower())
        text = ' '.join(text)

    ner_tags = []
    tags = []
    with open(join(ner_path, fname), 'r') as ner_file:
        for l in ner_file:
            l = l.strip().split('\t')
            if len(l) == 2:
                wd, tag = l
                tags.append(tag)
                ner_tags.append((wd.lower(), tag))

    def get_lemma(wd):
        if wd in wd_lemma:
            return wd_lemma[wd.lower()]
        else:
            return wd.lower()

    def lemmatize_ner(ner):
        try:
            name = ner.split(' ')
            name = [wd.lower() for wd in name]
            if len(name) == 1:
                return get_lemma(name[0])
            else:
                stemmed_ner = name[:-1]
                inflected = name[-1]
                laststem = get_lemma(inflected)
                stemmed_ner.append(laststem)
                return ' '.join(stemmed_ner)
        except:
            return None

    chunker = nltk.chunk.regexp.RegexpParser(patterns)
    chunks = nltk.chunk.tree2conlltags(chunker.parse(ner_tags))
    all_ners = [' '.join(word.lower() for word, tag, chunk in group).lower()
                for key, group in itertools.groupby(chunks,
                                                    lambda l:
                                                    l[1] != 'O') if key]

    person_chunker = nltk.chunk.regexp.RegexpParser(person_pattern)
    person_chunks = nltk.chunk.tree2conlltags(person_chunker.parse(ner_tags))
    persons = [' '.join(word for word, tag, chunk in group)
               for key, group in itertools.groupby(person_chunks,
                                                   lambda l:
                                                   l[1] == 'I-PER') if key]
    persons = [lemmatize_ner(ner) for ner in persons
               if isinstance(lemmatize_ner(ner), str)]

    location_chunker = nltk.chunk.regexp.RegexpParser(location_patterns)
    location_chunks = nltk.chunk.tree2conlltags(location_chunker.parse(ner_tags))
    locations = [' '.join(word for word, tag, chunk in group)
                 for key, group in itertools.groupby(location_chunks,
                                                     lambda l:
                                                     l[1] == 'I-LOC') if key]
    locations = [lemmatize_ner(ner) for ner in locations]


    organization_chunker = nltk.chunk.regexp.RegexpParser(organization_pattern)
    organization_chunks = nltk.chunk.tree2conlltags(organization_chunker.parse(ner_tags))
    organizations = [' '.join(word for word, tag, chunk in group)
                     for key, group in itertools.groupby(organization_chunks,
                                                         lambda l:
                                                         l[1] == 'I-ORG')
                     if key]
    organizations = [lemmatize_ner(ner) for ner in organizations]

    misc_chunker = nltk.chunk.regexp.RegexpParser(misc_pattern)
    misc_chunks = nltk.chunk.tree2conlltags(misc_chunker.parse(ner_tags))
    miscs = [' '.join(word for word, tag, chunk in group)
             for key, group in itertools.groupby(misc_chunks,
                                                 lambda l:
                                                 l[1] == 'I-MISC') if key]
    miscs = [lemmatize_ner(ner) for ner in miscs]


    all_ners = [e.lower() for e in all_ners if ' ' in e]
    all_ners = [e.split() for e in all_ners]
    all_ners = [' '.join([get_lemma(wd) for wd in phrase]) for phrase in all_ners]

    for ner in all_ners:
        if ner in text:
            text = text.replace(ner, '|'.join(ner.split()))
    with open(join(out_path, outname), 'w') as outfile:
        outfile.write(text)
    ner_opath = 'data/interim/ners'
    with open(join(ner_opath, fname[:-4] + '_persons.txt'), 'w') as f:
        if len(persons) > 0:
            f.write('\n'.join(persons))
    with open(join(ner_opath, fname[:-4] + '_organizations.txt'), 'w') as f:
        if len(organizations) > 0:
            f.write('\n'.join(organizations))
    with open(join(ner_opath, fname[:-4] + '_locations.txt'), 'w') as f:
        if len(locations) > 0:
            f.write('\n'.join(locations))
    with open(join(ner_opath, fname[:-4] + '_miscs.txt'), 'w') as f:
        if len(miscs) > 0:
            f.write('\n'.join(miscs))
