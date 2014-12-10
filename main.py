# -*- coding: utf-8 -*-
import json
from pprint import pprint       
json_data = open('AllSets.json')
data = json.load(json_data)
#pprint(data)
json_data.close 

allcards = dict()
for key in data.viewkeys():
	for item in data[key]:
		t = item['type']
		if(t == 'Minion' or t == 'Spell' or t == 'Weapon'):
			if not 'cost' in item.viewkeys() :
				cost = 0
			else:
				cost = item['cost']
			allcards[item['id']] = [item['name'], cost]

#for card in allcards:
#	print card, allcards[card]


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
class_cards = dict()
N = 0;

def tostring(t):
	return ' <{}> {} ({})'.format(allcards[t[0]][1], allcards[t[0]][0], t[1])

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

			counter = Counter(cards)
			decklist.append(counter.items())
			transaction = counter.items()
			transaction.append(heroes[k]);
			dataset.append(transaction)

	return heroes, dataset


def filter_rules(rules):
    #print '\nRules:'
    for hero in heroes:
        class_cards[hero] = set()
    for rule in rules[:]:
        if(len(rule[1]) == 1):
            r = next(iter(rule[1]))
            if(r in heroes):
     #           print " - ", rule
                class_cards[r] = class_cards[r].union(rule[0])
                rules.remove(rule)
      #  else:
       #     print " + ", rule
    
    #print class_cards
    return rules


def build_heap(L, support_data):
    H['Any'] = []    
    for i in range(len(L)-1):
        for j in range(0, len(L[i])):
            A = list(L[i][j])
            for a in A:
                if(a in H.viewkeys()) is False:
                    #print "Creating the key ", a
                    H[a] = []
                if(len(L[i][j].intersection(set(heroes))) == 0):
                    t = (-(i+1),-(i+1)*support_data[L[i][j]],L[i][j])
                    if(class_of_set(L[i][j]) == None and (t in H['Any']) is not True):
                        pq.heappush(H['Any'], t)
                pq.heappush(H[a], (-i,-i*support_data[L[i][j]],L[i][j]))
                        					
def class_of_set(s):
	for hero in heroes[1:]:
		if (len(s.intersection(class_cards[hero])) > 0):
			return hero
	return None

def is_eligible_tuple(t, hero):
	#print "t[2]: ", t[2]	
    found = list(set(heroes).intersection(t[2]));
	#print "found: ", found
    if(len(found) == 1):
        found = found[0]
        return found == hero
        
    for h in heroes:
        found = list(class_cards[h].intersection(t[2]))
        if(len(found) > 0 and h != hero):
            #print "Found: ", h, found            
            return False
    return True
	
def getNextEligibleTuple(e, hero, _H):
	while True:
		if len(_H[e]) == 0:
			return None
		front = pq.heappop(_H[e])
		if is_eligible_tuple(front,hero): break
	
	return front
	
def build_best_scored_deck(hero):
	deck = set()
	_H = H.copy()
#	usedCards = list
	
	h = []
	score = 0.0;
	size = 0;
	
	deck.add(hero)
	pq.heappush(h, (pq.heappop(_H[hero]), hero))
	
	while(size < 30 and len(h) > 0):
		t = pq.heappop(h)
		e = t[1]
		
		front = getNextEligibleTuple(e, hero, _H)					
		if front is not None:
			pq.heappush(h, (front, e))
		
		t = t[0]
		cards = t[2]
		newcards = list(cards - deck)
		
		if (len(newcards) > 0):
			weight = 0
			#print "Size: ", size
			for card in newcards:
			#	print card[0], tostring(card)
				weight += card[1] 
			
			if(weight + size <= 30):
				score += t[1];
				size += weight;
				deck = deck.union(cards)
				for card in newcards:
					front = getNextEligibleTuple(card, hero, _H)
					if front is not None:
						pq.heappush(h, (front, card))
				
	
	deck.remove(hero)
	
	return deck, -score;	

def verify_built_deck(deck, hero):
	N = len(decklist)/9
	k = heroes.index(hero)
	
	if( k == 0 ): return None, None
	
	min_diff = 31
	deck_id = -1
	
	for i in range(N):
		u = (k-1)*N + i
		
		diff, cards = calc_diff_decks(deck, set(decklist[u]))
		if(diff < min_diff):
			min_diff = diff
			deck_id = u
		if(diff == 0): return deck_id, min_diff
	
	return deck_id, min_diff


def calc_diff_decks(d1, d2):
	cards = d1 & d2
	_d1 = list(d1 - cards)
	_d2 = list(d2 - cards)
	
	for i in range(len(_d1)-1):
		for j in range(i+1, len(_d2)):
			if(_d1[i][0] == _d2[j][0]) :
				cards.add((_d1[i][0],1))
	
	count = 0
	for card in list(cards):
		count += card[1]
	
	return (30 - count), list(cards)		
		
##########################################################################################
					
heroes, dataset = load_dataset()

print "Amount of decks:", len(decklist)
print namelist[0], decklist[0]

L, support_data = ap.apriori(dataset, minsupport)
rules = ap.generateRules(L, support_data, min_confidence)

total = 0
#print '\nL:'
#for l in L:
 #   print " * ", len(l), l
  #  total += len(l)

#print "Total of itemsets supported:", total

#print "Amount of rules:", len(rules)
rules = filter_rules(rules)
#print "New amount of rules:", len(rules)
# removing obvious rules:

build_heap(L,support_data)
print "Lengh of Any:", len(H['Any'])
#for hero in heroes:
 #   if hero in H.viewkeys():
  #      print hero, ':\n', H[hero]

#count = Counter(H['Any'])
#print "Lengh of Counter(Any):", len(count)
#print count

#print "\nAmount of different relevant cards (keys):", len(H) - 10
#oH = list(H.viewkeys())
#oH.sort()
#print oH[10:]

print '\n List of class exclusive cards:'
for hero in heroes:
    print  ' (', len(class_cards[hero]), ')', hero
    print '\t', class_cards[hero]

for hero in heroes:
	deck, score = build_best_scored_deck(hero)  
	print '\nThe best scored deck for ', hero, ':'
	for card in list(deck):
		print ' -', tostring(card)
	print 'Synergy (score):', score	
	
	id, diff = verify_built_deck(deck, hero)
	
	if(id != None):
		print "Closest Real Deck:"
		print ' - "', namelist[id], '", with', 30-diff, 'similar cards.'   
    

