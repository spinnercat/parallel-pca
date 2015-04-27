# Class using numpy's PCA for comparison purposes.
from pca import PCA
import numpy as np
import mdp

class NumpyPCA(PCA):
  def do_pca(self, data):
    return mdp.pca(data)