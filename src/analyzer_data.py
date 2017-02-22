import numpy

from src.analyzer.analyzer_prepare import *

sessions = SessionsData()
sessions.split_load_sessions("../data/split")

prepare = PrepareData()
prepare.print_verbose = False
prepare.print_last = True
matrix = prepare.prepare_data_matrix(sessions)
numpy.savetxt("../data/matrix_data.txt", matrix, '% 8d')
