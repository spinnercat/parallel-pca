import numpy as np
from numpy_pca import NumpyPCA
from parallel_pca import ParallelPCA
from serial_pca import SerialPCA

serial_pca = SerialPCA()
parallel_pca = ParallelPCA()
np_pca = NumpyPCA()

# Dimension of data for testing
dimension = 3
# N is the number of samples
n = 4

def generate_sample_data():
  data = []
  for i in range(0,n):
    datum = np.zeros(dimension)
    base = np.random.normal(0.0, 1)
    datum[0] = base
    for j in range(1, dimension):
      # Generate data with just a bit of noise - should be roughly [x, 2x, 3x, etc.]
      datum[j] = (base + np.random.normal(0.0, abs(base * 0.1))) * (j+1)
    data.append(datum)
  return np.array(data)

print generate_sample_data()
