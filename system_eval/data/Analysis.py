import numpy as np
import json



percentile = {
	"write" : 0.011838204860687252,
	"read" : 0.028472673892974847
}

files_to_analyze = [
	"./stock_1.json",
	"./stock_4.json",
	"./stock_8.json",
	"./stock_16.json"
]

out_csv = "results.csv"


def analysis(name,experiment,data_to_analyze):
	data = []
	count = 0.0
	for d in data_to_analyze:

		if d[2] >= percentile[experiment]:
			count += 1.0
	
		data.append(d[2]) #we only need the response time

	average = np.average(data,axis=0)
	stdev = np.std(data,axis=0)
	SLO_VIO = count / float(len(data))

	return [name,experiment,average,stdev,SLO_VIO]



for fil in files_to_analyze:
	data_to_analyze = None
	with open(fil,'r') as fout:
		data_to_analyze = json.loads(fout.read())
	print(analysis(fil,"write",data_to_analyze["write"]))
	print(analysis(fil,"read",data_to_analyze["read"]))
