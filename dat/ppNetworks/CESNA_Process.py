'''
Process protein networks for CESNA
Proc_Net processes the edges and Proc_Feat processes the features
Currently does not differentiate between mutations
'''


def Proc_Net(File):
    with open(File, 'r') as I:
        Input = I.readlines()

    with open(File[:-4]+'_CESNA.txt', 'w') as O:
        for line in Input[1:]:
            line_s = line.split('\t')
            O.write(line_s[0] + '\t' + line_s[1] + '\n')


def Proc_Feat(File1, File2):
    with open(File1, 'r') as I1:
        Input1 = I1.readlines()

    with open(File2, 'r') as I2:
        Input2 = I2.readlines()

    count = 1

    with open('pp_feat.txt', 'w') as O1:
        with open('pp_feat_name.txt', 'w') as O2:
            for line in Input1:
                line_s = line.split('\t')
                O2.write(str(count) + '\t' + line_s[0] + '\n')
                line_s[-1] = line_s[-1][:-1]
                for val in line_s[1:]:
                    O1.write(val + '\t' + str(count) + '\n')
                count += 1

    with open('pp_feat.txt', 'a') as O1:
        with open('pp_feat_name.txt', 'a') as O2:
            # O1.write('Here starts mutation:\n')
            O2.write(str(count) + '\t' + 'MUTATION' + '\n')
            for line in Input2[1:]:
                line_s = line.split('\t')
                O1.write(line_s[0] + '\t' + str(count) + '\n')


if __name__ == '__main__':
    Proc_Net('network.txt')
    Proc_Feat('nodes_attributes_pathway.txt', 'nodes_attributes_mutation.txt')
