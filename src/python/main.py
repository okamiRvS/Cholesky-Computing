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
import datetime
import csv
from os import walk

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


today = datetime.date.today()

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

def read_matrix(path):
	start = time.process_time()
	# Read in mtx file by scipy
	coo_mat = scipy.io.mmread(path)
	end = time.process_time()
	print("Import time: " + str(1000 * (end - start)), " ms")

	# Scipy matrix in coo layout can be easily converted to other types: csr and csc.
	# csr_mat = coo_mat.tocsr(copy=True)
	return coo_mat.tocsc()
	#print(A.todense())

def print_csv(header=False, row=None):
	fields=['program','name','import', 'rows', 'cols', 'nonZeros', 'size', 'chol', 'chol_size', 'sol_time', 'err']
	with open("Results_" + str(today) + '.csv', 'a', newline='') as csvfile:
		spamwriter = csv.DictWriter(csvfile, fieldnames=fields, delimiter=',')
		if header:
			spamwriter.writeheader()
		else :
			spamwriter.writerow(row)

def workflow(dirpath, matrix):
	row = {}
	row['program'] = "Python"
	try:
		row['name'] = matrix 
		start = time.process_time()
		A = read_matrix(dirpath+matrix)
		end = time.process_time()
		row['import'] = str(1000* (end - start))

		# dir(A) is similar to vars(A)
		# get dimensions of matrix
		[xSize, ySize] = A.get_shape()
		row['rows'] = xSize
		print("rows", xSize)
		row['cols'] = ySize
		print("cols", ySize)
		row['nonZeros'] = A.nnz
		print("Number of nonzero: ", A.nnz)
		size = A.data.nbytes + A.indptr.nbytes + A.indices.nbytes
		row['size'] = size
		print("A size: ", size, " bytes")

		# vettore incognite tutte a 1
		xe = np.ones(ySize)

		# vettore termini noti dato da A*xe = b
		b = A.dot(xe)

		# sparse_cholesky execution
		start = time.process_time()
		Ls = sparse_cholesky(A)
		end = time.process_time()
		row['chol'] = str(1000* (end - start))
		print("Time execution of sparse cholesky: " + str(1000* (end - start)), " ms")
		print('\n')

		start = time.process_time()
		x = Ls(b) # solves the equation Ax=b
		end = time.process_time()
		row['sol_time'] = str(1000* (end - start))

		# If you just want the number of bytes of the array elements
		chol_size = Ls.L().data.nbytes + Ls.L().indptr.nbytes + Ls.L().indices.nbytes
		row['chol_size'] = chol_size
		print("Ls size: ", chol_size, " bytes")
		print('\n')

		print("The solution is: ")
		print(x)
		err = np.linalg.norm(x-xe)/np.linalg.norm(xe)
		row['err'] = err
		print("The error is: ", err)

		print_csv(row=row)
	except:
		print("Error with: " + matrix)



#@profile
def main():
	f = []
	for (dirpath, dirnames, filenames) in walk("../../data/"):
	    f.extend(filenames)
	    break
	print_csv(header=True)
	for matrix in f:
		workflow(dirpath, matrix)


if __name__ == "__main__":
	main()