import os
from skimage import io
import numpy as np
from brancher import *

# Takes a LaTeX string and indicator label, compiles png and returns indicator.
def jpg(symbol, n_samples, clear=False):
    # optionally, remove earlier images and their labels
    if clear:
        os.system("rm images2/*")
        os.system("rm labels2/labels2.csv")
    # list of n.png images sorted by number n
    images = sorted(os.listdir("images2")[1:], key=lambda x: int(x[:-4]))

    if images != []:
        start = int(images[-1][:-4]) + 1
    else:
        start = 0

    # appends images, starting with (n+1).png if n.png already exists
    for i in xrange(start, start + n_samples):
        content,indic = tex_poly(symbol, 2)

        with open('expression.tex','w') as f:
            f.write(content)

        os.system("latex expression scriptname >/dev/null")
        os.system("dvipng -D 200 expression -T 16cm,5cm -o \
                  images2/{}.png >/dev/null".format(i))

        # appends labels to the .csv file
        with open('labels2/labels2.csv', 'a') as f:
            np.savetxt(f, indic.reshape(1, indic.shape[0]))


# assuming images and labels exist, returns train and test data as arrays
# optionally can take bounds as ((h1,h2),(w1,w2)) to zoom in on the images
def get_data(bounds=False, limit=None, conv=True, jitter=False):

    # obtains list of images in images directory
    images = sorted(os.listdir("images")[1:], key=lambda x: int(x[:-4]))
    if limit:
        images = images[limit[0]:limit[1]]

    # makes arrays representing these images and their labels
    y = np.loadtxt("labels/labels.csv")[limit[0]:limit[1]]


    sample_size = len(images)
    X = np.zeros((sample_size,393,1259)).astype('uint8')
    for i in xrange(len(images)):
        X[i] = io.imread('images/' + images[i])

    # manually specify pixels to subset image
    if bounds:
        X = X[:, bounds[0][0]:bounds[0][1], bounds[1][0]:bounds[1][1]]

    # given some more room to zoom in on, zooms in on a random place for each
    # image, having the effect of moving the symbols around
    if jitter:
        r = np.random.randint(-jitter, jitter, size=(sample_size, 2))
        height = X.shape[2] - 2*jitter
        width = X.shape[1] - 2*jitter
        temp = np.zeros((sample_size, height, width))
        for i in xrange(sample_size):
            temp[i] = X[i, jitter + r[i,0]:height + jitter + r[i,0],
                           jitter + r[i,1]:width + jitter + r[i,1]]
        X = temp

    # splits 80/20 into train and test sets, returning these
    split = int(y.shape[0] * .8)
    X_train, y_train, X_test, y_test = X[:split], y[:split], X[split:], y[split:]

    # make dimensions appropriate for CNNs
    if conv:
        X_train, X_test = X_train[:,:,:,np.newaxis], X_test[:,:,:,np.newaxis]

    return X_train, y_train, X_test, y_test


# removes all whitespace above, below, left, or right of text
def trim_whitespace(a):
    temp = 255 - a
    rows = np.sum(temp, axis=0)
    left, right = np.argwhere(rows).min(), np.argwhere(rows).max()

    cols = np.sum(temp, axis=1)
    top, bot = np.argwhere(cols).min(), np.argwhere(cols).max()

    a = a[top:bot+1, left:right+1]
    return a

# given an array image, segments it into characters by empty vertical space
# returns a list of arrays representing the image segments
def segment(a, threshold=50):
    densities = np.sum(255 - a, axis=0)
    blanks = list(np.argwhere(densities<threshold).flatten())
    gaps = partition(blanks)
    for g in gaps:
        m = 255*a.shape[0]
        for i in g:
            if i < m:
                m = i
        g = m

    segs = [a[:,:gaps[0]]]
    segs += [a[:,gaps[i-1]:gaps[i]] for i in range(1, len(gaps))]
    segs += [a[:,gaps[-1]:]]
    return segs

# given a sorted list, returns a partition of lists with consecutive numbers
def partition(l):
    p = [0]
    for i in xrange(1, len(l)):
        if l[i] != l[i-1] + 1:
            p.append(i)
    p.append(len(l))
    return [l[p[i]:p[i+1]] for i in xrange(len(p) - 1)]


def predict_word(model, a):
    segs = segment(trim_whitespace(a[:,:,0]))
    for arr in segs:
        temp = np.full((40,40), 255, dtype='uint8')
        temp[:arr.shape[0],arr.shape[1]] = arr
        arr = temp

    chars = []
    for arr in segs:
        chars.append(symbols[model.predict_classes(arr, batch_size=32, verbose=1)])
    return " ".join(chars)

    # np.sum(a, axis=1)
    # top = -1
    # for i in xrange(a.shape[0]):
    #     if np.sum(a[i]) == 0:
    #         top = i
    #     else:
    #         break
    # if top >= 0:
    #     a = a[top+1:]
    #
    # bot = -1
    # for i in range(a.shape[0])[::-1]:
    #     if np.sum(a[i]) == 0:
    #         bot = i
    #     else:
    #         break
    # if bot >= 0:
    #     a = a[:bot]
    #
    # left = -1
    # for i in xrange(a.shape[1]):
    #     if np.sum(a[:,i]) == 0:
    #         left = i
    #     else:
    #         break
    # if top >= 0:
    #     a = a[top+1:]





# def resize(a, dim):
#     height = dim[0]
#     width = dim[1]
#
#     h_factor = a.shape[0] / height + 1
#     w_factor = a.shape[1] / width + 1
