import numpy as np
from numpy_pca import NumpyPCA
#from parallel_pca import ParallelPCA
from serial_pca import SerialPCA
import time

serial_pca = SerialPCA()
#parallel_pca = ParallelPCA()
np_pca = NumpyPCA()

pca_calculators = [
  {"name": "Serial", "pca": serial_pca},
  # {"name": "Parallel", "pca": parallel_pca},
  #{"name": "Numpy", "pca": np_pca}
]

# Dimension of data for testing
dimension = 5
# N is the number of samples
n = 100

np.random.seed(0)
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

def read_file(file):
  file = open(file)
  results = []
  for row in file:
    results.append([float(x) for x in row.split()])
  return results

if __name__ == '__main__':
  data = read_file('images.txt')
  for calculator in pca_calculators:
    test_data = np.copy(data)
    start_time = time.time()
    components = calculator["pca"].do_pca(test_data)
    end_time = time.time()
    print "PCA calculation using "+calculator["name"]
    print "Time:", end_time - start_time
    print components
    print "\n\n\n\n"

