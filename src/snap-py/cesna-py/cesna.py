import argparse
import os
import sys
sys.path.append("swig")

from snap import *
# from models import CesnaModel

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Input/output files related arguments
    parser.add_argument('-o', '--out-prefix', help='Output file prefix', default='')
    parser.add_argument('-e', '--edges', help='Input edgelist file name', default='./data/1912/1912.edges')
    parser.add_argument('-a', '--attribs', help='Input node attribute file name', default='./data/1912/1912.nodefeat')
    parser.add_argument('-n', '--attrib-names', help='Input file name for the names of attributes', default='./data/1912/1912.nodefeatnames')

    # Hyperparameters for the CESNA model
    parser.add_argument('--num-coms', help='Number of communities to detect. Detected automatically if 0', type=int, default=0)
    parser.add_argument('--min-coms', help='Smallest number of communities to try', type=int, default=3)
    parser.add_argument('--max-coms', help='Largest number of communities to try', type=int, default=20)
    parser.add_argument('--attr-weight', help='Relative importance of the feature-related log-likelihood', type=float, default=0.5)
    parser.add_argument('--reg', help='Regularization parameter for the logistic weights', type=float, default=1)
    parser.add_argument('--alpha', help='Alpha parameter for the backtracking line search', type=float, default=0.05)
    parser.add_argument('--beta', help='Beta parameter for the backtracking line search', type=float, default=0.3)

    args = parser.parse_args()

    G = LoadEdgeList(PUNGraph, args.edges, 0, 1)
    G.Dump()

    
    # G = UndirectedGraph(args.edges, args.attribs, args.attrib_names)
    # M = CesnaModel(G, args.num_coms, args.min_coms, args.max_coms, args.attr_weight,
    #                args.reg, args.alpha, args.beta)

