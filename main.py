# -*- coding: utf-8 -*-
#import json
#from pprint import pprint
#json_data = open('AllSets.json')
#data = json.load(json_data)
#pprint(data)
#json_data.close         

import sys
import apriorialg as ap
from collections import Counter

arg = sys.argv[1:]


img_domain = 'https://s3-us-west-2.amazonaws.com/hearthstats/cards/'

minsupport = float(arg[0])
min_confidence = float(arg[1])

winrate = list()
winrate.append([])
decklist = list()
namelist = list()

def load_dataset():
	f = open('data.txt')
	heroes = tuple(f.readline().strip().split())
	print type(heroes)
	dataset = list()
	for k in range(1,10):
		N = int(f.readline().strip())
		print N
		rate = f.readline().strip().split()
		winrate.append(rate)
		for i in range(N):
			name = f.readline().strip()
			namelist.append(name)
			cards = f.readline().strip().split()
			key = N*(k-1)+i
			decklist.append(cards)
			
			counter = Counter(cards)
			transaction = counter.items()
			transaction.append(heroes[k]);
			dataset.append(transaction)
		
	return heroes, dataset

def filter_rules(rules):
	print '\nRules:'
	for rule in rules[:]:
		if(rule[2] == 1.0 and len(rule[1]) == 1):
			r = next(iter(rule[1]))
			if(r in heroes):
				print " - ", rule
				rules.remove(rule)
		else:
			print " + ", rule
	return rules

	
heroes, dataset = load_dataset()

print "Amount of decks:", len(decklist)
print namelist[0], decklist[0]
print "Win rate", decklist

L, support_data = ap.apriori(dataset, minsupport)
rules = ap.generateRules(L, support_data, min_confidence)

print '\nL:'
for l in L:
	print " * ", l

print "Amount of rules:", len(rules)
rules = filter_rules(rules)
print "New amount of rules:", len(rules)
# removing obvious rules:

 