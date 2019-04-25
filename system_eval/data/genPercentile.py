import numpy as np
import json


write_data = None
read_data = None
with open('./base_line.json','r') as fin:
	data = json.loads(fin.read())
	write_data = data["write"]
	read_data = data["read"]


def gen_percentile(data):
	analysis = []
	for d in data:
		analysis.append([d[2]])

	return np.percentile(analysis,99,axis=0)[0]

print("Write 99% percentile {0}".format(gen_percentile(write_data)))
print("Read 99% percentile {0}".format(gen_percentile(read_data)))
