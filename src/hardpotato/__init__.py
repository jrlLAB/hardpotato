"""
hardpotato library

"""

from . import potentiostat
from . import load_data

__version__ = "1.3.11"
__author__ = 'Oliver Rodriguez'

# modules to import when user does 'from pypotato import *':
__all__ = ['potentiostat', 'load_data']
