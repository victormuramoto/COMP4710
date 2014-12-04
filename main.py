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


winrate = list()
winrate.append([])

arg = sys.argv[1:]

def load_dataset():
	f = open('data.txt')
	heroes = f.readline().strip().split()
	dataset = list()
	for k in range(1,10):
		N = int(f.readline().strip())
		rate = f.readline().strip().split()
		winrate.append(rate)
		for i in range(N):
			name = f.readline().strip()
			cards = f.readline().strip().split()
			
			counter = Counter(cards)
			transaction = counter.items()
			transaction.append(heroes[k]);
			dataset.append(transaction)
		
	return dataset

img_domain = 'https://s3-us-west-2.amazonaws.com/hearthstats/cards/'

minsupport = float(arg[0])
min_confidence = float(arg[1])
	
dataset = load_dataset()

L, support_data = ap.apriori(dataset, minsupport)
rules = ap.generateRules(L, support_data, min_confidence)

print '\nL:'
for l in L:
	print " * ", l

#print '\nSupport data:\n', support_data
print '\nRules:'
for rule in rules:
	print " - ", rule

		
# argumentos para a DP:
# - eliminar todos os itens de L que contenham alguma carta que não pertença ao deck
# - peso da mochila é igual à quantidade de cartas inseridas
# - V será medido pela radiciação de grau igual a quantidade de itemsets sobre o valor da 
# multiplicação do support de cada itemset envolvido.
# - o resultado da D.P. dará o valor da sinergia / coerência do Deck. 