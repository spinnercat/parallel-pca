This code provides a framework for running and benchmarking both serial and
parallel versions of PCA.

Input files should be organized such that every row contains all the data for
a subblock. The dimension of each image and the nmber of blocks used should
be changed in the respective files, as described below.

To run the default serial version (referred to as NumpyPCA)
and the serial approximation (referred to as SerialPCA), we use the
framework provided by ParallelPCATester.py. You can just run this using
'python ParallelPCATester.py.'

To run the parallel version, run 'python parallel_pca.py'.


There are several helper files, including face_data_creator.py,
data_creator.py, utils.py, and matrix_utils.py that are not as important to a
user. They include the creation of input files from the original dataset of
images, as well as the functions used to measure the efficacy of PCA and
for matrix multiplication.
