
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

    # Need to know number of nodes for Svinet, checked 3610 (5197 wrong) for pp network and 1494 for 1912.edges
    # Got 35060 nodes and 419 communities
    print node_counter - 1

    Output = sorted(Output)

    with open('network_textiq_num.txt', 'w') as O:
        for edge in Output:
            O.write(edge)

# Detected 11 for pp network and 16 for 1912.edge and 418 for text iq

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

    # Create lists to contain remaps
    Comm = [[] for n in range(0, Num_Comm)]
    # print Comm

    # Remap
    for i in range(0, Num_Comm):
        line_s = Input_Comm[i].split(' ')
        for node in line_s[:-1]:
            Comm[i].append(Nodes_Rev[int(node)])

    with open('RCommunities_' + str(Num_Comm) + '.txt', 'w') as O:
        for c in Comm:
            O.write(" ".join(elem for elem in c) + '\n')


if __name__ == '__main__':
    Proc_Svinet('network_textiq.txt')
    # ReMap_Communities('network.txt', 'communities.txt')
