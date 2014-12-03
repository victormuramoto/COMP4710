# -*- coding: utf-8 -*-
#import json
#from pprint import pprint
#json_data = open('AllSets.json')
#data = json.load(json_data)
#pprint(data)
#json_data.close         

from collections import Counter

f = open('data.txt')
count = Counter()
i = 0
transactions = dict()
for line in f:
    line = line.strip()    
    if i == 0:
        url = line
    if i == 31:
        print 'this is a count'
        transactions[url] = count        
        print transactions[url]
        count.clear()
        i= 0
    count[line] += 1
    i = i +1
    #for x in range(1,32):
     #   print line
    

    