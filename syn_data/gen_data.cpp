#include <fstream>
#include <iostream>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <random>

int main()
{
    gsl_rng * r;
    const gsl_rng_type * T;

    gsl_rng_env_setup();

    T = gsl_rng_default;
    r = gsl_rng_alloc (T);

    // printf ("generator type: %s\n", gsl_rng_name (r));
    // printf ("seed = %lu\n", gsl_rng_default_seed);
    // printf ("first value = %lu\n", gsl_rng_get (r));

    int k = 3; // k is the # of communities
    const double alpha = double (1.0) / k;
    // printf ("k = %d and alpha = %f\n", k, alpha);

    double eta = 1; // eta is the hpyerparameter of the Beta istribution
    double comm_str [k];
    for (uint32_t i = 0; i < k; ++i)
        comm_str[i] = gsl_ran_beta(r, eta, eta);

    // for (uint32_t i = 0; i < k; ++i)
    //     printf ("%f\n", comm_str[i]);

    int n = 100; // Number of nodes
    double theta = 1; // Used for gsl_ran_dirichlet

    double alpha_array [k]; // Array for gsl_ran_dirichlet
    for (uint32_t i = 0; i < k; ++i)
        alpha_array[i] = alpha;

    double pi [n][k]; // Array to store pi

    // Populate pi
    for (uint32_t i = 0; i < n; ++i)
        gsl_ran_dirichlet(r, k, alpha_array, pi[i]);

    // Convert to binary; TODO: using sampling
    for (uint32_t i = 0; i < n; ++i){
        for (uint32_t j = 0; j < k ; ++j){
            if (pi[i][j] > 0.5){
                pi[i][j] = 1;
            }
            else{
                pi[i][j] = 0;
            }
        }
    }

    // for (uint32_t i = 0; i < n; ++i){
    //     for (uint32_t j = 0; j < k ; ++j){
    //         printf("%d, %d, %f\n", i, j ,pi[i][j]);
    //     }
    // }

    double mean = 0.0; // Set mean
    double var = 1; // Set var
    double prob = 0.5; // Set probability for Bernoulli

    // Save input values
    std::ofstream inputs ("inputs.txt");
    if (inputs.is_open()){
        inputs << "k = " << k << "\n";
        inputs << "alpha = " << alpha << "\n";
        inputs << "eta = " << eta << "\n";
        inputs << "mean = " << mean << "\n";
        inputs << "var = " << var << "\n";
        inputs << "prob = " << prob << "\n";
        inputs << "comm_str = ";
        for (uint32_t i = 0; i < k; ++i)
            inputs << comm_str[i] << " ";
        inputs << "\n" << "n = " << n << "\n" << "pi = " << "\n";
        for (uint32_t i = 0; i < n; ++i){
            for (uint32_t j = 0; j < k ; ++j){
                inputs << pi[i][j] << "\t";
            }
            inputs << "\n";
        }
        inputs.close();
    }

    // Save attribute matrix
    std::ofstream attributes ("attributes.txt");
    if (attributes.is_open()){
        for (uint32_t i = 0; i < n; ++i){
                attributes << gsl_ran_gaussian(r, var) << "\t";
                attributes << gsl_ran_gaussian(r, var) << "\t";
                attributes << gsl_ran_bernoulli(r, prob) << "\t";
                attributes << gsl_ran_bernoulli(r, prob) << "\t";
                attributes << "\n";
        }
    attributes.close();
    }

    int num_edge = 2000; // Define number of edges
    double epsilon = 0.2;
    int adj_matrix [n][n];

    // Populate adjancency matrix with 0s
    for (uint32_t i = 0; i < n; ++i)
        for (uint32_t j = 0; j < n ; ++j)
            adj_matrix[i][j] = 0;

    int count = 0;
    while (count < num_edge){
        int run_eps = 1;
        // printf("count %d\n", count);
        int a = gsl_rng_uniform_int(r, n);
        int b = gsl_rng_uniform_int(r, n);
        // printf("%d, %d\n", a, b);
        if (a == b){
            continue;
        }

        for (uint32_t j = 0; j < k ; ++j){
            if (pi[a][j] == pi[b][j]){
                int x = gsl_ran_bernoulli(r, comm_str[j]);
                // printf("Match 1 %d\n", x);
                if (x == 1){
                    if (adj_matrix[a][b])
                        continue;
                    else
                        adj_matrix[a][b] = 1;
                        run_eps = 0;
                        ++count;
                        continue;
                    }
                }

        if (run_eps == 1){
            int x = gsl_ran_bernoulli(r, epsilon);
            // printf("0 %d\n", x);
            if (x == 1){
                if (adj_matrix[a][b])
                        continue;
                    else
                        adj_matrix[a][b] = 1;
                        ++count;
                        continue;
                }
            }
        }
    }

    std::ofstream matrix ("matrix.txt");
    if (matrix.is_open()){
        for (uint32_t i = 0; i < n; ++i){
            for (uint32_t j = 0; j < n ; ++j){
                matrix << adj_matrix [i][j] << "\t";
            }
            matrix << "\n";
        }
    matrix.close();
    }
}
