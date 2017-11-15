# -*- coding: utf-8 -*-

import json
import models
from api.failure_modes import new_subcomponent_failure_mode

class fmeca():
    
    __tablename__ = 'fmeca'
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, subcomponents, inspection_type):
        self.lists = json.loads(open('lists.json', 'r').read())
        self.failure_modes = _interpret_failure_modes()
        self.subcomponents = subcomponents
        self.inspection_type = inspection_type
        
    def run_fmeca(self):
        for s in self.subcomponents:
            failure_modes = self.components[s]['Failure Modes']
            print(failure_modes)
    
    def _interpret_failure_modes(self):
        sc_data = json.loads(open('components.json', 'r').read())
        self.sc = []
        for subcomp in sc_data:
            for fm in subcomp:
                f = FailureMode(self.sc)
            
                
if __name__ == '__main__':
    f = fmeca(["Actuated Process Valve"], 'ROV')
    f.run_fmeca()