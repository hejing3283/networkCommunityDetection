'''
Process networks for ContentMapEquation
'''


def Proc_CME(Net, Path, Mut):
    with open(Net, 'r') as I_Net:
        Input_Net = I_Net.readlines()

    node_counter = 0

    Nodes = {}

    # Output = set()

    for line in Input_Net[1:]:
        line_s = line.split('\t')
        # print line_s
        # Checks if nodes exist in the dictionary
        if line_s[0] not in Nodes:
            Nodes[line_s[0]] = [[node_counter], set(), set()]
            node_counter += 1
        if line_s[1][:-1] not in Nodes:
            Nodes[line_s[1][:-1]] = [[node_counter], set(), set()]
            node_counter += 1
        # Add edges to set of both nodes
        Nodes[line_s[0]][1].update(Nodes[line_s[1][:-1]][0])
        Nodes[line_s[1][:-1]][1].update(Nodes[line_s[0]][1])

    print node_counter

    with open(Path, 'r') as I_Path:
        Input_Path = I_Path.readlines()

    with open(Mut, 'r') as I_Mut:
        Input_Mut = I_Mut.readlines()

    # Set count for features
    count = 0

    # For pathways
    for line in Input_Path:
        line_s = line.split('\t')
        # Remove stray '\n's
        line_s[-1] = line_s[-1][:-1]
        # Write only if node exists
        for val in line_s[1:]:
            # print val
            try:
                # print Nodes[val][2]
                Nodes[val][2].update([count])
            except KeyError:
                pass
        # Increase count
        count += 1

    # For mutations
    for line in Input_Mut[1:]:
        line_s = line.split('\t')
        # Write only if node exists
        if line_s[0] in Nodes:
            Nodes[line_s[0]][2].update([count])

    # print Nodes

    # count number of attributes to ensure correctness
    attr_count = 0

    with open('pp_networks_CME.txt', 'w') as O:
        O.write(str(node_counter) + '\n')
        for n in Nodes:
            Temp = Nodes[n]
            output = str(Temp[0][0]) + ',' + str(len(Temp[1]))
            for m in Temp[1]:
                output = output + ':' + str(m) + ',' + str(1)
            O.write(output + '\n')
        # O.write('Features start here' + '\n')
        for n in Nodes:
            Temp = Nodes[n]
            # Check if set is empty
            if len(Temp[2]) > 0:
                output = str(Temp[0][0]) + '\t' + str(len(Temp[2]))
                attr_count += len(Temp[2])
                for m in Temp[2]:
                    output = output + '\t' + str(m) + '\t' + str(1)
                O.write(output + '\n')

    print attr_count

if __name__ == '__main__':
    Proc_CME('network.txt', 'nodes_attributes_pathway.txt', 'nodes_attributes_mutation.txt')
