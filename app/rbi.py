# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 22:25:48 2017

@author: Stuart
"""


class RBI():

    def __init__(self, fmeca, inspection_type, commercial_risk_cutoff):
        self.fmeca = fmeca
        self.inspection_type = inspection_type
        self.rbi_failure_modes = []
        self.commercial_risk_cutoff = commercial_risk_cutoff
        self.total_annual_commercial_risk = 0.0
        self.risk_based_calculated_inspection = 0.0

    def run_RBI(self):
        for f in s.failure_modes:
            if f.inspection_type == self.inspection_type and f.time_dependant:
                self.rbi_failure_modes.append(f)
        for f in self.rbi_failure_modes:
            self.total_annual_commercial_risk += f.annual_commercial_risk
        self.risk_based_calculated_inspection = self.total_annual_commercial_risk / \
            self.commercial_risk_cutoff
