from pypotato import *

# Select the potentiostat model to use:
model = 'chi760e'

# Path to the chi software, including extension .exe
path = 'C:/Users/jrl/Desktop/CHI/chi760e/chi760e.exe'

# Folder where to save the data, it needs to be created previously
folder = 'C:/Users/jrl/echem/Data'

# Initialization:
potentiostat.Setup(model, path, folder)


# Experimental parameters:
ttot = 1        # s, total time
dt = 0.01       # s, time increment
fileName = 'OCP' # base file name for data file
header = 'OCP'   # header for data file

# initialize experiment:
ocp = potentiostat.OCP(ttot, dt, fileName, header)
# Run experiment:
ocp.run()
