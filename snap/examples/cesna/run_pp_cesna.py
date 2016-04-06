# run CESNA on PP network

import os
import sys


def ReMap_Communities(Net, Comm):
    # Get dictionary of proteins and numbers
    with open(Net, 'r') as I_Net:
        Input_Net = I_Net.readlines()

    node_counter = 1

    Nodes = {}

    for line in Input_Net[1:]:
        line_s = line.split('\t')
        if line_s[0] not in Nodes:
            Nodes[line_s[0]] = node_counter
            node_counter += 1
        if line_s[1][:-1] not in Nodes:
            Nodes[line_s[1][:-1]] = node_counter
            node_counter += 1

    # Reverse dictionary
    Nodes_Rev = {}

    for key, val in Nodes.items():
        Nodes_Rev[val] = key

    # Read communities
    with open(Comm, 'r') as I_Comm:
        Input_Comm = I_Comm.readlines()

    # Count number of communities
    Num_Comm = len(Input_Comm)
    print(Num_Comm)

    # Create lists to contain remaps
    Comm = [[] for n in range(0, Num_Comm)]
    # print Comm

    # Remap
    for i in range(0, Num_Comm):
        line_s = Input_Comm[i].split()
        for node in line_s[:-1]:
            Comm[i].append(Nodes_Rev[int(node)])

    with open('RCommunities_' + str(Num_Comm) + '.txt', 'w') as O:
        for c in Comm:
            O.write(" ".join(elem for elem in c) + '\n')


def run_cesna_pp():
	num_comm = [4, 10, 14, 20, 24, 30, 34]
	for i in num_comm:
		os.system('./cesna -c:%d -o:out/%d_ -i:pp_networks_num.txt -a:pp_feat_num.txt -n:pp_feat_name_num.txt' % (i, i))

		ReMap_Communities('network_textiq.txt', 'out/%d_cmtyvv.txt' % i)


if __name__ == '__main__':
	run_cesna_pp()


