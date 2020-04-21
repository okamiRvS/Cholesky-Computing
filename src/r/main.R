library("Matrix")

# set workspace path
# setwd("../../git/cholesky-computing/src/r")

# read matrix

A <- readMM("../../data/ex15.mtx")

# find b for x to be [1, 1, ..., 1]

xe <- matrix(1, 1, ncol(A))
b <- xe %*% A

# Cholesky decomposition
# https://www.rdocumentation.org/packages/Matrix/versions/1.2-18/topics/chol

R <- tryCatch(
  {
    Matrix::chol(A)
  },
  error = function(e){
    print(e) # if matrix is not positive definite or symmetric, an error is signalled.
  },
  warning = function(w) {
    print(w) # not positive definite matrix warning
  }
)

# solve the linear system
# R is upper triangular, so i can apply backward substitution
# https://stat.ethz.ch/R-manual/R-devel/library/base/html/backsolve.html

y <- backsolve(R, b, nrow(b))

x <- forwardsolve(t(R), y)

# relative error
# https://www.rdocumentation.org/packages/pracma/versions/1.9.9/topics/Norm

err <-  norm(x - xe, type = "2") / norm(xe, type = "2")
