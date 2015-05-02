# from mrjob.job import MRJob
import numpy as np
from pca import PCA

# Class implementing PCA in parallel
class ParallelPCA(PCA):
  def do_pca(self, data):
    raise Exception("Not implemented")

#TODO(mardo): form of input?
# dimensions
# blocks?
# size?
class MRPCACovParallel(MRJob):
    #def mapper_init(self):
    # self.sum = 0

  def mapper(self, _, line):
    dataBlock = np.array(float(line.split()))
    yield None, 1./size * np.dot(dataBlock.T, dataBlock)

   #def mapper_final(self):
   #  yield None, self.sum

  def reducer(self, _, values):
    total_cov = np.zeros(values[0].shape)
    for cov in values:
      total_cov += cov

    w, v = np.linalg.eig(total_cov)
    yield w, v

class MRPCAEigenParallel(MRJob):
  def mapper_init(self):
    self.sum = 0

  def mapper(self, _, line):
    dataBlock =
    cov = 1./size * np.dot(dataBlock.T, dataBlock)
    w, v = np.linalg.eig(covs[k])

  #def mapper_final(self):
  #  yield None, self.sum

  def reducer(self, _, values):
    for eig in eigs:
      eigs = np.hstack((eigs, v))
    total_cov = np.zeros(values[0].shape)
    for cov in values:
      total_cov += cov

    w, v = np.linalg.eig(total_cov)
    R = 1 / len(means) * np.dot(eigs.T, eigs)
    wR, vR = np.linalg.eig(R)
    wR[wR < 0] = 0.1
    inv_sqrt = size * np.diag(wR**(-0.5))
    vT = np.dot(np.dot(eigs, vR), inv_sqrt)
    yield wR, vT.T

if __name__ == '__main__':
    MRPCACovParallel.run()
