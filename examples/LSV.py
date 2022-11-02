from pypotato import *

# Select the potentiostat model to use:
model = 'chi1205b'

# Path to the chi software, including extension .exe
path = 'C:/Users/oliverrz/Desktop/CHI/chi1205b_mini2/chi1205b.exe'

# Folder where to save the data, it needs to be created previously
folder = 'C:/Users/oliverrz/gitHub/pytentiostat_fork/examples/data'

# Initialization:
potentiostat.Setup(model, path, folder)


# Experimental parameters:
Eini = -0.5     # V, initial potential
Efin = 0.5     # V, final potential
sr = 1          # V/s, scan rate
dE = 0.001      # V, potential increment
sens = 1e-6     # A/V, current sensitivity
E2 = 0.5        # V, potential of the second working electrode
sens2 = 1e-9    # A/V, current sensitivity of the second working electrode
fileName = 'LSV'# base file name for data file
header = 'LSV'  # header for data file

# initialize experiment:
lsv = potentiostat.LSV(Eini, Efin, sr, dE, sens, fileName, header)
# Include second working electrode in bipotentiostat mode.
# Comment or delete the next line to remove bipot mode.
#cv.bipot(E2,sens2)
# Run experiment:
lsv.run()
