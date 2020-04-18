import pdb
import sys
import scipy.io
import scipy.sparse
from scipy.sparse import linalg as splinalg
from scipy import array, linalg, dot
import pandas as pd #print(pd.__version__)
import numpy as np
import time
#from scikits.sparse.cholmod import cholesky

# https://en.wikipedia.org/wiki/Path_(computing)
# https://gist.github.com/Puriney/98544b779bcb815926f7acf87f537e61
# https://github.com/benfred/implicit/blob/master/benchmarks/benchmark_als.py

def no_sparse_cholesky(csc_mat):
	#print(csc_mat.todense(), end="\n\n")

	# lower=True is upper-triangular
	L = linalg.cholesky(csc_mat.todense(), lower=True) # Perform Cholesky decomposition 
	print(L, end="\n\n")

	return L

def sparse_cholesky(spA): 
	# The input matrix spA must be a sparse symmetric positive-definite.

	'''
	Scipy does not currently provide a routine for cholesky decomposition
	of a sparse matrix. This functionality is available in numpy and scipy
	for dense matrices and in scikits.sparse for sparse matrices, depending on your matrix.
	'''
	pdb.set_trace()
	factor = cholesky(spA)
	spB = factor.L()
	np.allclose(spA.todense(),spB.dot(spB.T).todense()) # Just for verification

def main():
	# Read in mtx file by scipy
	coo_mat = scipy.io.mmread('../../data/ex15.mtx')

	# Scipy matrix in coo layout can be easily converted to other types: csr and csc.
	# csr_mat = coo_mat.tocsr(copy=True)
	csc_mat = coo_mat.tocsc()
	print(csc_mat, end="\n\n")
	
	start = time.process_time()
	L = no_sparse_cholesky(csc_mat)
	#sparse_cholesky(csc_mat)
	end = time.process_time()

	print("Time execution: " + str(end - start), end="\n\n")

	#print(np.allclose(L.T.dot(L),csc_mat)) # Verify




	'''
	# csr to Pandas sparse data frame
	sp_df = pd.SparseDataFrame(csr_mat)#.fillna(0)
	print(sp_df)

	sp_df = pd.SparseDataFrame(csr_mat).fillna(0)
	print(sp_df)

	'''

if __name__ == "__main__":
	main()