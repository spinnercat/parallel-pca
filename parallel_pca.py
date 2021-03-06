from mrjob.job import MRJob
from mrjob.protocol import PickleProtocol
import numpy as np
from pca import PCA
# from data_creator import n, dimension, num_blocks
import time
import utils
from matrix_utils import matrix_multiply

from ParallelPCATester import read_file

SMART = True

# Class implementing PCA in parallel
# dimensions
# blocks?
# size?
n = 512
dimension = 100 * 80
num_blocks = 1
per_block = n / num_blocks
class MRPCACovParallel(MRJob):

  MRJob.INTERNAL_PROTOCOL = PickleProtocol
  MRJob.OUTPUT_PROTOCOL = PickleProtocol

  def mapper(self, k, line):
    print "mapper", k
    dataBlockRow = np.array([float(x) for x in line.split()])
    size = len(dataBlockRow) / dimension
    dataBlock = dataBlockRow.reshape((size, dimension))
    print "doing multiplication"
    cov = 1./size * matrix_multiply(dataBlock.T, dataBlock)
    print "done with mutiplication"
    yield None, cov

  def reducer(self, _, values):
    print "reducer"
    total_cov = np.zeros((dimension, dimension))
    for cov in values:
      total_cov += (1. / num_blocks) * cov

    print "calculate eigenvalues"
    w, v = np.linalg.eig(total_cov)
    num_eigens = 1
    idx = (-w).argsort()
    v = v[:,idx[:num_eigens]]
    print w, v.T
    yield None, v.T

class MRPCAEigenParallel(MRJob):

  def mapper(self, _, line):
    start_time_y = time.time()
    dataBlockRow = np.array([float(x) for x in line.split()])
    size = len(dataBlockRow) / dimension
    dataBlock = dataBlockRow.reshape((size, dimension))

    if SMART:
        cov = 1./size * matrix_multiply(dataBlock, dataBlock.T)
        w, v = np.linalg.eig(cov)
        v = matrix_multiply(dataBlock.T, v)
    else:
        cov = 1./size * matrix_multiply(dataBlock.T, dataBlock)
        w, v = np.linalg.eig(cov)

    num_eigens = 10
    idx = (-w).argsort()
    w = w[idx[:num_eigens]]
    v = v[:,idx[:num_eigens]]
    psi = matrix_multiply(v, (np.diag((per_block * w)**0.5)))
    end_time_y = time.time()
    print "MAP TIME ", end_time_y - start_time_y
    yield None, psi 

  def reducer(self, _, values):
    start_time_x = time.time()
    psis = np.array([])
    for psi in values:
      if len(psis) == 0:
        psis = psi
      else:
        psis = np.hstack((psis, psi))

    R = 1. / per_block * matrix_multiply(psis.T, psis)
    wR, vR = np.linalg.eig(R)
    wR = np.real(wR)
    vR = np.real(vR)
    wR[wR <= 0] = 1e-20

    inv_sqrt = np.diag((per_block * wR)**(-0.5))
    vT = matrix_multiply(matrix_multiply(psis, vR), inv_sqrt)

    num_final_eigens = 50
    idx = (-wR).argsort()
    end_time_x = time.time()
    print vT, idx
    print "reduce time ",end_time_x - start_time_x
    yield None, 0

if __name__ == '__main__':
    data = read_file('images.txt')

    file = open('data_1_blocks', 'r')
    mr_job = MRPCAEigenParallel()
    mr_job.sandbox(stdin=file)

    start_time = time.time()
    print "start time ", start_time
    with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            _, value = mr_job.parse_output_line(line)
    end_time = time.time()

    utils.reconstruct_images(value, np.array(data))
    utils.calc_error(value, np.array(data))

    print "Time", end_time - start_time

