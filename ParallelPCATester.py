import numpy as np
from numpy_pca import NumpyPCA
from parallel_pca import ParallelPCA
from serial_pca import SerialPCA
import time

serial_pca = SerialPCA()
parallel_pca = ParallelPCA()
np_pca = NumpyPCA()

pca_calculators = [
  {"name": "Serial", "pca": serial_pca},
  # {"name": "Parallel", "pca": parallel_pca},
  #{"name": "Numpy", "pca": np_pca}
]
data = []

for calculator in pca_calculators:
  test_data = np.copy(data)
  start_time = time.time()
  components = calculator["pca"].do_pca(test_data)
  end_time = time.time()
  print "PCA calculation using "+calculator["name"]
  print components
  print "\n\n\n\n"

