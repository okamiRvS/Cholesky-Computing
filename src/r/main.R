library("Matrix")

# https://www.r-bloggers.com/5-ways-to-measure-running-time-of-r-code/

# set workspace path
# setwd("~/git/cholesky-computing/src/r")

matrix = readMM("../../data/ex15.mtx")  

# start = Sys.time()

# https://www.rdocumentation.org/packages/Matrix/versions/1.2-18/topics/chol
c = Matrix::chol(matrix)
# if matrix is not positive definite, an error is signalled.

# end = Sys.time()
# time = end - start

