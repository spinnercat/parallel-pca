from mrjob.job import MRJob
import numpy as np

# Class implementing PCA in parallel
class ParallelPCA(object):
  def __init__(self):

  # Do nothing

  def PCA(self):
# Idk what to do


N = 100001
h = 1. / N


class MREstimatePiIntegrationCombiner(MRJob):
  def mapper_init(self):
    self.sum = 0

  def mapper(self, _, line):
    index = int(line)
    x = index * h
    if h == 0:
      self.sum += 0.5
    elif h != N - 1:
      self.sum += np.sqrt(1 - x * x)

  def mapper_final(self):
    yield None, self.sum

  def reducer(self, _, values):
    yield None, h * sum(values)


if __name__ == '__main__':
  MREstimatePiIntegrationCombiner.run()
