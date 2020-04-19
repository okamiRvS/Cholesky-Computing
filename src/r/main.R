library("Matrix")


#https://www.r-bloggers.com/5-ways-to-measure-running-time-of-r-code/

# set workspace path
# setwd("~/git/cholesky-computing/src/r")

matrix = readMM("../../data/ex15.mtx")  

#https://www.rdocumentation.org/packages/Matrix/versions/1.2-18/topics/chol
c = chol(matrix)
#print(c)
