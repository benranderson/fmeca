# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 22:15:35 2017

@author: Stuart
"""

v = {}

import json
with open('facility_assumptions.json', 'r') as j:
    d = json.load(j) 
    for l in d:
        v[l] = { "Vessel Abbreviation": l["Vessel Abbreviation"],
                 "Gross Cost (£/day)": l["Gross Cost (£/day)"],
                 "Mobilisation Time (days)": l["Mobilisation Time (days)"]}
        
print(v)