# -*- coding: utf-8 -*-
#import json
#from pprint import pprint
#json_data = open('AllSets.json')
#data = json.load(json_data)
#pprint(data)
#json_data.close         

import apriorialg as ap
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

minsupport = 0.5
min_confidence = 0.7
	
dataset = load_dataset()

L, support_data = ap.apriori(dataset, minsupport)
rules = ap.generateRules(L, support_data, min_confidence)

print 'L:\n', L
print '\nSupport data:\n', support_data
print '\nRules:\n', rules
		
    

    