from mrjob.job import MRJob
from mrjob.protocol import PickleProtocol
import numpy as np
from pca import PCA
from data_creator import n, dimension, num_blocks
import time
import utils

from ParallelPCATester import read_file

SMART = True

# Class implementing PCA in parallel
class ParallelPCA(PCA):
  def do_pca(self, data):
    raise Exception("Not implemented")

# dimensions
# blocks?
# size?
per_block = n / num_blocks
class MRPCACovParallel(MRJob):
    #def mapper_init(self):
    # self.sum = 0

  MRJob.INTERNAL_PROTOCOL = PickleProtocol
  MRJob.OUTPUT_PROTOCOL = PickleProtocol

  def mapper(self, k, line):
    print "mapper", k
    dataBlockRow = np.array([float(x) for x in line.split()])
    size = len(dataBlockRow) / dimension
    dataBlock = dataBlockRow.reshape((size, dimension))
    print "doing multiplication"
    cov = 1./size * np.dot(dataBlock.T, dataBlock)
    print "done with mutiplication"
    yield None, cov

   #def mapper_final(self):
   #  yield None, self.sum

  def reducer(self, _, values):
    print "reducer"
    total_cov = np.zeros((dimension, dimension))
    for cov in values:
      total_cov += (1. / num_blocks) * cov

    print "calculate eigenvalues"
    w, v = np.linalg.eig(total_cov)
    print w, v.T
    yield None, None

class MRPCAEigenParallel(MRJob):

  def mapper(self, _, line):
    dataBlockRow = np.array([float(x) for x in line.split()])
    size = len(dataBlockRow) / dimension
    dataBlock = dataBlockRow.reshape((size, dimension))

    if SMART:
        cov = 1./size * np.dot(dataBlock, dataBlock.T)
        w, v = np.linalg.eig(cov)
        v = np.dot(dataBlock.T, v)
    else:
        cov = 1./size * np.dot(dataBlock.T, dataBlock)
        w, v = np.linalg.eig(cov)

    num_eigens = 10
    idx = (-w).argsort()
    w = w[idx[:num_eigens]]
    v = v[:,idx[:num_eigens]]
    psi = np.dot(v, (np.diag((per_block * w)**0.5)))
    yield None, psi 

  def reducer(self, _, values):
    psis = np.array([])
    for psi in values:
      if len(psis) == 0:
        psis = psi
      else:
        psis = np.hstack((psis, psi))

    R = 1. / per_block * np.dot(psis.T, psis)
    wR, vR = np.linalg.eig(R)
    wR = np.real(wR)
    vR = np.real(vR)
    wR[wR <= 0] = 1e-20

    inv_sqrt = np.diag((per_block * wR)**(-0.5))
    vT = np.dot(np.dot(psis, vR), inv_sqrt)

    idx = (-wR).argsort()
    print wR[idx], vT[:,idx[:5]].T
    yield None, vT[:,idx[:5]].T

if __name__ == '__main__':
    data = read_file('images.txt')

    file = open('data.out', 'r')
    mr_job = MRPCAEigenParallel()
    mr_job.sandbox(stdin=file)

    start_time = time.time()
    with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            _, value = mr_job.parse_output_line(line)
    end_time = time.time()

    print value.shape
    print np.array(data).shape
    # utils.reconstruct_images(value, np.array(data))
    utils.calc_error(value, np.array(data))

    print "Time", end_time - start_time

