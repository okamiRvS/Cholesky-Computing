import pdb
import sys
import scipy.io
import scipy.sparse as sparse
from scipy.sparse import linalg as splinalg
import numpy as np
from numpy import linalg as LA
import time
#from scikits.sparse.cholmod import cholesky

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

	factor = cholesky(A)
	'''

	# https://gist.github.com/omitakahiro/c49e5168d04438c5b20c921b928f1f5d
	n = A.shape[0]
	LU = splinalg.splu(A,diag_pivot_thresh=0) # sparse LU decomposition

	try : 
		resu = sparse.diags(LU.U.diagonal()**0.5)
		final = LU.L.dot(resu)
		return final
	except :
		print("The matrix is not positive definite")
		time.sleep(10)
		exit(1)

def main():
	# Read in mtx file by scipy
	coo_mat = scipy.io.mmread('../../data/ex15.mtx')

	# Scipy matrix in coo layout can be easily converted to other types: csr and csc.
	# csr_mat = coo_mat.tocsr(copy=True)
	A = coo_mat.tocsc()
	print(A.todense(), end="\n\n")

	# get dimensions of matrix
	[xSize, ySize] = A.get_shape()

	# vettore incognite tutte a 1
	xe = np.ones(ySize)

	# vettore termini noti dato da A*xe = b
	b = A.dot(xe)

	# no sparse_cholesky execution
	start = time.process_time()
	L = no_sparse_cholesky(A.todense())
	end = time.process_time()
	print("Time execution no_sparse_cholesky: " + str(end - start), end="\n\n")
	print(np.dot(L, L.T.conj()), end="\n\n") # Verify
	#print(LA.norm(x - xe)/LA.norm(xe))
	pdb.set_trace()

	# sparse_cholesky execution
	start = time.process_time()
	Ls = sparse_cholesky(A)
	end = time.process_time()
	print("Time execution sparse_cholesky: " + str(end - start), end="\n\n")
	print(np.dot(Ls, Ls.T.conj()), end="\n\n") # Verify
	pdb.set_trace()



if __name__ == "__main__":
	main()