#include <string>
#include <iostream>
#include <fstream>

#include "../../include/matrixParser/sparseMatrixMarket.h"

Eigen::SparseMatrix<double> readMatrix(std::string &filename)
{
    // Vector of sparse matrix triplets
    std::vector<T> tripletList;

    Eigen::SparseMatrix<double> matrixOut;
    int rows;
    int cols;
    int nonzeros;

    std::vector<double> T_element;
    std::ifstream infile;
    bool bDimRow = true;
    bool bIsSymmetric = false;
    std::string line;
    infile.open(filename);

    while (std::getline(infile, line))
    {
        if (line[0] == '%')
        {   // Metadata
            if (line[1] == '%' & line.find("symmetric") != std::string::npos) 
            {   // Check if matrix is symmetric
                bIsSymmetric = true;
            }
        }
        else
        {
            std::istringstream iss(line);
            std::string token;
            while (std::getline(iss, token, ' '))
            {
                T_element.push_back(std::stod(token));
            }
            if (bDimRow)
            {
                rows = trunc(T_element[0]);
                cols = trunc(T_element[1]);
                nonzeros = trunc(T_element[2]);
                if (bIsSymmetric) 
                {
                    tripletList.reserve(2 * nonzeros - 3 * rows);
                } else {
                    tripletList.reserve(nonzeros);
                }             
                bDimRow = false;
            }
            else
            {
                if (T_element[2] != 0)
                {
                    tripletList.push_back(T(T_element[0] - 1, T_element[1] - 1, T_element[2]));
                    if (bIsSymmetric && T_element[0] != T_element[1])
                    {
                        tripletList.push_back(T(T_element[1] - 1, T_element[0] - 1, T_element[2]));
                    }
                }
            }
            T_element.clear();
        }
    }
    matrixOut.resize(rows, cols);
    matrixOut.setFromTriplets(tripletList.begin(), tripletList.end());

    return matrixOut;
}
