# -*- coding: utf-8 -*-
#import json
#from pprint import pprint
#json_data = open('AllSets.json')
#data = json.load(json_data)
#pprint(data)
#json_data.close         

from collections import Counter

def load_dataset():
	f = open('data.txt')
	heroes = f.readline().strip().split()

	dataset = list()

	for k in range(1,10):
		N = int(f.readline().strip())
		for i in range(N):
			name = f.readline().strip()
			line = f.readline().strip().split()
			c = Counter(line)
			transaction = c.items()
			transaction.insert(0,heroes[k]);
			#print name, c
			dataset.append(transaction)
	
	return dataset
	
dataset = load_dataset()

print dataset
		
    

    