sample_size = 1000
X = np.zeros((sample_size,393,1259)).astype('uint8')
y = np.zeros(sample_size).astype('uint8')
for i in xrange(sample_size):
    arr,pos = jpg()
    X[i] = arr
    y[i] = pos

X_piece = X_zoom[:,:,:40]
X_piece_train, X_piece_test = X_piece[:800].reshape(800,40*40), X_piece[800:].reshape(200,40*40)

import csv
with open('labels/labels.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for i in b:
        wr.writerow(i)
