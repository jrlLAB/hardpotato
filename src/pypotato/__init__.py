"""
pypotato library

"""

from . import potentiostat
from . import load_data

__version__ = "1.2.3"
__author__ = 'Oliver Rodriguez'

# modules to import when user does 'from pytentiostat import *':
__all__ = ['potentiostat', 'load_data']
