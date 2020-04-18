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
    std::string line;
    infile.open(filename);
    while (std::getline(infile, line))
    {
        if (line[0] == '%')
        { // Metadata
            // do something
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
                this->rows = trunc(T_element[0]);
                this->cols = trunc(T_element[1]);
                this->nonzeros = trunc(T_element[2]);
                tripletList.reserve(nonzeros);
                bDimRow = false;
            }
            else
            {
                tripletList.push_back(T(T_element[0] - 1, T_element[1] - 1, T_element[2]));
            }
            T_element.clear();
        }
    }
    this->_matrixMarket.resize(rows, cols);
    this->_matrixMarket.setFromTriplets(tripletList.begin(), tripletList.end());
}

Eigen::SparseMatrix<double> sparseMatrixMarket::matrixMarket()
{
    return this->_matrixMarket;
}
