from sklearn.model_selection import StratifiedKFold
from keras.models import Sequential
from keras.layers import Dense
import numpy
import matplotlib.pyplot as plt

dataset = numpy.loadtxt("../data/matrix.txt", dtype=int)
seed = 7
numpy.random.seed(seed)
# split into input (X) and output (Y) variables
columns = len(dataset[0])
classes = 3
X = dataset[:, 0:columns - classes]
Y = dataset[:, columns - classes:columns]
header = 1
print("total columns in dataset: {}".format(columns))
print("first lines in dataset:\n{}".format(dataset[0:header]))
print("first lines in X:\n{}".format(X[0:header]))
print("first lines in Y:\n{}".format(Y[0:header]))

# create model
model = Sequential()
model.add(Dense(12, input_dim=len(X[0]), init='uniform', activation='relu'))
model.add(Dense(12, init='uniform', activation='relu'))
model.add(Dense(classes, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(X, Y, validation_split=0.3, nb_epoch=20, batch_size=1000)

# kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
# for train, test in kfold.split(X, Y):
#     model.fit(X[train], Y[train], validation_data=(X[test], Y[test]), nb_epoch=3000, batch_size=1000)

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))


plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()



# calculate predictions
# predictions = model.predict(X)
# print(predictions)
# for i,x in enumerate(X):
#    print ("{} {},{}".format(i,x,predictions[i]))
