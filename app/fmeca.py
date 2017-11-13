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
                for f in s.failure_modes:
                    # This is basically each row in the FMECA table
                