# -*- coding: utf-8 -*-

import json

lists = json.loads(open('lists.json', 'r').read())

system_type = ''
service_type = ''
unique_id = ''
total_number_of_failure_modes = ''

def fmecaGenerate(component):
    pass