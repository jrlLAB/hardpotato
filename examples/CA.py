import hardpotato as hp
import softpotato as sp

# Select the potentiostat model to use:
#model = 'chi760e'
#model = 'chi1205b'
model = 'emstatpico'

# Path to the chi software, including extension .exe
path = 'C:/Users/oliverrz/Desktop/CHI/chi1205b_mini2/chi1205b.exe'

# Folder where to save the data, it needs to be created previously
folder = 'C:/Users/oliverrz/Desktop/data'

# Initialization:
hp.potentiostat.Setup(model, path, folder)

# Experimental parameters:
Estep = 0.5     # V, step potential
dt = 0.01       # s, time increment
ttot = 1        # s, total time
sens = 1e-6     # A/V, current sensitivity
E2 = 0.5        # V, potential of the second working electrode
sens2 = 1e-9    # A/V, current sensitivity of the second working electrode
fileName = 'CA' # base file name for data file
header = 'CA'   # header for data file

# Initialize experiment:
ca = hp.potentiostat.CA(Estep, dt, ttot, sens, fileName, header)
# Run experiment:
ca.run()

# Load recently acquired data
data = hp.load_data.CA(fileName +'.txt', folder, model)
i = data.i
t = data.t

# Plot CV with softpotato
sp.plotting.plot(t, i, xlab='$t$ / s', fig=1, show=1)

