# coding=utf-8
import pdb
import sys
import scipy.io
import scipy.sparse as sparse
from scipy.sparse import linalg as splinalg
from sksparse.cholmod import cholesky
import numpy as np
from numpy import linalg as LA
import time

# To install scikit-sparse
# IT WORKS ON LINUX, NOT ON WIN7, MAYBE IN WIN10
# https://scikit-sparse.readthedocs.io/en/latest/overview.html
# IF DOESN'T WORK FOLLOW THESE:
#
# AND THESE AS FOLLOW IN THIS ORDER
# pip3 install scikits.bootstrap # maybe this not useful
# pip3 install Cython
# pip3 install scikits.sparse

# To install Memory Profiler
# https://pypi.org/project/memory-profiler/
# python3 -m memory_profiler main.py

# Guide
# https://en.wikipedia.org/wiki/Path_(computing)
# https://gist.github.com/Puriney/98544b779bcb815926f7acf87f537e61
# https://github.com/benfred/implicit/blob/master/benchmarks/benchmark_als.py

# Time calculation
# https://stackoverflow.com/questions/53542186/how-to-compute-the-return-value-of-pythons-time-process-time-in-millisecond?noredirect=1&lq=1

def no_sparse_cholesky(csc_mat):
	# lower=True is upper-triangular
	L = scipy.linalg.cholesky(csc_mat, lower=True) # Perform Cholesky decomposition 
	#print(L, end="\n\n")
	return L

def sparse_cholesky(A): 
	# The input matrix spA must be a sparse symmetric positive-definite.

	'''
	Scipy does not currently provide a routine for cholesky decomposition
	of a sparse matrix. This functionality is available in numpy and scipy
	for dense matrices and in scikits.sparse for sparse matrices, depending on your matrix.
	'''
	
	return cholesky(A)

def read_matrix():
	start = time.process_time()
	# Read in mtx file by scipy
	coo_mat = scipy.io.mmread('../../data/G3_circuit.mtx')
	end = time.process_time()
	print("Import time: " + str(1000 * (end - start)), " ms")

	# Scipy matrix in coo layout can be easily converted to other types: csr and csc.
	# csr_mat = coo_mat.tocsr(copy=True)
	return coo_mat.tocsc()
	#print(A.todense())

#@profile
def main():
	A = read_matrix()

	# dir(A) is similar to vars(A)
	# get dimensions of matrix
	[xSize, ySize] = A.get_shape()
	print("rows", xSize)
	print("cols", ySize)
	print("Number of nonzero: ", A.nnz)
	print("A size: ", A.data.nbytes + A.indptr.nbytes + A.indices.nbytes, " bytes")

	# vettore incognite tutte a 1
	xe = np.ones(ySize)

	# vettore termini noti dato da A*xe = b
	b = A.dot(xe)

	# sparse_cholesky execution
	start = time.process_time()
	Ls = sparse_cholesky(A)
	end = time.process_time()
	print("Time execution of sparse cholesky: " + str(1000* (end - start)), " ms")
	print('\n')

	x = Ls(b) # solves the equation Ax=b

	# If you just want the number of bytes of the array elements
	print("Ls size: ", Ls.L().data.nbytes + Ls.L().indptr.nbytes + Ls.L().indices.nbytes, " bytes")
	print('\n')

	print("The solution is: ")
	print(x)
	print("The error is: ", np.linalg.norm(x-xe)/np.linalg.norm(xe))

	'''
	# no sparse_cholesky execution
	start = time.process_time()
	L = no_sparse_cholesky(A.todense())
	end = time.process_time()
	print("Time execution no_sparse_cholesky: " + str(end - start))
	print(np.dot(L, L.T.conj())) # Verify
	
	'''

if __name__ == "__main__":
	main()