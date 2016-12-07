# TeXGen

The aim of this project is to perform optical character recognition (OCR) on arbitrary characters, especially mathematical symbols. In particular, given a LaTeX-formatted formula, we want to identify the symbols composing it, and return the LaTeX for those symbols:

<!-- ![text](pictures/diagram.png) -->

To accomplish this task, we trained a convolutional neural network (CNN) in Keras. Using LaTeX, dvipng, and a couple Python scripts, thousands of .png files were generated of mathematical symbols. Using this data, we have so far gotten 97% accuracy on individual Greek letters.

For multiple characters, we took the simplistic approach of segmenting along vertical white space:

<!-- ![text](pictures/split.png) -->

However, we did have kerning in some cases:

<!-- ![text](pictures/kern.png) -->

Going forward, we hope to train the CNN on a wider range of mathematical symbols, which requires much more data generation, since LaTeX alone has thousands of mathematical symbols. In addition, we plan to develop better segmentation, account for different image sizes, and train the model on a variety of fonts.
