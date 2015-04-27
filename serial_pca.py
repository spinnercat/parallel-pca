# Class implementing the same algorithm as we run in parallel, but in serial for comparison purposes.
from pca import PCA

class SerialPCA(PCA):
  def do_pca(self, data):
    raise "Not implemented"