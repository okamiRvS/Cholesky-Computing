library("Matrix")

# https://www.r-bloggers.com/5-ways-to-measure-running-time-of-r-code/

# set workspace path
# setwd("../../git/cholesky-computing/src/r")

matrix <- readMM("../../data/ex15.mtx")  

start <- Sys.time()

# https://www.rdocumentation.org/packages/Matrix/versions/1.2-18/topics/chol

cholesky <- tryCatch(
  {
    Matrix::chol(matrix)
  },
  error = function(e){
    print(e) # if matrix is not positive definite or symmetric, an error is signalled.
  },
  warning = function(w) {
    print(w) # not positive definite matrix warning
  }
)

end <- Sys.time()
time <- end - start
time

print(cholesky)

