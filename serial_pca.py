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
        psis = np.array([])
        for k in range(blocks):
            dataBlock = dataNew[(k * blocks):((k + 1) * blocks),:]
            covs.append(1./size * np.dot(dataBlock.T, dataBlock))
            w, v = np.linalg.eig(covs[k])
            psi = np.dot(v, (np.diag((size * w)**0.5)))
            if len(psis) == 0:
                psis = psi
            else:
                psis = np.hstack((psis, psi))

        R = 1./size * np.dot(psis.T, psis)
        wR, vR = np.linalg.eig(R)

        inv_sqrt = np.diag((size * wR)**(-0.5))
        vT = np.dot(np.dot(psis, vR), inv_sqrt)
        idx = (-wR).argsort()
        print wR[idx], vT[:,idx].T
        return wR[idx], vT[:,idx].T

