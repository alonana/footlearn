from keras.models import Sequential
from keras.layers import Dense
import numpy

dataset = numpy.loadtxt("../data/matrix.txt", dtype=int)
seed = 7
numpy.random.seed(seed)
# split into input (X) and output (Y) variables
columns = len(dataset[0])
X = dataset[:, 0:columns - 1]
Y = dataset[:, columns - 1]
header = 3
print("total columns in dataset: {}", columns)
print("first lines in dataset:\n{}", dataset[0:header])
print("first lines in X:\n{}", X[0:header])
print("first lines in Y:\n{}", Y[0:header])

# create model
model = Sequential()
model.add(Dense(12, input_dim=len(X[0]), init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, nb_epoch=3000, batch_size=1000)
# evaluate the model
scores = model.evaluate(X, Y)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

# calculate predictions
# predictions = model.predict(X)
# print(predictions)
# for i,x in enumerate(X):
#    print ("{} {},{}".format(i,x,predictions[i]))
