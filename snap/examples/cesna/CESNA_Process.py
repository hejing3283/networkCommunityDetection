
'''
Process protein networks for CESNA
Proc_Net processes the edges and Proc_Feat processes the features
Currently does not differentiate between mutations
'''

def Proc_All(Net, Path, Mut):
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

    # Need to know number of nodes for Svinet
    print node_counter

    Output = sorted(Output)

    with open('pp_networks_num.txt', 'w') as O:
        for edge in Output:
            O.write(edge)

    with open(Path, 'r') as I_Path:
        Input_Path = I_Path.readlines()

    with open(Mut, 'r') as I_Mut:
        Input_Mut = I_Mut.readlines()

    # Set count for features
    count = 1

    feat_name_out = set()
    feat_num_out = set()

    # For pathways
    for line in Input_Path:
        line_s = line.split('\t')
        # Add feature name to set
        feat_name_out.update([str(count) + '\t' + line_s[0] + '\n'])
        # Remove stray '\n's
        line_s[-1] = line_s[-1][:-1]
        # Add to set only if node exists
        for val in line_s[1:]:
            # print val
            try:
                # print Nodes[val][2]
                feat_num_out.update([str(Nodes[val]) + '\t' + str(count) + '\n'])
            except KeyError:
                pass
        # Increase count
        count += 1

    # For mutations
    for line in Input_Mut[1:]:
        line_s = line.split('\t')
        feat_name_out.update([str(count) + '\t' + 'MUTATION' + '\n'])
        # Write only if node exists
        if line_s[0] in Nodes:
            feat_num_out.update([str(Nodes[line_s[0]]) + '\t' + str(count) + '\n'])

    with open('pp_feat_num.txt', 'w') as O1:
        for i in feat_num_out:
            O1.write(i)

    with open('pp_feat_name.txt', 'w') as O2:
        for i in feat_name_out:
            O2.write(i)


    # Doesn't account for duplications
    # # For pathways
    # with open('pp_feat_num.txt', 'w') as O1:
    #     with open('pp_feat_name_num.txt', 'w') as O2:
    #         for line in Input_Path:
    #             line_s = line.split('\t')
    #             # Write feature name
    #             O2.write(str(count) + '\t' + line_s[0] + '\n')
    #             # Remove stray '\n's
    #             line_s[-1] = line_s[-1][:-1]
    #             # Write only if node exists
    #             for val in line_s[1:]:
    #                 try:
    #                     O1.write(str(Nodes[val]) + '\t' + str(count) + '\n')
    #                 except KeyError:
    #                     pass
    #             # Increase count
    #             count += 1

    # # For mutations
    # with open('pp_feat_num.txt', 'a') as O1:
    #     with open('pp_feat_name_num.txt', 'a') as O2:
    #         # Write feature name
    #         O2.write(str(count) + '\t' + 'MUTATION' + '\n')
    #         for line in Input_Mut[1:]:
    #             line_s = line.split('\t')
    #             # Write only if node exists
    #             if line_s[0] in Nodes:
    #                 O1.write(str(Nodes[line_s[0]]) + '\t' + str(count) + '\n')


# def Proc_Net(File):
#     with open(File, 'r') as I:
#         Input = I.readlines()

#     node_counter = 1

#     Nodes = {}

#     with open(File[:-4]+'_CESNA_Num.txt', 'w') as O:
#         for line in Input[1:]:
#             line_s = line.split('\t')
#             if line_s[0] not in Nodes:
#                 Nodes[line_s[0]] = node_counter
#                 node_counter += 1
#             if line_s[1] not in Nodes:
#                 Nodes[line_s[1]] = node_counter
#                 node_counter += 1
#             O.write(str(Nodes[line_s[0]]) + '\t' + str(Nodes[line_s[1]]) + '\n')
#             # O.write(line_s[0] + '\t' + line_s[1] + '\n')
#         # for line in Input[1:]:
#         #     line_s = line.split('\t')
#         #     O.write(line_s[0] + '\t' + line_s[1] + '\n')


# def Proc_Feat(File1, File2):
#     with open(File1, 'r') as I1:
#         Input1 = I1.readlines()

#     with open(File2, 'r') as I2:
#         Input2 = I2.readlines()

#     count = 1

#     with open('pp_feat.txt', 'w') as O1:
#         with open('pp_feat_name.txt', 'w') as O2:
#             for line in Input1:
#                 line_s = line.split('\t')
#                 O2.write(str(count) + '\t' + line_s[0] + '\n')
#                 line_s[-1] = line_s[-1][:-1]
#                 for val in line_s[1:]:
#                     O1.write(val + '\t' + str(count) + '\n')
#                 count += 1

#     with open('pp_feat.txt', 'a') as O1:
#         with open('pp_feat_name.txt', 'a') as O2:
#             # O1.write('Here starts mutation:\n')
#             O2.write(str(count) + '\t' + 'MUTATION' + '\n')
#             for line in Input2[1:]:
#                 line_s = line.split('\t')
#                 O1.write(line_s[0] + '\t' + str(count) + '\n')


if __name__ == '__main__':
    Proc_All('network.txt', 'nodes_attributes_pathway.txt', 'nodes_attributes_mutation.txt')
