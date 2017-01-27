from src.analyzer_prepare import *
import numpy

prepare = PrepareData()
prepare.print_verbose = True
matrix = prepare.prepare_data_matrix()
for row in matrix:
    print(row)

numpy.savetxt("../data/matrix.txt", matrix, '% 4d')
