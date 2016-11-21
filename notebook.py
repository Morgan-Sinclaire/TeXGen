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


lr_ = .0001
batch_size_ = 32
epochs_ = 50

model = Sequential()
# input: 100x100 images with 3 channels -> (3, 100, 100) tensors.
# this applies 32 convolution filters of size 3x3 each.
model.add(Convolution2D(32, 3, 3, border_mode='valid', input_shape=(393, 1259,1)))
model.add(Activation('relu'))
model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Convolution2D(32, 3, 3, border_mode='valid'))
model.add(Activation('relu'))
model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
# Note: Keras does automatic shape inference.
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(7))
model.add(Activation('softmax'))

sgd = SGD(lr=lr_, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

try:
    print("start training")
    model.fit(X_train, y_train, batch_size=batch_size_, nb_epoch=epochs_, verbose=1)
except (KeyboardInterrupt, SystemExit):
    print("training interrupted.")
    pass
    #raise

from keras.models import model_from_json
with open('nn.json', 'w') as j:
    j.write(nn.to_json())
nn.save_weights('nn.h5')
with open('nn.json', 'r') as j:
    a = model_from_json(j.read())
a.load_weights('nn.h5')
