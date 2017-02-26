import matplotlib.pyplot as plt
import numpy
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from keras.models import model_from_json

WIN = "WIN"
EVEN = "EVEN"
LOSS = "LOSS"
COLUMN_WIN = 0
COLUMN_EVEN = 1
COLUMN_LOSS = 2

FILE_MODEL_WEIGHTS = "../data/model_weights_{}.h5"
FILE_MODEL_STRUCTURE = "../data/model_structure_{}.json"
ACCURACY_TO = 1.0
ACCURACY_FROM = 0.5
EPOCH = 300
Y_CLASSES = 3


class Dataset:
    def __init__(self, file_suffix, y_column):
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


def run_nn(name, drop1=None, drop2=None, drop3=None, dataset_suffix="data", y_column=0):
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
    plt.legend(['acc', 'val_acc', ], loc='upper left')
    axes = plt.gca()
    axes.set_xticks(numpy.arange(0, EPOCH, EPOCH / 10))
    axes.set_ylim([ACCURACY_FROM, ACCURACY_TO])
    axes.set_yticks(numpy.arange(ACCURACY_FROM, ACCURACY_TO, 0.02))
    plt.grid()

    plt.savefig("../data/nn/{}.svg".format(name))
    plt.close()

    save_model(model, name)

    return model


def save_model(model, name):
    # save structure
    model_json = model.to_json()
    with open(FILE_MODEL_STRUCTURE.format(name), "w") as json_file:
        json_file.write(model_json)
    # save weights
    model.save_weights(FILE_MODEL_WEIGHTS.format(name))


def load_model(name):
    with open(FILE_MODEL_STRUCTURE.format(name), "r") as json_file:
        model = model_from_json(json_file.read())
        model.load_weights(FILE_MODEL_WEIGHTS.format(name))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model


def predict(model, y_column, dataset_suffix="predictions"):
    dataset = Dataset(dataset_suffix, y_column)
    score = model.evaluate(dataset.x_matrix, dataset.y_matrix, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))
    return model.predict(dataset.x_matrix)


# numpy.random.seed(7)
do_train = False
do_predict = True

if do_train:
    run_nn(WIN, drop1=0.3, drop2=0.1, drop3=0.2, y_column=COLUMN_WIN)
    run_nn(EVEN, drop1=0.1, drop2=None, drop3=None, y_column=COLUMN_EVEN)
    run_nn(LOSS, drop1=0.1, drop2=None, drop3=None, y_column=COLUMN_LOSS)

if do_predict:
    model_win = load_model(WIN)
    model_even = load_model(EVEN)
    model_loss = load_model(LOSS)
    prediction_database = "data"
    predictions_win = predict(model_win, dataset_suffix=prediction_database, y_column=COLUMN_WIN)
    predictions_even = predict(model_even, dataset_suffix=prediction_database, y_column=COLUMN_EVEN)
    predictions_loss = predict(model_loss, dataset_suffix=prediction_database, y_column=COLUMN_LOSS)

    y_win = Dataset(prediction_database, COLUMN_WIN).y_matrix
    y_even = Dataset(prediction_database, COLUMN_EVEN).y_matrix
    y_loss = Dataset(prediction_database, COLUMN_LOSS).y_matrix
    total_ok_win = 0
    total_ok_even = 0
    total_ok_loss = 0
    total_ok_all = 0
    for i in range(len(y_win)):
        prediction_win = predictions_win[i]
        prediction_even = predictions_even[i]
        prediction_loss = predictions_loss[i]
        predict_absolute_win = int(prediction_win > 0.5)
        predict_absolute_even = int(prediction_even > 0.5)
        predict_absolute_loss = int(prediction_loss > 0.5)
        actual_win = y_win[i][0]
        actual_even = y_even[i][0]
        actual_loss = y_loss[i][0]
        ok_win = (actual_win == predict_absolute_win)
        ok_even = (actual_even == predict_absolute_even)
        ok_loss = (actual_loss == predict_absolute_loss)

        if ok_win:
            total_ok_win += 1
        if ok_even:
            total_ok_even += 1
        if ok_loss:
            total_ok_loss += 1
        if ok_win and ok_even and ok_loss:
            total_ok_all += 1

        print("actual ({},{},{}) predict (win/even/loss) ({},{},{}) absolute ({},{},{})".format(
            actual_win,
            actual_even,
            actual_loss,
            prediction_win,
            prediction_even,
            prediction_loss,
            predict_absolute_win,
            predict_absolute_even,
            predict_absolute_loss
        ))

        #     accurates_absolute = [predict_absolute[col] == y[col] for col in range(dataset.classes)]
        #     predict_relative = [int(predict_probabilities[col] == max(predict_probabilities)) for col in
        #                         range(dataset.classes)]
        #     accurates_relative = [predict_relative[col] == y[col] for col in range(dataset.classes)]
        #     accurate_absolute_all = all(accurates_absolute)
        #     accurates_relative_all = all(accurates_relative)
        #     if accurate_absolute_all:
        #         total_ok_absolute += 1
        #     if accurates_relative_all:
        #         total_ok_relative += 1
        #     print(
        #         "index {} expected {}  probabilities {:<40} absolute{} accurate{:<21}={:<7} relative{} accurate{:<21}={:<7}".format(
        #             i,
        #             y,
        #             str(predict_probabilities),
        #             predict_absolute,
        #             str(accurates_absolute),
        #             str(accurate_absolute_all),
        #             predict_relative,
        #             str(accurates_relative),
        #             str(accurates_relative_all),
        #         ))
        #
        # print("total ok absolute {}/{} = {}".format(total_ok_absolute, dataset.height, total_ok_absolute / dataset.height))
        # print("total ok relative {}/{} = {}".format(total_ok_relative, dataset.height, total_ok_relative / dataset.height))
        print("total ok (winn/even/loss) ({},{},{})  all {} ".format(
            total_ok_win,
            total_ok_even,
            total_ok_loss,
            total_ok_all
        ))
