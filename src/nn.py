import matplotlib.pyplot as plt
import numpy
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from keras.models import model_from_json

FILE_MODEL_WEIGHTS = "../data/model.h5"
FILE_MODEL_STRUCTURE = "../data/nn_model.json"
ACCURACY_TO = 0.9
ACCURACY_FROM = 0.5
EPOCH = 100
Y_CLASSES = 3


class Dataset:
    def __init__(self, file_suffix, y_column=0):
        dataset = numpy.loadtxt("../data/matrix_{}.txt".format(file_suffix), dtype=int)
        columns = len(dataset[0])
        print("total columns in dataset: {}".format(columns))
        self.x_matrix = dataset[:, 0:columns - Y_CLASSES]
        self.y_matrix = dataset[:, columns - Y_CLASSES:columns]
        self.y_matrix = self.y_matrix[:, (0 + y_column):(1 + y_column)]
        self.x_width = len(self.x_matrix[0])
        self.height = len(self.x_matrix)
        self.classes = 1
        print("first line in X:\n{}".format(self.x_matrix[0]))
        print("first line in Y:\n{}".format(self.y_matrix[0]))


def run_nn(result_file, drop1=None, drop2=None, drop3=None, dataset_suffix="data", y_column=0):
    dataset = Dataset(dataset_suffix, y_column=y_column)

    # create model
    model = Sequential()
    if drop1 is not None:
        model.add(Dropout(drop1, input_shape=(dataset.x_width,)))

    model.add(Dense(dataset.x_width, input_dim=dataset.x_width, init='uniform', activation='relu'))

    if drop2 is not None:
        model.add(Dropout(drop2))

    model.add(Dense(dataset.x_width, init='uniform', activation='relu'))

    if drop3 is not None:
        model.add(Dropout(drop3))

    model.add(Dense(dataset.classes, init='uniform', activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    history = model.fit(dataset.x_matrix, dataset.y_matrix, validation_split=0.3, nb_epoch=EPOCH, batch_size=1000)

    # evaluate the model
    scores = model.evaluate(dataset.x_matrix, dataset.y_matrix)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    stats = history.history
    plt.plot(stats['acc'], color="#0c8c52")
    plt.plot(stats['val_acc'], color="#db7053")
    plt.title('model accuracy {} {} {}'.format(drop1, drop2, drop3))
    plt.xlabel('epoch')
    plt.legend(['acc', 'val_acc', ], loc='upper right')
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


def predict(model, dataset_suffix="predictions"):
    dataset = Dataset(dataset_suffix)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    score = model.evaluate(dataset.x_matrix, dataset.y_matrix, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))
    predictions = model.predict(dataset.x_matrix)
    total_ok_absolute = 0
    total_ok_relative = 0
    for i, y in enumerate(dataset.y_matrix):
        predict_probabilities = predictions[i]
        predict_absolute = [int(predict_probabilities[col] > 0.5) for col in range(dataset.classes)]
        predict_relative = [int(predict_probabilities[col] == max(predict_probabilities)) for col in
                            range(dataset.classes)]
        accurates_absolute = [predict_absolute[col] == y[col] for col in range(dataset.classes)]
        accurates_relative = [predict_relative[col] == y[col] for col in range(dataset.classes)]
        accurate_absolute_all = all(accurates_absolute)
        accurates_relative_all = all(accurates_relative)
        if accurate_absolute_all:
            total_ok_absolute += 1
        if accurates_relative_all:
            total_ok_relative += 1
        print(
            "index {} expected {}  probabilities {:<40} absolute{} accurate{:<21}={:<7} relative{} accurate{:<21}={:<7}".format(
                i,
                y,
                str(predict_probabilities),
                predict_absolute,
                str(accurates_absolute),
                str(accurate_absolute_all),
                predict_relative,
                str(accurates_relative),
                str(accurates_relative_all),
            ))

    print("total ok absolute {}/{} = {}".format(total_ok_absolute, dataset.height, total_ok_absolute / dataset.height))
    print("total ok relative {}/{} = {}".format(total_ok_relative, dataset.height, total_ok_relative / dataset.height))


# numpy.random.seed(7)
do_train = True
do_predict = False
if do_train:
    # fit_model = run_nn("WIN", drop1=0.5, drop2=0.2, drop3=0.2, y_column=0)
    fit_model = run_nn("EVEN", drop1=0.5, drop2=0.2, drop3=0.2, y_column=1)
    # fit_model = run_nn("LOSS", drop1=0.5, drop2=0.2, drop3=0.2, y_column=2)
    save_model(fit_model)

if do_predict:
    loaded_model = load_model()
    predict(loaded_model, "data")
