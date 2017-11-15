# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 22:15:35 2017

@author: Stuart
"""

vessels = {}

import json
with open('facility_assumptions.json', 'r') as j:
    d = json.load(j)
    vessels = d["Vessels"]
        
print(vessels)