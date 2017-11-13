# -*- coding: utf-8 -*-

import json

class fmeca():

    lists = json.loads(open('lists.json', 'r').read())

    components = []

    def __init__(self, components):
        self.components = components
        
    def run_fmeca(self):
        for c in components:
            for s in c.subcomponents:
                