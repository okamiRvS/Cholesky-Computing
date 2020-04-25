library("Matrix", "pryr")

# set workspace path
# setwd("../../git/cholesky-computing/src/r")

# read matrix

A <- readMM("../../data/ex15.mtx")
m_i <- pryr::mem_used()
# find b for x to be [1, 1, ..., 1]

xe <- rep(1, 1, ncol(A))
b <-  A %*% xe  

# Cholesky decomposition

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
s <- Sys.time()

y <- Matrix::solve(t(R), b)
x <- Matrix::solve(R, y)

timing <- Sys.time() - s 
m_f <- pryr::mem_used()
mem <- m_f - m_i

# relative error

err <-  norm(x - xe, type = "2") / norm(xe, type = "2")
