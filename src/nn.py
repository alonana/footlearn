import matplotlib.pyplot as plt
import numpy
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from keras.models import model_from_json

FILE_MODEL_WEIGHTS = "../data/model.h5"
FILE_MODEL_STRUCTURE = "../data/nn_model.json"
ACCURACY_TO = 1.1
ACCURACY_FROM = 0.6
EPOCH = 300


def run_nn(result_file, drop1=None, drop2=None, drop3=None):
    dataset = numpy.loadtxt("../data/matrix.txt", dtype=int)
    numpy.random.seed(7)
    # split into input (X) and output (Y) variables
    columns = len(dataset[0])
    classes = 1
    x_matrix = dataset[:, 0:columns - classes]
    y_matrix = dataset[:, columns - classes:columns]
    print("total columns in dataset: {}".format(columns))
    # print("first lines in dataset:\n{}".format(dataset[0:header]))
    # print("first lines in X:\n{}".format(X[0:header]))
    # print("first lines in Y:\n{}".format(Y[0:header]))

    # create model
    model = Sequential()
    if drop1 is not None:
        model.add(Dropout(drop1, input_shape=(len(x_matrix[0]),)))

    model.add(Dense(150, input_dim=len(x_matrix[0]), init='uniform', activation='relu'))

    if drop2 is not None:
        model.add(Dropout(drop2))

    model.add(Dense(150, init='uniform', activation='relu'))

    if drop3 is not None:
        model.add(Dropout(drop3))

    model.add(Dense(classes, init='uniform', activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    history = model.fit(x_matrix, y_matrix, validation_split=0.3, nb_epoch=EPOCH, batch_size=1000)

    # kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    # for train, test in kfold.split(X, Y):
    #     model.fit(X[train], Y[train], validation_data=(X[test], Y[test]), nb_epoch=3000, batch_size=1000)

    # evaluate the model
    scores = model.evaluate(x_matrix, y_matrix)
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
    return model


def save_model(model):
    # save structure
    model_json = model.to_json()
    with open(FILE_MODEL_STRUCTURE, "w") as json_file:
        json_file.write(model_json)
    # save weights
    model.save_weights(FILE_MODEL_WEIGHTS)


def load_model():
    with open(FILE_MODEL_STRUCTURE, "r") as json_file:
        model = model_from_json(json_file.read())
        model.load_weights(FILE_MODEL_WEIGHTS)
        return model


train = False
if train:
    fit_model = run_nn("5_2_2", drop1=0.5, drop2=0.2, drop3=0.2)
    save_model(fit_model)

loaded_model = load_model()

dataset = numpy.loadtxt("../data/matrix.txt", dtype=int)
numpy.random.seed(7)
# split into input (X) and output (Y) variables
columns = len(dataset[0])
classes = 1
x_matrix = dataset[:, 0:columns - classes]
y_matrix = dataset[:, columns - classes:columns]
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
score = loaded_model.evaluate(x_matrix, y_matrix, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1] * 100))
predictions = loaded_model.predict(x_matrix)
total_ok = 0
for i, y in enumerate(y_matrix):
    predict_probability = predictions[i]
    predict_boolean = int(predict_probability > 0.5)
    accurate = predict_boolean == y[0]
    if accurate:
        total_ok += 1
    # if not accurate:
    print("index {} expected {} actual {}({}) accurate {}".format(
        i,
        y[0],
        predict_boolean,
        predict_probability,
        accurate))

print("total ok {}/{} = {}", total_ok, len(y_matrix), total_ok / len(y_matrix))
