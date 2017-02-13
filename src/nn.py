import matplotlib.pyplot as plt
import numpy
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential

ACCURACY_TO = 1.1
ACCURACY_FROM = 0.6
EPOCH = 300


def run_nn(result_file, drop1=None, drop2=None, drop3=None):
    dataset = numpy.loadtxt("../data/matrix.txt", dtype=int)
    numpy.random.seed(7)
    # split into input (X) and output (Y) variables
    columns = len(dataset[0])
    classes = 1
    X = dataset[:, 0:columns - classes]
    Y = dataset[:, columns - classes:columns]
    print("total columns in dataset: {}".format(columns))
    # print("first lines in dataset:\n{}".format(dataset[0:header]))
    # print("first lines in X:\n{}".format(X[0:header]))
    # print("first lines in Y:\n{}".format(Y[0:header]))

    # create model
    model = Sequential()
    if drop1 is not None:
        model.add(Dropout(drop1, input_shape=(len(X[0]),)))

    model.add(Dense(150, input_dim=len(X[0]), init='uniform', activation='relu'))

    if drop2 is not None:
        model.add(Dropout(drop2))

    model.add(Dense(150, init='uniform', activation='relu'))

    if drop3 is not None:
        model.add(Dropout(drop3))

    model.add(Dense(classes, init='uniform', activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    history = model.fit(X, Y, validation_split=0.3, nb_epoch=EPOCH, batch_size=1000)

    # kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    # for train, test in kfold.split(X, Y):
    #     model.fit(X[train], Y[train], validation_data=(X[test], Y[test]), nb_epoch=3000, batch_size=1000)

    # evaluate the model
    scores = model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    plt.plot(history.history['acc'], color="#0c8c52")
    plt.plot(history.history['loss'], color="#ed3807")
    plt.plot(history.history['val_acc'], color="#44936f", linestyle="--", linewidth=3)
    plt.plot(history.history['val_loss'], color="#db7053", linestyle="--", linewidth=3)
    plt.title('model accuracy {} {} {}'.format(drop1, drop2, drop3))
    plt.xlabel('epoch')
    plt.legend(['acc', 'loss', 'val_acc', 'val_loss', ], loc='upper right')
    axes = plt.gca()
    axes.set_xticks(numpy.arange(0, EPOCH, EPOCH / 10))
    axes.set_ylim([ACCURACY_FROM, ACCURACY_TO])
    axes.set_yticks(numpy.arange(ACCURACY_FROM, ACCURACY_TO, 0.02))
    plt.grid()

    plt.savefig("../data/nn/{}.svg".format(result_file))
    plt.close()



# run_nn("x_x_x")
# run_nn("4_x_x", drop1=0.4)
# run_nn("4_4_4", drop1=0.4, drop2=0.4, drop3=0.4)
run_nn("5_2_2", drop1=0.5, drop2=0.2, drop3=0.2)

# calculate predictions
# predictions = model.predict(X)
# print(predictions)
# for i,x in enumerate(X):
#    print ("{} {},{}".format(i,x,predictions[i]))
