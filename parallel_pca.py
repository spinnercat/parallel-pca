from mrjob.job import MRJob
from mrjob.protocol import PickleProtocol
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
dims = 4
blocks = 2
per_block = 2
class MRPCACovParallel(MRJob):
    #def mapper_init(self):
    # self.sum = 0

  MRJob.INTERNAL_PROTOCOL = PickleProtocol
  MRJob.OUTPUT_PROTOCOL = PickleProtocol

  def mapper(self, _, line):
    dataBlockRow = np.array([float(x) for x in line.split()])
    size = len(dataBlockRow) / dims
    dataBlock = dataBlockRow.reshape((size, dims))
    yield None, 1./size * np.dot(dataBlock.T, dataBlock)

   #def mapper_final(self):
   #  yield None, self.sum

  def reducer(self, _, values):
    total_cov = np.zeros((dims, dims))
    for cov in values:
      total_cov += (1. / blocks) * cov

    w, v = np.linalg.eig(total_cov)
    yield w, v

class MRPCAEigenParallel(MRJob):
    #def mapper_init(self):
    #self.sum = 0

  def mapper(self, _, line):
    dataBlockRow = np.array([float(x) for x in line.split()])
    size = len(dataBlockRow) / dims
    dataBlock = dataBlockRow.reshape((size, dims))
    cov = 1./size * np.dot(dataBlock.T, dataBlock)
    w, v = np.linalg.eig(cov)
    yield None, v

  #def mapper_final(self):
  #  yield None, self.sum

  def reducer(self, _, values):
    eigs = np.array([])
    for eig in values:
      if len(eigs) == 0:
        eigs = eig
      else:
        eigs = np.hstack((eigs, eig))

    R = 1. / per_block * np.dot(eigs.T, eigs)
    wR, vR = np.linalg.eig(R)
    wR[wR < 0] = 0.1
    inv_sqrt = per_block * np.diag(wR**(-0.5))
    vT = np.dot(np.dot(eigs, vR), inv_sqrt)
    print wR, vT.T
    yield wR, vT.T

if __name__ == '__main__':
    MRPCACovParallel.run()
