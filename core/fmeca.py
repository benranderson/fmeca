# -*- coding: utf-8 -*-

class FMECA:
    
    def __init__(self, db_session):
        self.db_session = db_session
        self._compile_fmeca()
        self.fmeca_rows = {}
        
    def _compile_fmeca():
        for sc in self.cubcomponents:
            
            for fm in sc.failure_modes:
            
        pass