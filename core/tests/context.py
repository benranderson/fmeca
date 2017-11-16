import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import core
import core.rbi as rbi
from core.rbi import Component, SubComponent, Failure, Consequence
