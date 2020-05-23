library(spam)
library(spam64)
library(Matrix)

# set workspace path
# setwd("../../git/cholesky-computing/src/r")

# read matrixes in data
matrixes = list.files(path='../../data')

for (mat in matrixes) {
  # clear memory
  rm(list=ls()[! ls() %in% c("matrixes","mat")])
  gc();
  
  # Get matrix info
  name <- mat
  i <- Sys.time()
  A <- read.MM(paste("../../data/", name, sep = ""))
  imp_t <- as.numeric(difftime(Sys.time(), i, units = "secs")[[1]])*1000
  a_size <- object.size(A)
  nrow <- nrow(A)
  ncol <- ncol(A)
  nonZ <- Matrix::nnzero(A)

  # find b for x to be [1, 1, ..., 1]
  xe <- rep(1, 1, ncol(A))
  b <- as.spam(A %*% xe)
  
  # Cholesky decomposition
  i2 <- Sys.time()
  R <- tryCatch(
    {
      chol.spam(A)
    },
    error = function(e){
      print(name)
      print(e) # if matrix is not positive definite or symmetric, an error is signalled.
    }
  )
  if(inherits(R, "error")) next;  # skip to next matrix if error occours
  
  chol_t <- as.numeric(difftime(Sys.time(), i2, units = "secs")[[1]])*1000
  r_size <- object.size(R)
  
  # solve the linear system
  i3 = Sys.time()
  x <- solve.spam(R,b)
  solve_t = as.numeric(difftime(Sys.time(), i3, units = "secs")[[1]])*1000
  
  # relative error
  err <-  norm(x - xe, type = "2") / norm(xe, type = "2")

  df <- data.frame(program = c("R"),
                   name = c(name),
                   import = c(imp_t),
                   rows = c(nrow),
                   cols = c(ncol),
                   nonZeros = c(nonZ),
                   size = c(a_size),
                   chol = c(chol_t),
                   chol_size = c(r_size),
                   sol_time = c(solve_t),
                   err = c(err))
  colnames(df) <- c('program', 'name', 'import','rows', 'cols', 'nonZeros','size', 'chol', 'chol_size', 'sol_time', 'err');
  write.table(df, "results.csv", sep = ",", col.names = !file.exists("results.csv"), row.names = FALSE, append=TRUE, quote = FALSE)
}

