# Class implementing the same algorithm as we run in parallel, but in serial for comparison purposes.
from pca import PCA
import numpy as np

class SerialPCA(object):
    def do_pca(self, data):
        #return self.doPCA_cov(data, 2)
        return self.doPCA_eig(data, 2)

    def doPCA_cov(self, data, blocks):
        def center(X):
            meanX = X.mean(axis = 0)[np.newaxis,:]
            centeredX = X - meanX
            return (meanX, centeredX)

        (means, dataNew) = center(data)
        size = len(data) / blocks
        print size
        covs = []
        for k in range(blocks):
            dataBlock = dataNew[(k * blocks):((k + 1) * blocks),:]
            covs.append(1./size * np.dot(dataBlock.T, dataBlock))

        print covs[0]
        acc = np.zeros(covs[0].shape)
        for cov in covs:
            acc += (1. / blocks) * cov

        w, v = np.linalg.eig(cov)
        return (w, np.transpose(v))

    def doPCA_eig(self, data, blocks):
        def center(X):
            meanX = X.mean(axis = 0)[np.newaxis,:]
            centeredX = X - meanX
            return (meanX, centeredX)

        (means, dataNew) = center(data)
        size = len(data) / blocks
        covs = []
        eigs = np.array([])
        for k in range(blocks):
            dataBlock = dataNew[(k * blocks):((k + 1) * blocks),:]
            covs.append(1./size * np.dot(dataBlock.T, dataBlock))
            w, v = np.linalg.eig(covs[k])
            if len(eigs) == 0:
                eigs = v
            else:
                eigs = np.hstack((eigs, v))

        print eigs.shape
        R = 1 / len(means) * np.dot(eigs.T, eigs)
        wR, vR = np.linalg.eig(R)
        wR[wR < 0] = 0.1
        print wR
        inv_sqrt = size * np.diag(wR**(-0.5))
        vT = np.dot(np.dot(eigs, vR), inv_sqrt)
        return vT.T

