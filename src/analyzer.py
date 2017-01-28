from src.analyzer_prepare import *
import numpy

prepare = PrepareData()
prepare.print_verbose = False
matrix = prepare.prepare_data_matrix()

y = 0
for row in matrix:
    if row[-1] == 1:
        y += 1
print("{} out of {} = {}% are y=1".format(y, len(matrix), y/len(matrix)))
numpy.savetxt("../data/matrix.txt", matrix, '% 4d')
