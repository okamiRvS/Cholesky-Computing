#include "../../include/Eigen/Sparse"
#include "../../include/Eigen/SparseCholesky"
#include "../../include/matrixParser/sparseMatrixMarket.h"

#include <string>
#include <iostream>
#include <chrono>
#include <dirent.h>
#include <sys/types.h>

bool hasEnding(std::string const &fullString, std::string const &ending)
{
    if (fullString.length() >= ending.length())
    {
        return (0 == fullString.compare(fullString.length() - ending.length(), ending.length(), ending));
    }
    else
    {
        return false;
    }
}

int main(int argc, char *argv[])
{
    std::string path;
    struct dirent *entry;

    if (argc == 1)
    {
        path = "./data";
    }
    else if (argc == 2)
    {
        path = argv[1];
    }
    else
    {
        std::cout << "Too many arguments." << std::endl;
        return 0;
    }

    DIR *dir = opendir(path.c_str());
    if (dir == NULL)
    {
        return 0;
    }

    std::chrono::_V2::system_clock::time_point t1;
    std::chrono::_V2::system_clock::time_point t2;
    int64_t duration;

    while ((entry = readdir(dir)) != NULL)
    {
        if (hasEnding(entry->d_name, ".mtx"))
        {
            std::string mtxFile = path + "/" + entry->d_name;
            std::cout << entry->d_name << std::endl;

            // Import
            t1 = std::chrono::high_resolution_clock::now();
            Eigen::SparseMatrix<double> spMatrix = readMatrix(mtxFile);
            t2 = std::chrono::high_resolution_clock::now();
            duration = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
            std::cout << "Import:" << '\t' << '\t' << duration << " ms" << std::endl;

            std::cout << "rows:" << '\t' << '\t' << spMatrix.rows() << std::endl;
            std::cout << "cols:" << '\t' << '\t' << spMatrix.cols() << std::endl;
            std::cout << "nonZeros:" << '\t' << spMatrix.nonZeros() << std::endl;
            std::cout << "size:" << '\t' << '\t'
                      << (spMatrix.outerSize() + spMatrix.nonZeros() + 1) * 4 +
                          (spMatrix.nonZeros() * 8) 
                      << " byte" << std::endl;

            // Cholesky decomposition
            t1 = std::chrono::high_resolution_clock::now();
            Eigen::SimplicialLLT<Eigen::SparseMatrix<double>> chol(spMatrix);
            t2 = std::chrono::high_resolution_clock::now();
            duration = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
            std::cout << "Chol:" << '\t' << '\t' << duration << " ms" << std::endl;
            std::cout << "Chol size:" << '\t'
                      << (chol.matrixL().nestedExpression().outerSize() + chol.matrixL().nestedExpression().nonZeros() + 1) * 4 +
                          (chol.matrixL().nestedExpression().nonZeros() * 8)
                      << " byte" << std::endl;

            // Relative error
            Eigen::VectorXd x(spMatrix.rows());
            x.setOnes();
            Eigen::VectorXd b = spMatrix * x;

            t1 = std::chrono::high_resolution_clock::now();
            Eigen::VectorXd xChol = chol.solve(b);
            t2 = std::chrono::high_resolution_clock::now();
            duration = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
            std::cout << "Sol time:" << '\t' << duration << " ms" << std::endl;

            std::cout << "err:" << '\t' << '\t' << (xChol - x).norm() / x.norm() << std::endl
                      << std::endl;
        }
    }

    return 0;
}
