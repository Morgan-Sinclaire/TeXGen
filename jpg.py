import os
from skimage import io
from skimage.viewer import ImageViewer
import numpy as np
from timeit import timeit
from brancher import *

#
def jpg():
    content,indic = tex_poly(random.choice(symbols))

    with open('expression.tex','w') as f:
        f.write(content)

    os.system("latex expression scriptname >/dev/null")
    os.system("dvipng -D 200 expression -T 16cm,5cm >/dev/null")

    # return io.imread('expression1.png'),pos
    return indic


# def gen(n_samples):
#     labels = np.zeros((1000,7))

labels = np.zeros((1000,7))

for i in xrange(1000):
    labels[i] = jpg()
    os.system("mv expression1.png images/expression{}.png".format(i))

np.savetxt("labels/labels.csv", labels)
