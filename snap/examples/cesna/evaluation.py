# evaluation metric for CESNA

import os
import sys
import numpy as np
from sklearn import metrics

def compute_jaccard_index(set_1, set_2):
	n = len(set_1.intersection(set_2))
	return n / (float(len(set_1) + len(set_2) - n))


def Precision(C_Star, C):
    intersect = len(set.intersection(C_Star, C))
    total_C = len(C)
    return float(intersect) / total_C

def Recall(C_Star, C):
    intersect = len(set.intersection(C_Star, C))
    total_C_Star = len(C_Star)
    return float(intersect) / total_C_Star

def F1(C_Star, C):
    Prec = Precision(C_Star, C)
    Rec = Recall(C_Star, C)
    try:
    	return 2 * Prec * Rec / (Prec + Rec)
    except ZeroDivisionError:
    	return 0


def run_evaluation(weights_f, comm_f, truth_f, similarity_function):
	best = [(0, 0)]*5
	for i in range(3, 35):
		os.system('./cesna -c:%d -o:out/' % i)

		weights_file = open(weights_f, 'r')
		comm_file = open(comm_f, 'r')
		truth_file = open(truth_f, 'r')

		comms = []
		for line in comm_file:
			comms.append(set(line.strip().split()))

		truths = []
		for line in truth_file:
			truths.append(set(line.strip().split()[1:]))

		weights_file.close()
		comm_file.close()
		truth_file.close()

		sum_truths = 0.0
		sum_comms = 0.0

		for comm in comms:
			sum_comms += max([similarity_function(truth, comm) for truth in truths])

		for truth in truths:
			sum_truths += max([similarity_function(truth, comm) for comm in comms])

		result = (1/float(2*len(truths)))*sum_truths + (1/float(2*len(comms)))*sum_comms

		better = False
		for b in best:
			if result > b[0]:
				better = True
		if better:
			idx = best.index(min(best))
			best[idx] = (result, i)

	return best


if __name__ == '__main__':
	if (len(sys.argv) != 4):
		print("Usage: python3 evaluation.py <weights.txt> <cmtyvv.txt> <circles>")
		sys.exit()


	# [(0.32958382518984364, 9), (0.3418168919088339, 5), (0.3434018315546361, 7), (0.37638399408110157, 3), (0.38306664281461983, 4)]
	print(sorted(run_evaluation(sys.argv[1], sys.argv[2], sys.argv[3], compute_jaccard_index)))
	# [(0.423209368661001, 9), (0.4249453170715279, 5), (0.42735091699387007, 7), (0.4536551269170219, 3), (0.4616275002937089, 4)]
	print(sorted(run_evaluation(sys.argv[1], sys.argv[2], sys.argv[3], F1)))


