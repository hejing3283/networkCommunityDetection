import pystan
import numpy as np
import matplotlib as plt

cesna_code = """
data {
    // To do once figure out how data is formatted
}
parameters {
    real W[K][C];
    real F[U][C];
}
transformed parameters {
    real Q[I][K];
    real X[I][K];
    real lg_G[I][J];
    real lg_X[I][K];
    for (i in 1:I)
        for (k in 1:K)
            Q[i][k] = \\ To figure out how to sum properly
    for (i in 1:I)
        for (k in 1:K)
            X[i][k] = Q[i][k](1 - Q[i][k])
    for (i in 1:I)
        for (j in 1:J)
            lg_G[i][j] = log(1 - exp(F[i][c] * F[j][c])) - (F[i][c] * F[j][c]) \\ Not sure of log and exp
    for (i in 1:I)
        for (k in 1:K)
            lg_X[i][k] = X[i][k]log(Q[i][k] + (1 - X[i][k]) * log(1 - Q[i][k]) \\ Not sure of exp
}
model {
    \\ To figure out once data is completed
}
