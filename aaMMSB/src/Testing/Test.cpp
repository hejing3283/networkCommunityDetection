// #include <iostream>
// #include <eigen3/Eigen/Core>
// #include <vector>
// #include "matrix.hh"

// int main()
// {

//     uint32_t k = 3;
//     const uint32_t _k = k;
//     // std::cout << typeid(_k).name() << "\n";
//     Eigen::Matrix<double, 3, 1> phi_1;
//     // Eigen::Matrix<double, 1, 1> m;
//     // m<<1;
//     // int a =m;
//     // cout <<a;
//     phi_1 << 2.0, 2.0, 2.0;

//     Eigen::Matrix<double, 3, 1> phi_2 = 1.0 / phi_1;



//     // Eigen::Matrix<double, 3, 3> phi_2;
//     // phi_1 << 0, 0, 0, 0, 0, 0, 0, 0, 0;
//     // std::cout << phi_1 << "\n";
//     // double x = phi_1.transpose() * phi_1;
//     // std::cout << x << "\n";
//     printf("Good\n");


//     // Eigen::MatrixXd eta_g_top = Eigen::MatrixXd::Zero(3);
//     // Eigen::MatrixXd a2 = Eigen::MatrixXd::Zero(3, 1);

//     // std::vector<int> v = {7, 5, 16, 8};

//     // std::vector<double> phi (4,1);
//     // (Eigen::Matrix) v;

//     // // Eigen::Array<double, 3, 1> phi_2;
//     // // phi_2 << 1.0, 1.0, 1.0;

    // // Eigen::Array<double, 3, 1> phi_3 = 3 * (phi_1 + phi_2);

    // // for (uint32_t i = 0; i < 3; ++i)
    //     // printf("%f ", phi_3[i]);

    // // Eigen::ArrayXf phi_3 = phi_1 + phi_2;

    // Eigen::Matrix<double, 3, 3>  Test = phi_1.asDiagonal();

    // for (uint32_t i = 0; i < 3; ++i){
    //     for (uint32_t j = 0; j < 3; ++j){
    //         printf("%f ", Test(i,j));
    //     }
    // }
    // printf("%f", pow(2,2));
// }

// #include "stdafx.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "optimization.h"

using namespace alglib;

void function1_grad(const real_1d_array &x, double &func, real_1d_array &grad, void *ptr)
{
    //
    // this callback calculates f(x0,x1) = 100*(x0+3)^4 + (x1-3)^4
    // and its derivatives df/d0 and df/dx1
    //
    func = 100*pow(x[0]+3,4) + pow(x[1]-3,4);
    for (uint32_t i = 2; i<5; ++i)
      func += 100*pow(x[i]+3,4) + pow(x[i]-3,4);
    grad[0] = 400*pow(x[0]+3,3);
    grad[1] = 4*pow(x[1]-3,3);
}

int main(int argc, char **argv)
{
    //
    // This example demonstrates minimization of f(x,y) = 100*(x+3)^4+(y-3)^4
    // using LBFGS method.
    //
    real_1d_array x = "[0,0]";
    double epsg = 0.0000000001;
    double epsf = 0;
    double epsx = 0;
    ae_int_t maxits = 0;
    minlbfgsstate state;
    minlbfgsreport rep;

    minlbfgscreate(1, x, state);
    minlbfgssetcond(state, epsg, epsf, epsx, maxits);
    alglib::minlbfgsoptimize(state, function1_grad);
    minlbfgsresults(state, x, rep);

    printf("%d\n", int(rep.terminationtype)); // EXPECTED: 4
    printf("%s\n", x.tostring(2).c_str()); // EXPECTED: [-3,3]
    return 0;
}

