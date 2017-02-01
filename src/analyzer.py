from src.analyzer_prepare import *
import numpy

prepare = PrepareData()
prepare.print_verbose = False
matrix = prepare.prepare_data_matrix()

numpy.savetxt("../data/matrix.txt", matrix, '% 8d')
