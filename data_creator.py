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

n = 1000 # Number of data points
dimension = 5 # Dimension of each point
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

def split_data(data):
  results = []
  num_per_block = n / num_blocks
  for block in range(0, num_blocks):
    row = []
    for i in range(num_per_block):
      row.extend(data[block * num_per_block + i])
    results.append(row)
  return results

if __name__ == '__main__':
  data = generate_sample_data()
  split_data = split_data(data)

  out_file = open("data.out", 'wr')
  for row in split_data:
    for x in row:
      out_file.write(str(x)+" ")
    out_file.write("\n")

  out_file.close()
