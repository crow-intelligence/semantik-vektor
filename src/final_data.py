with open('data/etc/PrecoSenti/PrecoNeg.txt', 'r') as f:
    neg = f.read().strip().split('\n')

with open('data/etc/PrecoSenti/PrecoPos.txt', 'r') as f:
    pos = f.read().strip().split('\n')

with open('models/tsne3.tsv', 'r') as f, open('models/final.tsv', 'w') as of:
    h = 'word\tsentiment\tx\ty\tz\n'
    of.write(h)
    for l in f:
        l = l.strip().split('\t')
        wd = l[0]
        category = 'neutral'
        if wd in neg:
            category = 'negative'
        if wd in pos:
            category = 'positive'
        o = wd + '\t' + category + '\t' + '\t'.join(l[1:]) + '\n'
        of.write(o)
