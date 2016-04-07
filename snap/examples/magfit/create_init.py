

def create_init(node_attr_file):

	outfile = open('init_test.config', 'w')

	data = []
	with open(node_attr_file, 'r') as f:
		for line in f:
			data.append([float(e) for e in line.split()])

	data = data[:100]
	print(len(data[0]))
	for i in range(0, len(data[0])-1, 2):
		l_0_0 = 0.0
		l_0_1 = 0.0
		l_1_0 = 0.0
		l_1_1 = 0.0
		for j in range(0, len(data)):
			if data[j][i] == 0:
				if data[j][i+1] == 0:
					l_0_0 += 1.0
				else:
					l_0_1 += 1.0
			else:
				if data[j][i+1] == 0:
					l_1_0 += 1.0
				else:
					l_1_1 += 1.0

		outfile.write('0.4 & ' + str(l_0_0/len(data)) + ' ' + 
			str(l_0_1/len(data)) + ';' + str(l_1_0/len(data)) + 
			' ' + str(l_1_1/len(data)) + '\n')
		outfile.write('0.4 & ' + str(l_0_0/len(data)) + ' ' + 
			str(l_0_1/len(data)) + ';' + str(l_1_0/len(data)) + 
			' ' + str(l_1_1/len(data)) + '\n')

	if len(data[0]) % 2 != 0:
		outfile.write('0.4 & ' + str(l_0_0/len(data)) + ' ' + 
			str(l_0_1/len(data)) + ';' + str(l_1_0/len(data)) + 
			' ' + str(l_1_1/len(data)) + '\n')


def main():
	create_init('node_attr_file.txt')

main()
