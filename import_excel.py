# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 08:22:32 2017

@author: stuart.roy
"""

from openpyxl import load_workbook



wb = load_workbook('..\FMEA Tool - Sandbox.xlsm')


print(wb.get_sheet_names())