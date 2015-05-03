import numpy as np
import pickle

"""
make each row of vs and x have norm 1 and multiply
vs: m-by-n
xs: p-by-n
"""
def project(vs, xs):
    for row in vs:
        row /= np.float(np.sqrt(sum(row**2)))

    return np.dot(vs, xs.T)

def calc_error(vs, xs):
    compressed = project(vs, xs)
    print compressed
    rec = np.dot(compressed.T, vs)
    print rec

    print np.sqrt(np.sum((rec - xs)**2) / rec.size)

if __name__ == '__main__':
    vs = np.array([[2., 0., 0.], [0., 2., 0.]])
    xs = np.array([[2., 3., 1.], [4., 5., 6.], [-1., -3., 5.]])
    calc_error(vs, xs)

