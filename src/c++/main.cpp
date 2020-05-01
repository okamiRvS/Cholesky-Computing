#include "../../include/Eigen/Sparse"
#include "../../include/Eigen/SparseCholesky"
#include "../../include/matrixParser/sparseMatrixMarket.h"

#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include <dirent.h>
#include <sys/types.h>
#include <cstdio>
#include <ctime>

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
    std::ofstream outCSV;

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

    std::time_t rawtime;
    std::tm* timeinfo;
    char buffer [80];

    std::time(&rawtime);
    timeinfo = std::localtime(&rawtime);

    std::strftime(buffer,80,"%Y-%m-%d-%H-%M-%S",timeinfo);
    std::puts(buffer);
    std::string time(buffer);

    outCSV.open("Results_" + time + ".csv");
    outCSV << "program,name,import,rows,cols,nonZeros,size,chol,chol_size,sol_time,err\n";

    while ((entry = readdir(dir)) != NULL)
    {
        if (hasEnding(entry->d_name, ".mtx"))
        {
            std::string mtxFile = path + "/" + entry->d_name;

            outCSV << "C++,";
            std::cout << entry->d_name << std::endl;
            outCSV << entry->d_name << ",";

            // Import
            t1 = std::chrono::high_resolution_clock::now();
            Eigen::SparseMatrix<double> spMatrix = readMatrix(mtxFile);
            t2 = std::chrono::high_resolution_clock::now();
            duration = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
            outCSV << duration << ",";
            std::cout << "Import:" << '\t' << '\t' << duration << " ms" << std::endl;

            outCSV << spMatrix.rows() << ",";
            std::cout << "rows:" << '\t' << '\t' << spMatrix.rows() << std::endl;
            outCSV << spMatrix.cols() << ",";
            std::cout << "cols:" << '\t' << '\t' << spMatrix.cols() << std::endl;
            outCSV << spMatrix.nonZeros() << ",";
            std::cout << "nonZeros:" << '\t' << spMatrix.nonZeros() << std::endl;
            outCSV << (spMatrix.outerSize() + spMatrix.nonZeros() + 1) * 4 +
                          (spMatrix.nonZeros() * 8)  << ",";
            std::cout << "size:" << '\t' << '\t'
                      << (spMatrix.outerSize() + spMatrix.nonZeros() + 1) * 4 +
                          (spMatrix.nonZeros() * 8) 
                      << " byte" << std::endl;

            // Cholesky decomposition
            t1 = std::chrono::high_resolution_clock::now();
            Eigen::SimplicialLLT<Eigen::SparseMatrix<double>> chol(spMatrix);
            t2 = std::chrono::high_resolution_clock::now();
            duration = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
            outCSV << duration << ",";
            std::cout << "Chol:" << '\t' << '\t' << duration << " ms" << std::endl;
            outCSV << (chol.matrixL().nestedExpression().outerSize() + chol.matrixL().nestedExpression().nonZeros() + 1) * 4 +
                          (chol.matrixL().nestedExpression().nonZeros() * 8) << ",";
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
            outCSV << duration << ",";
            std::cout << "Sol time:" << '\t' << duration << " ms" << std::endl;

            double error = (xChol - x).norm() / x.norm();
            outCSV << error << "\n";
            std::cout << "err:" << '\t' << '\t' << error << std::endl
                      << std::endl;
        }
    }

    return 0;
}
