#include <string>
#include <iostream>
#include <fstream>

#include "../../include/matrixParser/sparseMatrixMarket.h"

sparseMatrixMarket::sparseMatrixMarket(std::string &filename)
{
    readMatrix(filename);
}

void sparseMatrixMarket::readMatrix(std::string &filename)
{
    // Vector of sparse matrix triplets
    std::vector<T> tripletList;

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
                this->_rows = trunc(T_element[0]);
                this->_cols = trunc(T_element[1]);
                this->_nonzeros = trunc(T_element[2]);
                if (bIsSymmetric) 
                {
                    tripletList.reserve(2 * this->_nonzeros - 3 * this->_rows);
                } else {
                    tripletList.reserve(this->_nonzeros);
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
    this->_matrixMarket.resize(this->_rows, this->_cols);
    this->_matrixMarket.setFromTriplets(tripletList.begin(), tripletList.end());
}

Eigen::SparseMatrix<double> & sparseMatrixMarket::matrixMarket()
{
    return this->_matrixMarket;
}

int sparseMatrixMarket::rows()
{
    return this->_rows;
}

int sparseMatrixMarket::cols()
{
    return this->_cols;
}

int sparseMatrixMarket::nonzeros()
{
    return this->_nonzeros;
}