"""
pytentiostat library

"""

#from .potentiostat import *
#from .load_data import *
from . import potentiostat
from . import load_data

__version__ = "0.0.2"
__author__ = 'Oliver Rodriguez'

# modules to import when user does 'from pytentiostat import *':
__all__ = ['potentiostat', 'load_data' ]
