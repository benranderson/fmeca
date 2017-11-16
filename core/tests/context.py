import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import core
import core.risk_calculator as risk_calculator
from core.risk_calculator import Component, SubComponent, Failure, \
    Consequence, Vessel
