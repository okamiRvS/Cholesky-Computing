#include <string>
#include "../../include/Eigen/Sparse"

typedef Eigen::Triplet<double> T;
Eigen::SparseMatrix<double> readMatrix(std::string &filename);
