#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <iostream>
#include "matrix.h"

typedef std::vector<int> IntVector;
typedef std::vector<IntVector> IntVector2D;

typedef std::vector<float> DoubleVector;
typedef std::vector<DoubleVector> DoubleVector2D;

using namespace std;

int ApplyRand(int num)
{ return num + rand() - RAND_MAX/2; }

void OutputMatrix(const IntVector2D& m)
{
    cout << "\n";
    IntVector2D::const_iterator it = m.begin();
    while (it != m.end())
    {
        copy(it->begin(), it->end(), ostream_iterator<int>(cout, " "));
        cout << "\n";
        ++it;
    }
}

void OutputMatrix(const DoubleVector& m)
{
    cout << "\n";
    IntVector2D::const_iterator it = m.begin();
    while (it != m.end())
    {
        copy(it->begin(), it->end(), ostream_iterator<int>(cout, " "));
        cout << "\n";
        ++it;
    }
}


int main()
{
    IntVector2D matrix;
    ifstream pFile("../../dat/attributes_bin.txt");
    string s;

    while ( std::getline(pFile, s) )
    {
        // create empty row on back of matrix
        matrix.push_back(IntVector());
        IntVector& vBack = matrix.back();

        // create an istringstream to parse
        istringstream ss(s);

        // parse the data, adding each number to the last row of the matrix
        copy(istream_iterator<int>(ss), istream_iterator<int>(), back_inserter(vBack));
    }
    DoubleVector2D matrix2;
    std::ifstream f("../../dat/attributes_gau.txt");
       std::string l;
       std::vector<std::vector<double> > rows;
       while(std::getline(f, l)) {
           std::stringstream s(l);
           double d1;
           double d2;
           if(s >> d1 >> d2) {
               std::vector<double> row;
                row.push_back(d1);
                row.push_back(d2);
                rows.push_back(row);
            }
        }

        for(int i = 0; i < rows.size(); ++i)
            std::cout << rows[i][0] << " " << rows[i][1] << '\n';

    // output the matrix
    OutputMatrix(matrix);
    OutputMatrix(matrix2);

}
