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
Estep = 0.5     # V, step potential
dt = 0.01       # s, time increment
ttot = 1        # s, total time
sens = 1e-6     # A/V, current sensitivity
E2 = 0.5        # V, potential of the second working electrode
sens2 = 1e-9    # A/V, current sensitivity of the second working electrode
fileName = 'CA' # base file name for data file
header = 'CA'   # header for data file

# initialize experiment:
ca = potentiostat.CA(Estep, dt, ttot, sens, fileName, header)
# Include second working electrode in bipotentiostat mode.
# Comment or delete the next line to remove bipot mode.
#cv.bipot(E2,sens2)
# Run experiment:
ca.run()
