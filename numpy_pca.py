# Class using numpy's PCA for comparison purposes.
from pca import PCA
import numpy as np
from numpy import linalg as la


class NumpyPCA(PCA):
  def do_pca(self, data):
    data = np.transpose(data)
    for row in data:
      mean = float(sum(row)) / len(row)
      for i in range(0, len(row)):
        row[i] = row[i] - mean
    x = data
    print x

    covariance_matrix = np.dot(data, np.transpose(data))
    [eigenvalues,eigenvectors] =  la.eig(covariance_matrix)
    eigenvectors = np.transpose(eigenvectors)
    print "Eigenvalues of covariance: "
    print eigenvalues
    print eigenvectors

    combined = []
    for i in range(0, len(eigenvalues)):
      combined.append((eigenvectors[i], eigenvalues[i]))
    combined.sort(key=lambda c: c[1], reverse=True)

    q = []
    eigenvalues = []
    for i in range(0, len(combined)):
      q.append(combined[i][0])
      eigenvalues.append(combined[i][1])
    q = np.transpose(np.array(q)) # do we do this?

    qq = np.dot(np.transpose(q), q)
    y = np.dot(np.transpose(q), x)