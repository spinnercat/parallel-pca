# Class implementing the same algorithm as we run in parallel, but in serial for comparison purposes.
class SerialPCA(object):
    def doPCA(self, data, blocks):
        def center(X):
            meanX = X.mean(axis = 1)[:,np.newaxis]
            centeredX = X - meanX
            return (meanX, centeredX)

        (means, dataNew) = center(data)
        for k in range(blocks):
            cov = np.cov(dataNew[
