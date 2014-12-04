# -*- coding: utf-8 -*-
#import json
#from pprint import pprint
#json_data = open('AllSets.json')
#data = json.load(json_data)
#pprint(data)
#json_data.close         

import sys
import apriorialg as ap
import heapq as pq
from collections import Counter

arg = sys.argv[1:]

img_domain = 'https://s3-us-west-2.amazonaws.com/hearthstats/cards/'

minsupport = float(arg[0])
min_confidence = float(arg[1])

winrate = list()
winrate.append([])
decklist = list()
namelist = list()
H = dict()

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

def build_heap(L, support_data):
    H['Any'] = []    
    for i in range(len(L)-1):
        for j in range(0, len(L[i])):
            A = list(L[i][j])
            for a in A:
                if(a in H.viewkeys()) is False:
                    print "Creating the key ", a
                    H[a] = []
                if(len(L[i][j].intersection(set(heroes))) == 0):
                    t = (i+1,support_data[L[i][j]],L[i][j])
                    if((t in H['Any']) is not True):
                        pq.heappush(H['Any'], t)
                pq.heappush(H[a], (i,support_data[L[i][j]],L[i][j]))
                         					
heroes, dataset = load_dataset()

print "Amount of decks:", len(decklist)
print namelist[0], decklist[0]

L, support_data = ap.apriori(dataset, minsupport)
rules = ap.generateRules(L, support_data, min_confidence)

total = 0
print '\nL:'
for l in L:
    print " * ", len(l), l
    total += len(l)

print "Total of itemsets supported:", total

print "Amount of rules:", len(rules)
rules = filter_rules(rules)
print "New amount of rules:", len(rules)
# removing obvious rules:
build_heap(L,support_data)
print "Lengh of Any:", len(H['Any'])
for hero in heroes:
    if hero in H.viewkeys():
        print hero, ':\n', H[hero]

count = Counter(H['Any'])
print "Lengh of Counter(Any):", len(count)
print count

print "\nAmount of keys:", len(H)
oH = list(H.viewkeys())
oH.sort()
print oH 
