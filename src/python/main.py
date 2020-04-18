import pdb
import sys
import scipy.io
import scipy.sparse
from scipy.sparse import linalg as splinalg
from scipy import array, linalg, dot
import pandas as pd
print(pd.__version__)
import numpy as np
import pdb

# https://en.wikipedia.org/wiki/Path_(computing)
# https://gist.github.com/Puriney/98544b779bcb815926f7acf87f537e61
# https://github.com/benfred/implicit/blob/master/benchmarks/benchmark_als.py

# Read in mtx file by scipy
coo_mat = scipy.io.mmread('../../data/ex15.mtx')

# Scipy matrix in coo layout can be easily converted to other types: csr and csc.
# csr_mat = coo_mat.tocsr(copy=True)
csc_mat = coo_mat.tocsc()
print(csc_mat)

print("\n")	

# Default is upper-triangular
L = linalg.cholesky(csc_mat.todense(), lower=True)
print(L)

'''
# csr to Pandas sparse data frame
sp_df = pd.SparseDataFrame(csr_mat)#.fillna(0)
print(sp_df)

sp_df = pd.SparseDataFrame(csr_mat).fillna(0)
print(sp_df)

'''