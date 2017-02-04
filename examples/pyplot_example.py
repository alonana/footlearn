import matplotlib.pyplot as plt
import numpy

# print("configuration file: {}".format(matplotlib.matplotlib_fname()))
# print(rcsetup.all_backends)
plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
plt.ylabel('some numbers')
axes = plt.gca()
axes.set_ylim([2, 7])
axes.set_xticks(numpy.arange(0, 10, 2))
axes.set_yticks(numpy.arange(2, 7, 1))
plt.grid()
plt.savefig("../data/pyplot_example.svg")
