# Class using numpy's PCA for comparison purposes.
from pca import PCA
import numpy as np
from sklearn.decomposition import PCA


class NumpyPCA(PCA):
  def do_pca(self, data):
    pca = PCA(n_components=2)
    pca.fit(data)
    return pca.get_params()