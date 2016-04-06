
'''
Process protein networks for Svinet
Essentially the same as CESNA_Process, but displays number of nodes
'''


def Proc_Svinet(Net):
    with open(Net, 'r') as I_Net:
        Input_Net = I_Net.readlines()

    node_counter = 1

    Nodes = {}

    # Use set to catch repetitions
    Output = set()

    for line in Input_Net[1:]:
        line_s = line.split('\t')
        # Checks if the nodes are in the dictionary
        if line_s[0] not in Nodes:
            Nodes[line_s[0]] = node_counter
            node_counter += 1
        # To account for '\n's at the end
        if line_s[1][:-1] not in Nodes:
            Nodes[line_s[1][:-1]] = node_counter
            node_counter += 1
        Output.update([str(Nodes[line_s[0]]) + '\t' + str(Nodes[line_s[1][:-1]]) + '\n'])

    # Enable repetitions
    # with open('pp_networks_rep.txt', 'w') as O:
    #     for line in Input_Net[1:]:
    #         line_s = line.split('\t')
    #         if line_s[0] not in Nodes:
    #             Nodes[line_s[0]] = node_counter
    #             node_counter += 1
    #         if line_s[1] not in Nodes:
    #             Nodes[line_s[1]] = node_counter
    #             node_counter += 1
    #         O.write(str(Nodes[line_s[0]]) + '\t' + str(Nodes[line_s[1]]) + '\n')

    # Need to know number of nodes for Svinet, checked 3611 (5197 wrong) for pp network and 1494 for 1912.edges
    print node_counter

    Output = sorted(Output)

    with open('pp_networks_num.txt', 'w') as O:
        for edge in Output:
            O.write(edge)

# Detected 11 for pp network and 16 for 1912.edge

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
    Input_Comm = []
    with open(Comm, 'r') as I_Comm:
        for line in I_Comm:
            l = line.split()
            if l:
                x = l[0].strip('()').split(',')
                Input_Comm.append([int(e) for e in x])

    # Count number of communities
    # Num_Comm = len(Input_Comm)
    # print(Num_Comm)
    Num_Comm = 4

    # Create lists to contain remaps
    Comm = [[] for n in range(0, Num_Comm)]
    # print Comm

    # Remap
    for i in range(0, Num_Comm):
        for j in range(0, len(Input_Comm)):
            if Input_Comm[j][1] == i+1:
                node = Input_Comm[j][0]
                Comm[i].append(Nodes_Rev[int(node)])

    with open('RCommunities_' + str(Num_Comm) + '.txt', 'w') as O:
        for c in Comm:
            O.write(" ".join(elem for elem in c) + '\n')


if __name__ == '__main__':
    # Proc_Svinet('network.txt')
    ReMap_Communities('network.txt', 'clusters.mat')
