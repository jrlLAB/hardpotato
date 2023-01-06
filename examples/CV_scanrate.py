import hardpotato as hp
import numpy as np
import matplotlib.pyplot as plt
import softpotato as sp

# Select the potentiostat model to use:
model = 'chi760e'
#model = 'chi760e'
# Path to the chi software, including extension .exe
path = 'C:/Users/jrl/Desktop/CHI/chi760e/chi760e.exe'
# Folder where to save the data, it needs to be created previously
folder = 'C:/Users/jrl/echem/Data'
# Initialization:
hp.potentiostat.Setup(model, path, folder)


# Experimental parameters:
Eini = -0.5     # V, initial potential
Ev1 = 0.5       # V, first vertex potential
Ev2 = -0.5      # V, second vertex potential
Efin = -0.5     # V, final potential
dE = 0.001      # V, potential increment
nSweeps = 2     # number of sweeps
sens = 1e-6     # A/V, current sensitivity
E2 = 0.5        # V, potential of the second working electrode
sens2 = 1e-9    # A/V, current sensitivity of the second working electrode
header = 'CV'   # header for data file

sr = np.array([0.2, 0.5, 1])          # V/s, scan rates
nsr = sr.size

for x in range(nsr):
    # initialize experiment:
    fileName = 'CV_' + str(int(sr[x]*1000)) + 'mVs'# base file name for data file
    print(fileName)
    cv = hp.potentiostat.CV(Eini, Ev1,Ev2, Efin, sr[x], dE, nSweeps, sens, fileName, header)
    # Include second working electrode in bipotentiostat mode.
    # Comment or delete the next line to remove bipot mode.
    #cv.bipot(E2,sens2)
    # Run experiment:
    cv.run()
