# -*- coding: utf-8 -*-
import json
from pprint import pprint
json_data = open('AllSets.json')
data = json.load(json_data)
pprint(data)
json_data.close     