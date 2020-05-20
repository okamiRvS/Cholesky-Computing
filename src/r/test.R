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
  i <- Sys.time()
  name <- mat
  A <- read.MM(paste("../../data/", name, sep = ""))
  a_size <- object.size(A)
  nrow <- nrow(A)
  ncol <- ncol(A)
  nonZ <- Matrix::nnzero(A)
  imp_t <- Sys.time() - i
  
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
  
  chol_t <- Sys.time() - i2
  r_size <- object.size(R)
  
  # solve the linear system
  i3 = Sys.time()
  x <- solve.spam(R,b)
  solve_t = Sys.time() - i3
  
  # relative error
  err <-  norm(x - xe, type = "2") / norm(xe, type = "2")
  
  # comment
  if(FALSE) {
    textfile=file.path("R_results.txt");
    printer = file(textfile,"a+");
    write(name, textfile, append=TRUE);
    write(
      c("Import:", as.numeric(imp_t) * 1000,
        "rows:", nrow, 
        "cols:", ncol,
        "nonZeros:", nonZ,
        "size:", a_size,
        "Chol:", as.numeric(chol_t * 1000),
        "sol_time:" = as.numeric(solve_t * 1000),
        "Chol size:", r_size,
        "err:", err),
      textfile, sep = "\t\t\t",append = TRUE, ncolumns = 2);
    write("\n", textfile, append=TRUE);
    close(printer)
  }
  
  sol_time = c(as.numeric(solve_t * 1000))
  
  df <- data.frame(program = c("R"),
                   name = c(name),
                   import = c(as.numeric(imp_t) * 1000),
                   rows = c(nrow),
                   cols = c(ncol),
                   nonZeros = c(nonZ),
                   size = c(a_size),
                   chol = c(as.numeric(chol_t * 1000)),
                   chol_size = c(r_size),
                   sol_time = c(as.numeric(solve_t * 1000)),
                   err = c(err))
  colnames(df) <- c('program', 'name', 'import','rows', 'cols', 'nonZeros','size', 'chol', 'chol_size', 'sol_time', 'err');
  write.table(df, "results2.csv", sep = ",", col.names = !file.exists("results2.csv"), row.names = FALSE, append=TRUE, quote = FALSE)
}

