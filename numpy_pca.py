# Class using numpy's PCA for comparison purposes.
from pca import PCA
import numpy as np
from numpy import linalg as la
import utils
import copy


class NumpyPCA(PCA):
  def do_pca(self, orig_data):
    data = copy.copy(orig_data)

    # Step 1: Make all data mean 0
    data = np.transpose(data)
    for row in data:
      mean = float(sum(row)) / len(row)
      for i in range(0, len(row)):
        row[i] = row[i] - mean
    x = data
    print "getting covariance"
    covariance_matrix = np.dot(data, np.transpose(data))
    print "got covariance"
    print covariance_matrix.shape
    [eigenvalues,eigenvectors] =  la.eig(covariance_matrix)
    eigenvectors = np.transpose(eigenvectors)
    print "got eigenvectors"

    # Sort by eigenvalue
    combined = []
    for i in range(0, len(eigenvalues)):
      combined.append((eigenvectors[i], eigenvalues[i]))
    combined.sort(key=lambda c: c[1], reverse=True)

    eigenvectors = []
    eigenvalues = []
    for i in range(0, len(combined)):
      eigenvectors.append(combined[i][0])
      eigenvalues.append(combined[i][1])

    eigenvectors = np.array(eigenvectors)


    utils.calc_error(eigenvectors, orig_data)