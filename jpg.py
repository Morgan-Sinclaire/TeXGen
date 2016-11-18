import os
from skimage import io
from skimage.viewer import ImageViewer
import numpy as np
from timeit import timeit
from brancher import *

# Takes a LaTeX string and indicator label, compiles png and returns indicator.
def jpg(symbol, n_samples, clear=False):
    # optionally, remove earlier images and their labels
    if clear:
        os.system("rm images/*")
        os.system("rm labels/labels.csv")
    # list of n.png images sorted by number n
    images = sorted(os.listdir("images")[1:], key=lambda x: int(x[:-4]))

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
                  images/{}.png >/dev/null".format(i))

        # appends labels to the .csv file
        with open('labels/labels.csv', 'a') as f:
            np.savetxt(f, indic.reshape(1, indic.shape[0]))


        # return io.imread('expression1.png'),pos
jpg(symbol, 10, True)
