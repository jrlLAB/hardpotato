# Pypotato library
Python API to control the following potentiostats:

* CHI760E from CH Instruments (chi760e)
* CHI1205b from CH Instruments (chi1205b)
* Emstat Pico from PalmSens (emstatpico)


Authors:

* Oliver Rodriguez*
* Michael Pence
* Joaquin Rodriguez-Lopez

University of Illinois at Urbana-Champaign.

Funded by JCESR.

# Installation
Open a console and do:
```python
pip install pypotato
```

# Usage
```python
from pypotato import *

# Potentiostat setup
# Choose the correct model from ['chi760e', 'chi1205b', 'emstatpico']:
model = 'chi760e' 
# Write the path where the chi software is installed (this line is optional when
# using the Pico). Make sure to use / instead of \:
path = 'C:/Users/jrl/CHI/chi760e.exe' # This is ignored for the Pico
# Write the path where the data and plots are going to be automatically saved:
folder = 'C:/Users/jrl/Experiments/data'
# Setup:
potentiostat.Setup(model, path, folder)

# Run CV with default values:
cv = potentiostat.CV()
#cv.bipot() # uncomment to activate second working electrode
cv.run()

# Run a LSV with default values:
lsv = potentiostat.LSV()
#lsv.bipot() # uncomment to activate second working electrode
lsv.run()

# Run a CA with default values:
ca = potentiostat.CA()
#ca.bipot() # uncomment to activate second working electrode
ca.run()

# Run an OCP with default values:
ocp = potentiostat.OCP()
ocp.run()
```

# Notes for CH Instruments users
* Since the CHI potentiostat software only work in Windows, any script written with
pypotato will only work in Windows.
* The chi translators use macro commands that are only available in the most 
recent versions of the software. Please contact CHI support for help on updating
the potentiostat software and firmware.

# Notes for Emstat Pico users
* The communication to the Pico is done via the serial port, this means that no
external software is required. Because of this, there is no live plotting, however,
the data and plots are saved when the measurement is finished.
* Scripts written for the pico may also work in other operating systems, provided
the library is installed correctly. So far, pypotato with the Pico has been 
tested in Windows 10 and Manjaro Linux with kernel 5.15.xx. 

# Requirements
* numpy
* matplotlib
* scipy
* softpotato

# Acknowledgements
* To CH Instruments for making their software flexible enough that it can be 
started from the Windows command line and for creating the Macros.
* To PalmSens for developing MethodScript and writing code for parsing data. The
code is in the [PalmSens MethodScript GitHub account](https://github.com/PalmSens/MethodSCRIPT_Examples)
