import numpy as np


def read(path="../exploration/data.txt"):
    initial_matrix = np.genfromtxt(open(path, "r"), delimiter=" ", dtype=int)
    initial_matrix = np.array(initial_matrix).astype('int')
    return (initial_matrix[:,:-1], np.ravel(initial_matrix[:,-1:]))


#samples, classes = read("../exploration/data.txt")
#print samples
#print classes
