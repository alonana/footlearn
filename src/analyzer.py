from src.analyzer_prepare import *

prepare = PrepareData()
matrix = prepare.prepare_data_matrix()
print("{}", matrix)

correct = 0
for data_row in matrix:
    rank1 = data_row[0]
    rank2 = data_row[1]
    actual_win = data_row[3]
    predicted_win = 0
    if rank1 > rank2:
        predicted_win = 1

    if predicted_win == actual_win:
        correct += 1

accuracy = correct / len(matrix)
print("dummy accuracy: {}".format(accuracy))
