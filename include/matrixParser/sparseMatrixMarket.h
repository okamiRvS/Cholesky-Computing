#include <string>
#include "../../include/Eigen/Sparse"

typedef Eigen::Triplet<double> T;

class sparseMatrixMarket
{
private:
    int _rows, _cols, _nonzeros;
    Eigen::SparseMatrix<double> _matrixMarket;

public: 
    sparseMatrixMarket(std::string &filename);
    void readMatrix(std::string &filename);
    Eigen::SparseMatrix<double> & matrixMarket();
    int rows();
    int cols();
    int nonzeros();
};