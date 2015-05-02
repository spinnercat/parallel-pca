import numpy as np
import pickle

"""
make each row of vs and x have norm 1 and multiply
vs: m-by-n
xs: p-by-n
"""
def project(vs, xs):
   for row in vs:
       row /= np.sqrt(sum(row**2))

   for row in xs:
       row /= np.sqrt(sum(row**2))

   return np.dot(vs, xs.T)

if __name__ == '__main__':
   # read in vs from eigendecomposition
   # read in xs from data file
   pickle.load('eigen.out')
   compressed = project(vs, xs)
   rec = np.dot(compressed.T, vs)

   print np.sum(np.sum((rec - xs))^2)
