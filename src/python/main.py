# coding=utf-8
import pdb
import sys
import scipy.io
import scipy.sparse as sparse
from scipy.sparse import csc_matrix
from scipy.sparse import linalg as splinalg
from sksparse.cholmod import cholesky
import numpy as np
import time
import datetime
import csv
from os import walk

'''
To install scikit-sparse (IT WORKS ON LINUX, AND IN WIN10)
----------------------------------------------------------
Requirements:
To take "Microsoft Visual C++ Build Tools 2017" first of all you need visual studio 2017
Get it here": https://visualstudio.microsoft.com/it/vs/older-downloads/
Then in visual studio installer you could take as add-on in edit mode. This is important
to get elements to compile

Then install the GUI of cmake
https://tulip.labri.fr/TulipDrupal/?q=node/1081

There is a problem with scikit-sparse 0.4.3 version, so download the 0.4.4 here
https://github.com/scikit-sparse/scikit-sparse/
then take the setup.py here 
https://github.com/xmlyqing00/Cholmod-Scikit-Sparse-Windows/blob/master/scikit-sparse-0.4.3/setup.py
and switch it with setup.py of the 0.4.4 version

After that, follow this tutorial
https://github.com/xmlyqing00/Cholmod-Scikit-Sparse-Windows

Documentation
https://scikit-sparse.readthedocs.io/en/latest/overview.html
'''

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

		'''
		dir(Ls)
		Ls.L()

		print(vars(b))
		print(vars(b.data))
		print(b.data.size)
		'''

		# sparse_cholesky execution
		start = time.process_time()
		Ls = cholesky(A)
		end = time.process_time()
		row['chol'] = str(1000* (end - start))
		print("Time execution of sparse cholesky: " + str(1000* (end - start)), " ms")
		print('\n')

		start = time.process_time()
		x = Ls(b) # solves the equation Ax=b

		'''
		print(np.allclose(Ls.L().todense(), np.tril(Ls.L().todense()))) # check if lower triangular
		print(np.allclose(Ls.L().T.todense(), np.triu(Ls.L().T.todense()))) # check if upper triangular
		y = splinalg.spsolve_triangular(sparse.csr_matrix(Ls.L()), b, lower=True)
		x = splinalg.spsolve_triangular(sparse.csr_matrix(Ls.L().T), y, lower=False)
		'''
		
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
	except Exception as e:
		print(e)



# @profile
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