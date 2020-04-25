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

# non va il modulo scikits.sparse.cholmod perchè non si riesce a installare su
# windows 7, inoltre è un wrapper della libreria eigen di c++...

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
	# Read in mtx file by scipy
	coo_mat = scipy.io.mmread('../../data/ex15.mtx')

	# Scipy matrix in coo layout can be easily converted to other types: csr and csc.
	# csr_mat = coo_mat.tocsr(copy=True)
	return coo_mat.tocsc()
	#print(A.todense())
	#pdb.set_trace()

@profile
def main():
	A = read_matrix()
	print("Number of zeros", A.nnz)

	# If you just want the number of bytes of the array elements
	print("The number of bytes: ", A.data.nbytes + A.indptr.nbytes + A.indices.nbytes)
	print("A.data.nbytes", A.data.nbytes)
	print("A.indptr.nbytes", A.indptr.nbytes)
	print("A.indices.nbytes", A.indices.nbytes)

	#pdb.set_trace()

	# get dimensions of matrix
	[xSize, ySize] = A.get_shape()

	# vettore incognite tutte a 1
	xe = np.ones(ySize)

	# vettore termini noti dato da A*xe = b
	b = A.dot(xe)

	'''
	# no sparse_cholesky execution
	start = time.process_time()
	L = no_sparse_cholesky(A.todense())
	end = time.process_time()
	print("Time execution no_sparse_cholesky: " + str(end - start))
	print(np.dot(L, L.T.conj())) # Verify
	
	'''
	# sparse_cholesky execution
	start = time.process_time()
	Ls = sparse_cholesky(A)
	end = time.process_time()

	x = Ls(b) # solves the equation Ax=b

	print("The solution is: ")
	print(x)
	print('\n')
	print("Time execution sparse_cholesky: " + str(end - start))
	print("The error relative is: ", np.linalg.norm(x-xe)/np.linalg.norm(xe))

	# matrice cholesky size
	# prima e dopo 
	
	'''
	spB = Ls.L()
	bo = np.allclose(A.todense(),spB.dot(spB.T).todense()) # Just for verification
	print(bo)
	'''	

if __name__ == "__main__":
	main()