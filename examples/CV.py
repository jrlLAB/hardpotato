import pypotato as pp
import softpotato as sp

# Select the potentiostat model to use:
#model = 'chi760e'
model = 'chi1205b'
#model = 'emstatpico'

# Path to the chi software, including extension .exe. Negletected by emstatpico
path = 'C:/Users/oliverrz/Desktop/CHI/chi1205b_mini2/chi1205b.exe'

# Folder where to save the data, it needs to be created previously
folder = 'C:/Users/oliverrz/Desktop/data'

# Initialization:
pp.potentiostat.Setup(model, path, folder)

# Experimental parameters:
Eini = -0.5     # V, initial potential
Ev1 = 0.5       # V, first vertex potential
Ev2 = -0.5      # V, second vertex potential
Efin = -0.5     # V, final potential
sr = 1        # V/s, scan rate
dE = 0.001      # V, potential increment
nSweeps = 2     # number of sweeps
sens = 1e-6     # A/V, current sensitivity
E2 = 0.5        # V, potential of the second working electrode
sens2 = 1e-9    # A/V, current sensitivity of the second working electrode
fileName = 'CV' # base file name for data file
header = 'CV'   # header for data file

# Initialize experiment:
cv = pp.potentiostat.CV(Eini, Ev1,Ev2, Efin, sr, dE, nSweeps, sens, fileName, header)
# Run experiment:
cv.run()

# Load recently acquired data
data = pp.load_data.CV(fileName +'.txt', folder, model)
i = data.i
E = data.E

# Plot CV with softpotato
sp.plotting.plot(E, i, fig=1, show=1)

