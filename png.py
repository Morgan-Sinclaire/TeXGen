import os
from skimage import io
import numpy as np
from brancher import *

# Takes a LaTeX string and indicator label, compiles png and returns indicator.
def png(symbol, n_samples, clear=False):
    # optionally, remove earlier images and their labels
    if clear:
        os.system("rm imagesn/*")
        os.system("rm labelsn/labelsn.csv")
    # list of n.png images sorted by number n
    images = sorted(os.listdir("imagesn")[1:], key=lambda x: int(x[:-4]))

    if images != []:
        start = int(images[-1][:-4]) + 1
    else:
        start = 0

    # appends images, starting with (n+1).png if n.png already exists
    for i in xrange(start, start + n_samples):
        content,indic = tex_poly(symbol)

        with open('expression.tex','w') as f:
            f.write(content)

        os.system("latex expression scriptname >/dev/null")
        os.system("dvipng -D 200 expression -T 16cm,5cm -o \
                  imagesn/{}.png >/dev/null".format(i))

        # appends labels to the .csv file
        with open('labelsn/labelsn.csv', 'a') as f:
            np.savetxt(f, indic.reshape(1, indic.shape[0]))


# assuming images and labels exist, returns train and test data as arrays
# optionally can take bounds as ((h1,h2),(w1,w2)) to zoom in on the images
def get_data(bounds=False, limit=None, conv=True, jitter=False):

    # obtains list of images in images directory
    images = sorted(os.listdir("imagesn")[1:], key=lambda x: int(x[:-4]))
    if limit:
        images = images[limit[0]:limit[1]]

    # makes arrays representing these images and their labels
    # note: uint is important, since these are images
    y = np.loadtxt("labelsn/labelsn.csv")[limit[0]:limit[1]].astype('int8')

    sample_size = len(images)
    X = np.zeros((sample_size,393,1259)).astype('uint8')
    for i in xrange(len(images)):
        X[i] = io.imread('imagesn/' + images[i])

    # manually specify pixels to subset image
    if bounds:
        X = X[:, bounds[0][0]:bounds[0][1], bounds[1][0]:bounds[1][1]]

    # given some more room to zoom in on, zooms in on a random place for each
    # image, having the effect of moving the symbols around
    if jitter:
        r = np.random.randint(-jitter, jitter, size=(sample_size, 2))
        height = X.shape[1] - 2*jitter
        width = X.shape[2] - 2*jitter
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

# given 2D-array image, segments it into characters by empty vertical space
# returns a list of arrays representing the image segments
def segment(a, threshold=0):
    # find indices of vertical strips where pixels are entirely white,
    # or within threshold
    densities = np.sum(255 - a, axis=0)
    blanks = list(np.argwhere(densities[5:-5]<=threshold).flatten()+5)
    gaps = partition(blanks)
    for i in xrange(len(gaps)):
        m = 255*a.shape[0]
        for g in gaps[i]:
            if g < m:
                m = g
        gaps[i] = m

    # returns list of arrays representing the segments for each character
    segs = [a[:,:gaps[0]]]
    segs += [a[:,gaps[i-1]:gaps[i]] for i in range(1, len(gaps))]
    segs += [a[:,gaps[-1]:]]

    # puts each character in the middle of a 40x40 box
    # note: uint is important, since these are images
    for i in range(len(segs)):
        temp = np.full((40,40), 255, dtype='uint8')
        space = (40 - segs[i].shape[0], 40 - segs[i].shape[1])
        if space[0] >= 0 and space[1] >= 0:
            temp[space[0]/2:space[0]/2 + segs[i].shape[0],
                 space[1]/2:space[1]/2 + segs[i].shape[1]] = segs[i]
        else:
            segs[i] = segs[i][:40,:40]
        segs[i] = temp[:,:,np.newaxis]

    segs = np.array(segs)
    return segs

# given a sorted list, returns a partition of lists with consecutive numbers
def partition(l):
    p = [0]
    for i in xrange(1, len(l)):
        if l[i] != l[i-1] + 1:
            p.append(i)
    p.append(len(l))
    return [l[p[i]:p[i+1]] for i in xrange(len(p) - 1)]


def predict_char(model, char):
    pass

# takes a 3D image with multiple letters, returns which letters are in the image
def predict_word(model, a):
    # get character segments to feed into character-reading model
    segs = segment(trim_whitespace(a[:,:,0]))

    # has the model make predictions for each character image
    chars = []
    ind = model.predict_classes(segs, verbose=0)
    chars = [symbols[i] for i in ind]
    return " ".join(chars)

def score_words(model, X_test, y_test, n=None):
    if not n:
        n = X_test.shape[0]

    num_correct = 0

    for i in xrange(n):
        pred = predict_word(model, X_test[i])
        indic = y_test[i]
        label = ' '.join([symbols[j] for j in indic[np.argwhere(indic>=0)].flatten()])
        if pred == label:
            num_correct += 1
        # if np.argwhere(indic>=0).shape[0] == 10 and pred == label:
        #     print i
        if np.argwhere(indic>=0).shape[0] - len(pred.split()) >= 2:
            print i

    print "Accuracy: {}% on {} examples.".format(100. * num_correct / n, n)
#
#     return a
# def resize(a, dim):
#     height = dim[0]
#     width = dim[1]
#
#     h_factor = a.shape[0] / height + 1
#     w_factor = a.shape[1] / width + 1
