library("Matrix")

# set workspace path
# setwd("../../git/cholesky-computing/src/r")

A <- readMM("../../data/ex15.mtx")

# find b 
xe <- matrix(1, 1, ncol(A))
b <- xe %*% A


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

RRt <- R %*% t(R)
x <- as.vector(solve(RRt,t(b)))

# https://www.rdocumentation.org/packages/pracma/versions/1.9.9/topics/Norm
# relative error
err <-  norm(x - xe, type = "2") / norm(xe, type = "2")
