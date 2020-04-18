#include "../../include/Eigen/Sparse"
#include "../../include/Eigen/SparseCholesky"
#include "../../include/matrixParser/sparseMatrixMarket.h"

#include <string>
#include <iostream>
#include <chrono>

int main() {

    std::string filename = "./data/ex15.mtx";
    sparseMatrixMarket spMatrix(filename);

    auto t1 = std::chrono::high_resolution_clock::now();
    Eigen::SimplicialLLT<Eigen::SparseMatrix<double>> chol(spMatrix.matrixMarket());
    auto t2 = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>( t2 - t1 ).count();
    std::cout << duration/1000.0 << " ms";

    return 0;
}
