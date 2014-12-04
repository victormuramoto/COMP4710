import json
import string
import urllib
from pprint import pprint
json_data = open('AllSets.json')
data = json.load(json_data)

img_domain = 'https://s3-us-west-2.amazonaws.com/hearthstats/cards/'
count = 0
for item in data["System"]:
    name = item["name"]
    url = urllib.urlretrieve('https://s3-us-west-2.amazonaws.com/hearthstats/cards/' + name.lower().replace(" ","-") + ".png","cards//System//" + name.lower().replace(" ","-") + ".png")
    count = count + 1    

json_data.close
print count