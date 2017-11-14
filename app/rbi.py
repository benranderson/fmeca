# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 22:25:48 2017

@author: Stuart
"""

class RBI():
    
    def __init__(self, fmeca):
        self.fmeca = fmeca
        
    def run_RBI(self):
        for f in s.failure_modes:
            if f.inspection_type == self.inspection_type and f.time_dependant: