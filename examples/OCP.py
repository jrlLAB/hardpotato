import pypotato as pp
import softpotato as sp

# Select the potentiostat model to use:
#model = 'chi760e'
model = 'chi1205b'
#model = 'emstatpico'

# Path to the chi software, including extension .exe
path = 'C:/Users/oliverrz/Desktop/CHI/chi1205b_mini2/chi1205b.exe'

# Folder where to save the data, it needs to be created previously
folder = 'C:/Users/oliverrz/Desktop/data'

# Initialization:
pp.potentiostat.Setup(model, path, folder)

# Experimental parameters:
ttot = 1        # s, total time
dt = 0.01       # s, time increment
fileName = 'OCP' # base file name for data file
header = 'OCP'   # header for data file

# initialize experiment:
ocp = pp.potentiostat.OCP(ttot, dt, fileName, header)
# Run experiment:
ocp.run()

# Load recently acquired data
data = pp.load_data.OCP(fileName +'.txt', folder, model)
E = data.E
t = data.t

# Plot OCP with softpotato
sp.plotting.plot(t, E, xlab='$t$ / s', ylab='$E$ / V', fig=1, show=1)

