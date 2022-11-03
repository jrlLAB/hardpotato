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

# Example: techniques
Here are quick examples on how to use the library. For more help check the
[docs](https://github.com/oliverrdz/pypotato_fork/tree/main/docs) folder and the
[Wiki](https://github.com/jrlLAB/pypotato/wiki).

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


# Example: Randles-Sevcik methodology
```python
from pypotato import *
import numpy as np
import matplotlib.pyplot as plt
import softpotato as sp
from scipy.optimize import curve_fit

##### Setup
# Select the potentiostat model to use:
# emstatpico, chi1205b, chi760e
model = 'chi760e'
# Path to the chi software, including extension .exe
path = 'C:/Users/jrl/Desktop/CHI/chi760e/chi760e.exe'
# Folder where to save the data, it needs to be created previously
folder = 'C:/Users/jrl/echem/Data'
# Initialization:
potentiostat.Setup(model, path, folder)


##### Experimental parameters:
Eini = -0.3     # V, initial potential
Ev1 = 0.5       # V, first vertex potential
Ev2 = -0.3      # V, second vertex potential
Efin = -0.3     # V, final potential
dE = 0.001      # V, potential increment
nSweeps = 2     # number of sweeps
sens = 1e-4     # A/V, current sensitivity
header = 'CV'   # header for data file

##### Experiment:
sr = np.array([0.05, 0.1, 0.2])          # V/s, scan rate
nsr = sr.size
i = []
for x in range(nsr):
    # initialize experiment:
    fileName = 'CV_' + str(int(sr[x]*1000)) + 'mVs'# base file name for data file
    cv = potentiostat.CV(Eini, Ev1,Ev2, Efin, sr[x], dE, nSweeps, sens, fileName, header)
    # Run experiment:
    cv.run()
    # load data to do the data analysis later
    data = load_data.CV(fileName + '.txt', folder, model)
    i.append(data.i)
i = np.array(i)
i = i[:,:,0].T
E = data.E


##### Data analysis
# Estimation of D with Randles-Sevcik
n = 1
A = 0.071
C = 1e-6
def DiffCoef(sr, D):
    # Showcases how powerful softpotato can be for fitting:
    macro = sp.Macro(n, A, C, D)
    rs = macro.RandlesSevcik(sr)
    return rs
    
iPk_an = np.max(i, axis=0)
iPk_ca = np.min(i, axis=0)
iPk = np.array([iPk_an, iPk_ca]).T
popt, pcov = curve_fit(DiffCoef, sr, iPk_an)
D = popt[0]

# Estimation of E0 from all CVs:
EPk_an = E[np.argmax(i, axis=0)]
EPk_ca = E[np.argmin(i, axis=0)]
E0 = np.mean((EPk_an+EPk_ca)/2)


#### Simulation with softpotato
iSim = []
for x in range(nsr):
    wf = sp.technique.Sweep(Eini,Ev1, sr[x])
    sim = sp.simulate.E(wf, n, A, E0, 0, C, D, D)
    sim.run()
    iSim.append(sim.i)
iSim = np.array(iSim).T
print(iSim.shape)
ESim = sim.E

##### Printing results
print('\n\n----------Results----------')
print('D = {:.2f}x10^-6 cm2/s'.format(D*1e6))
print('E0 = {:.2f} mV'.format(E0*1e3))

##### Plotting
srsqrt = np.sqrt(sr)
sp.plotting.plot(E, i*1e6, ylab='$i$ / $\mu$A', fig=1, show=0)
sp.plotting.plot(srsqrt, iPk*1e6, mark='o-', xlab=r'$\nu^{1/2}$ / V$^{1/2}$ s$^{-1/2}$', 
                 ylab='$i$ / $\mu$A', fig=2, show=0)

plt.figure(3)
plt.plot(E, i*1e6)
plt.plot(wf.E, iSim*1e6, 'k--')
plt.title('Experiment (-) vs Simulation (--)')
sp.plotting.format(xlab='$E$ / V', ylab='$i$ / $\mu$A', legend=[0], show=1)

```

