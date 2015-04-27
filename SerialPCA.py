# Class implementing the same algorithm as we run in parallel, but in serial for comparison purposes.
class SerialPCA(object):
    def doPCA_cov(self, data, blocks):
        def center(X):
            meanX = X.mean(axis = 1)[:,np.newaxis]
            centeredX = X - meanX
            return (meanX, centeredX)

        (means, dataNew) = center(data)
        size = len(means) / blocks
        covs = []
        for k in range(blocks):
            covs.append(np.cov(dataNew[(k * blocks):((k + 1) * blocks)]))

        cov = (1. / blocks) * np.sum(covs)
        w, v = np.linalg.eig(cov)
        return v

    def doPCA_eig(self, data, blocks):
        def center(X):
            meanX = X.mean(axis = 1)[:,np.newaxis]
            centeredX = X - meanX
            return (meanX, centeredX)

        (means, dataNew) = center(data)
        size = len(means) / blocks
        covs = []
        eigs = np.array([[]])
        for k in range(blocks):
            covs.append(np.cov(dataNew[(k * blocks):((k + 1) * blocks)]))
            w, v = np.linalg.eig(covs[k])
            eigs = np.hstack(eigs, v)

        R = 1 / len(means) * np.dot(eigs.T, eigs)
        wR, vR = np.linalg.eig(R)
        vT = np.dot(np.dot(eigs, vR), np.inv(np.sqrt(len(means) * vR)))
        return vT
