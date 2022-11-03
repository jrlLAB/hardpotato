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
Eini = -0.5     # V, initial potential
Efin = 0.5      # V, final potential
sr = 1          # V/s, scan rate
dE = 0.001      # V, potential increment
sens = 1e-6     # A/V, current sensitivity
E2 = 0.5        # V, potential of the second working electrode
sens2 = 1e-9    # A/V, current sensitivity of the second working electrode
fileName = 'LSV'# base file name for data file
header = 'LSV'  # header for data file

# initialize experiment:
lsv = pp.potentiostat.LSV(Eini, Efin, sr, dE, sens, fileName, header)
# Run experiment:
lsv.run()

# Load recently acquired data
data = pp.load_data.LSV(fileName +'.txt', folder, model)
i = data.i
E = data.E

# Plot CV with softpotato
sp.plotting.plot(E, i, fig=1, show=1)

