# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
import numpy

# test my NN - if x1 + x2 between some ranges --> y=1
FILE_NAME = "../data/keras_example_simple.data"


def is_required(n):
    return 50 <= n <= 100 or 150 <= n <= 200 or 250 <= n <= 300 or 350 <= n <= 400


with open(FILE_NAME, 'w') as f:
    for i in range(0, 200, 10):
        for j in range(0, 200, 10):
            r = 1 if is_required(i + j) else 0
            f.write("{},{},{}\n".format(i, j, r))

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
dataset = numpy.loadtxt(FILE_NAME, delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:, 0:2]
Y = dataset[:, 2]
# create model
model = Sequential()
model.add(Dense(100, input_dim=2, init='uniform', activation='relu'))
model.add(Dense(100, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, nb_epoch=1000, batch_size=1000)
# evaluate the model
scores = model.evaluate(X, Y)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

# calculate predictions
predictions = model.predict(X)
# print(predictions)
for i, x in enumerate(X):
    sum = x[0] + x[1]
    predict_possibility = predictions[i]
    predict_boolean = predict_possibility > 0.5
    expected = is_required(sum)
    print("{}+{}={}  expected {} actual {}({}) accurate {}".format(
        x[0],
        x[1],
        sum,
        expected,
        predict_boolean,
        predict_possibility,
        predict_boolean == expected))
