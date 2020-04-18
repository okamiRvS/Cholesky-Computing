#include <string>
#include "../../include/Eigen/Sparse"

typedef Eigen::Triplet<double> T;

class sparseMatrixMarket
{
private:
    int rows, cols, nonzeros;
    Eigen::SparseMatrix<double> _matrixMarket;

public:
    std::string url, name, author;   
    sparseMatrixMarket(std::string &filename);
    void readMatrix(std::string &filename);
    Eigen::SparseMatrix<double> matrixMarket();
};