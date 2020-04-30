library("Matrix", "pryr")

# set workspace path
# setwd("../../git/cholesky-computing/src/r")

# read matrix

i <- Sys.time()
A <- readMM("../../data/ex15.mtx")
name <- "apache2.mtx"
a_size <- object.size(A)
nrow <- nrow(A)
ncol <- ncol(A)
nonZ <- nnzero(A)
imp_t <- Sys.time() - i

# find b for x to be [1, 1, ..., 1]

xe <- rep(1, 1, ncol(A))
b <-  A %*% xe  

# Cholesky decomposition
i2 <- Sys.time()
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
chol_t <- Sys.time() - i2
r_size <- object.size(R)

# solve the linear system
i3 = Sys.time()
y <- Matrix::solve(t(R), b)
x <- Matrix::solve(R, y)
solve_t = Sys.time() - i3

# relative error

err <-  norm(x - xe, type = "2") / norm(xe, type = "2")


textfile=file.path("R_results.txt");
printer = file(textfile,"a+");
write(name, textfile, append=TRUE);
write(c("Import: \t", imp_t, "rows: \t", nrow, 
        "cols: \t", ncol, "nonZeros: \t", nonZ,
        "size: \t", a_size, "Chol: \t", chol_t,
        "Chol size: \t", r_size, "err: \t", err), textfile, sep = " ",append = TRUE, ncolumns = 2);
write("\n", textfile, append=TRUE)
close(printer)