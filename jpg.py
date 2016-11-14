import os
from skimage import io
from skimage.viewer import ImageViewer
import numpy as np
from timeit import timeit
from brancher import *


def jpg():
    content = tex_poly(False)

    with open('expression.tex','w') as f:
        f.write(content)

    os.system("latex expression scriptname >/dev/null")
    os.system("dvipng -D 200 expression -T 16cm,5cm >/dev/null")

    return io.imread('expression1.png')

sample_size = 10
# data = np.array([jpg() for i in range(sample_size)])
#
# print data.shape
# for i in range(sample_size):
#     a = jpg()
#     if a.shape != (393, 1259):
#         print a.shape
#         ImageViewer(a).show()
# for i in range(10):
#     print jpg().shape

ImageViewer(jpg()).show()
