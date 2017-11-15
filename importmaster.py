# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 12:15:31 2017

@author: stuart.roy
"""

import json
        
f = open('..\master.txt', 'r').readlines()

subcomponents = {}
sc = None

def new_failure_mode(d):
    return {'Random/Time Dependant': d[4],
            'BP Ored MTTF': float(d[5]),
            'Detectable by Inspection': d[6].strip(),
            'Type of Inspection': d[7].strip() }

for l in f[1:]:
    d = l.strip().split('\t')
    if d[0] in subcomponents:
        subcomponents[d[0]][d[2]] = new_failure_mode(d)
    else:
        subcomponents[d[0]] = {d[2]: new_failure_mode(d)}
    
json_string = json.dumps(subcomponents)
with open('master.json', 'w') as o:
    o.write(json_string)
print(json_string)
    