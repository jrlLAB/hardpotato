# Pypotato library
Welcome to the pypotato GitHub repository. Pypotato is an open source Python
API to control commercially available potentiostats. It enables researchers to
write Python scripts that can include experimentation, immediate data analysis
using any third-party library and/or the control of other instruments. Pypotato
facilitates the standardization of electrochemical experiments by keeping a 
record of the experiments and data analysis that can be later run again to ensure 
repeatability. It also facilitates the sharing of electrochemical protocols 
between researchers and groups that own different potentiostats. 

Currently, the following potentiostats are included in the library:

* CHI760E from CH Instruments (chi760e)
* CHI1205b from CH Instruments (chi1205b)
* Emstat Pico from PalmSens (emstatpico)

with the following techniques:
* Cyclic voltammetry, CV
* Chronoamperometry, CA
* Linear sweep voltammetry, LSV
* Open circuit potential, OCP

For the CHI760E only (so far):
* Normal pulse voltammetry, NPV
* Electrochemical impedance spectroscopy, EIS


# Installation
Open a console and type:
```python
pip install pypotato
```

# Usage
Here are quick examples on how to use the library. For more help check the
[docs](https://github.com/oliverrdz/pypotato_fork/tree/main/docs) and the
[Examples](https://github.com/oliverrdz/pypotato_fork/tree/main/examples) folders.

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
* Since the CHI potentiostat software only works in Windows, any script written with
pypotato will only work in Windows.
* The CHI translators use macro commands that are only available in the most 
recent versions of the software. Please contact CHI support for help on updating
the potentiostat software and firmware.

# Notes for Emstat Pico users
* Contact PalmSens for instructions on how to update the firmware of the Pico.
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
* pyserial

# Acknowledgements
* To CH Instruments for making their software flexible enough that it can be 
started from the Windows command line and for creating the Macros.
* To PalmSens for developing MethodScript and writing code for parsing data. The
code is in the [PalmSens MethodScript GitHub account](https://github.com/PalmSens/MethodSCRIPT_Examples)

# Authors
Pypotato was developed at the University of Illinois at Urbana-Champaign by:

* Oliver Rodriguez ([oliverrdz.xyz](https://oliverrdz.xyz))
* Michael Pence
* Joaquin Rodriguez-Lopez (joaquinr@illinois.edu)

Funded by [JCESR](https://www.jcesr.org/).

