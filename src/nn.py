import matplotlib.pyplot as plt
import numpy
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from keras.models import model_from_json

ALL = "ALL"
WIN = "WIN"
EVEN = "EVEN"
LOSS = "LOSS"
COLUMN_WIN = 0
COLUMN_EVEN = 1
COLUMN_LOSS = 2

FILE_MODEL_WEIGHTS = "../data/model_weights_{}.h5"
FILE_MODEL_STRUCTURE = "../data/model_structure_{}.json"
ACCURACY_TO = 0.8
ACCURACY_FROM = 0.3
EPOCH = 300
Y_CLASSES = 3


class Dataset:
    def __init__(self, file_suffix, y_column):
        dataset = numpy.loadtxt("../data/matrix_{}.txt".format(file_suffix), dtype=int)
        columns = len(dataset[0])
        print("total columns in dataset: {}".format(columns))
        self.x_matrix = dataset[:, 0:columns - Y_CLASSES]
        self.y_matrix = dataset[:, columns - Y_CLASSES:columns]
        if y_column is None:
            self.classes = Y_CLASSES
        else:
            self.classes = 1
            self.y_matrix = self.y_matrix[:, (0 + y_column):(1 + y_column)]
        self.x_width = len(self.x_matrix[0])
        self.height = len(self.x_matrix)
        print("first line in X:\n{}".format(self.x_matrix[0]))
        print("first line in Y:\n{}".format(self.y_matrix[0]))


def get_used_loss(y_column):
    if y_column is None:
        return 'categorical_crossentropy'
    else:
        return 'binary_crossentropy'


def run_nn(name, drop1=None, drop2=None, drop3=None, dataset_suffix="data", y_column=None):
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
    model.compile(loss=get_used_loss(y_column), optimizer='adam', metrics=['accuracy'])
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


def load_model(name, y_column):
    with open(FILE_MODEL_STRUCTURE.format(name), "r") as json_file:
        model = model_from_json(json_file.read())
        model.load_weights(FILE_MODEL_WEIGHTS.format(name))
        model.compile(loss=get_used_loss(y_column), optimizer='adam', metrics=['accuracy'])
        return model


def predict(model, y_column=None, dataset_suffix="predictions"):
    dataset = Dataset(dataset_suffix, y_column)
    if y_column is not None:
        score = model.evaluate(dataset.x_matrix, dataset.y_matrix, verbose=0)
        print("%s evaluation %s: %.2f%%" % (y_column, model.metrics_names[1], score[1] * 100))
    return model.predict(dataset.x_matrix)


# numpy.random.seed(7)
do_train = True
do_predict = True
r = None
if do_train:
    m = run_nn(ALL, drop1=0.3, drop2=0.1, drop3=0.2)
    d = Dataset("data", None)
    r = m.predict(d.x_matrix)
    # run_nn(WIN, drop1=0.3, drop2=0.1, drop3=0.2, y_column=COLUMN_WIN)
    # run_nn(EVEN, drop1=0.1, drop2=None, drop3=None, y_column=COLUMN_EVEN)
    # run_nn(LOSS, drop1=0.1, drop2=None, drop3=None, y_column=COLUMN_LOSS)

if do_predict:
    model_win = load_model(WIN, y_column=COLUMN_WIN)
    model_even = load_model(EVEN, y_column=COLUMN_EVEN)
    model_loss = load_model(LOSS, y_column=COLUMN_LOSS)
    model_all = load_model(ALL, y_column=None)

    # prediction_database = "predictions"
    prediction_database = "data"

    predictions_win = predict(model_win, dataset_suffix=prediction_database, y_column=COLUMN_WIN)
    predictions_even = predict(model_even, dataset_suffix=prediction_database, y_column=COLUMN_EVEN)
    predictions_loss = predict(model_loss, dataset_suffix=prediction_database, y_column=COLUMN_LOSS)
    # predictions_all = predict(model_loss, dataset_suffix=prediction_database)
    predictions_all = r

    y_win = Dataset(prediction_database, COLUMN_WIN).y_matrix
    y_even = Dataset(prediction_database, COLUMN_EVEN).y_matrix
    y_loss = Dataset(prediction_database, COLUMN_LOSS).y_matrix
    total_ok_win = 0
    total_ok_even = 0
    total_ok_loss = 0
    total_ok_absolute = 0
    total_ok_relative = 0
    total_ok_all = 0
    for i in range(len(y_win)):
        prediction_win = predictions_win[i]
        prediction_even = predictions_even[i]
        prediction_loss = predictions_loss[i]
        prediction_all = predictions_all[i]
        predict_absolute_win = int(prediction_win > 0.5)
        predict_absolute_even = int(prediction_even > 0.5)
        predict_absolute_loss = int(prediction_loss > 0.5)
        actual_win = y_win[i][0]
        actual_even = y_even[i][0]
        actual_loss = y_loss[i][0]
        ok_win = (actual_win == predict_absolute_win)
        ok_even = (actual_even == predict_absolute_even)
        ok_loss = (actual_loss == predict_absolute_loss)
        max_prediction = max(prediction_win, prediction_even, prediction_loss)
        ok_relative = False
        if prediction_win == max_prediction:
            if actual_win:
                ok_relative = True
        elif prediction_loss == max_prediction:
            if actual_loss:
                ok_relative = True
        else:
            if actual_even:
                ok_relative = True

        if ok_relative:
            total_ok_relative += 1

        if ok_win:
            total_ok_win += 1
        if ok_even:
            total_ok_even += 1
        if ok_loss:
            total_ok_loss += 1
        if ok_win and ok_even and ok_loss:
            total_ok_absolute += 1

        max_prediction = max(prediction_all)
        ok_all = False
        if prediction_all[0] == max_prediction:
            if actual_win:
                ok_all = True
        elif prediction_all[2] == max_prediction:
            if actual_loss:
                ok_all = True
        else:
            if actual_even:
                ok_all = True

        if ok_all:
            total_ok_all += 1

        print(
            "{}: actual ({},{},{}) predict (win/even/loss) ({},{},{}) absolute ({},{},{}) relative max {} relative ok {}, all {} all ok {}".format(
                i,
                actual_win,
                actual_even,
                actual_loss,
                prediction_win,
                prediction_even,
                prediction_loss,
                predict_absolute_win,
                predict_absolute_even,
                predict_absolute_loss,
                max_prediction,
                ok_relative,
                prediction_all,
                ok_all
            ))

    print("total ok (win/even/loss) ({},{},{})  absolute {} relative {} all {} out of {}".format(
        total_ok_win,
        total_ok_even,
        total_ok_loss,
        total_ok_absolute,
        total_ok_relative,
        total_ok_all,
        len(y_win)
    ))
