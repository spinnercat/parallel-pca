"""
Format for file: Each line of the output file
should have all the data for a block, i.e.,
the subset of data each processing element works on. In this file,
I want a variable with the number of dimensions of each datum
as well as the total number of data points, so I can import those
variables into another file.
"""

import numpy as np
import pickle

n = 8795 # Number of data points
dimension = 100 * 80 # Dimension of each point
num_blocks = 4

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

def split_data(data, out_file):
  num_per_block = n / num_blocks
  for block in range(0, num_blocks):
    print block
    row = []
    for i in range(num_per_block):
      out_file.write(" ".join(data[block * num_per_block + i])+" ")
    out_file.write("\n")

def read_file(file):
  file = open(file)
  results = []
  row_count = 0
  for row in file:
    row_count += 1
    results.append(row.split())
  return results

if __name__ == '__main__':
  # data = generate_sample_data()
  data = read_file("images.txt")
  out_file = open("data_4_blocks", 'w')
  split_data(data, out_file)
  out_file.close()
