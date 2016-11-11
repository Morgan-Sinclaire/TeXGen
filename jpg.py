import os
from skimage import io
from brancher import *

content = tex_poly(.55)

with open('expression.tex','w') as f:
    f.write(content)

os.system("latex expression")
os.system("dvipng -D 200 expression -T tight")

a = io.imread('expression1.png')

# print a.shape
