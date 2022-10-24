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
ttot = 1        # s, total time
dt = 0.01       # s, time increment
fileName = 'OCP' # base file name for data file
header = 'OCP'   # header for data file

# initialize experiment:
ocp = potentiostat.OCP(ttot, dt, fileName, header)
# Run experiment:
ocp.run()
