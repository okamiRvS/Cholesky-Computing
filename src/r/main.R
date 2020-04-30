library("spam", "spam64")

# set workspace path
# setwd("../../git/cholesky-computing/src/r")

# read matrix

i <- Sys.time()
A <- read.MM("../../data/ex15.mtx")
name <- "ex15.mtx" # change matrix name
a_size <- object.size(A)
nrow <- nrow(A)
ncol <- ncol(A)
nonZ <- nnzero(A)
imp_t <- Sys.time() - i

# find b for x to be [1, 1, ..., 1]

xe <- rep(1, 1, ncol(A))
b <-  as.spam(A %*% xe)

# Cholesky decomposition
i2 <- Sys.time()
R <- tryCatch(
  {
    chol.spam(A)
  },
  error = function(e){
    print(e) # if matrix is not positive definite or symmetric, an error is signalled.
  }
)
chol_t <- Sys.time() - i2
r_size <- object.size(R)

# solve the linear system
i3 = Sys.time()
x <- solve.spam(R,b)
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