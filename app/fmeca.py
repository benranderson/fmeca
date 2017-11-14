# -*- coding: utf-8 -*-

import json
import models

class fmeca():

    def __init__(self, subcomponents, inspection_type):
        self.lists = json.loads(open('lists.json', 'r').read())
        self.components = _interpret_components()
        self.subcomponents = subcomponents
        self.inspection_type = inspection_type
        
    def run_fmeca(self):
        for s in self.subcomponents:
            failure_modes = self.components[s]['Failure Modes']
            print(failure_modes)
    
    def _interpret_components(self):
        c_data = json.loads(open('components.json', 'r').read())
        self.c = []
        for comp in c_data:
            
                
if __name__ == '__main__':
    f = fmeca(["Actuated Process Valve"], 'ROV')
    f.run_fmeca()