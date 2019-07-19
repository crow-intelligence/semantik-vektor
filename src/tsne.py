import pickle

import numpy as np
from sklearn.manifold import TSNE

m = np.load('models/semantik.npy')
vocab = pickle.load(open('models/semantik.p', 'rb'))

X_embedded = TSNE(n_components=2).fit_transform(m)

with open('models/tsne.tsv', 'w') as f:
    h = 'word\tx\ty\n'
    f.write(h)
    for i in range(len(vocab)):
        word = vocab[i]
        x = X_embedded[i][0]
        y = X_embedded[i][1]
        o = word + '\t' + str(x) + '\t' + str(y) + '\n'
        f.write(o)

Y_embedded = TSNE(n_components=3).fit_transform(m)

with open('models/tsne3.tsv', 'w') as f:
    h = 'word\tx\ty\tz\n'
    f.write(h)
    for i in range(len(vocab)):
        word = vocab[i]
        x = Y_embedded[i][0]
        y = Y_embedded[i][1]
        z = Y_embedded[i][2]
        o = word + '\t' + str(x) + '\t' + str(y) + '\t' + str(z) + '\n'
        f.write(o)
