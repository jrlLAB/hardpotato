from pypotato import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import softpotato as sp

model = 'chi1205b'
# Path to the chi software, including extension .exe
path = 'C:/Users/oliverrz/Desktop/CHI/chi1205b_mini2/chi1205b.exe'
# Folder where to save the data, it needs to be created previously
folder = 'C:/Users/oliverrz/gitHub/pytentiostat_fork/examples/data'
# Initialization:
potentiostat.Setup(model, path, folder)


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
A = 0.0314      # cm2, electrode area
C = 1e-6        # mol/cm3, bulk concentration of R

sr = np.array([0.2, 0.5, 1])          # V/s, scan rate
nsr = sr.size

E = []
i = []
for x in range(nsr):
    # initialize experiment:
    fileName = 'CV_' + str(int(sr[x]*1000)) + 'mVs'# base file name for data file
    cv = potentiostat.CV(Eini, Ev1,Ev2, Efin, sr, dE, nSweeps, sens, fileName, header)
    # Run experiment:
    cv.run()
    data = load_data.CV(fileName, folder, model)
    E.append(data.E)
    i.append(-data.i)

E = np.array(E)
i = np.array(i)

# Extracting peak currents and peak potentials:
iPk_an = np.max(i)
iPk_cat = np.min(i)
EPk_an = E[np.argmax(i[:,0])]
EPk_cat = E[np.argmin(i[:,0])]

# Calculating E0:
E0 = np.mean([EPk_an, EPk_cat])
print('E0 = {:.2f} V'.format(E0))

# Calculating D from Randles-Sevcik equation:
sr_sqrt = np.sqrt(sr)
res_an = linregress(sr_sqrt, iPk_an)
res_cat = linregress(sr_sqrt, iPk_cat)
D = (res.cat/((2.69e5)*A*C))
print(D)
print('D = {:.2f} x10^5 cm/s'.format(D*1e5))

# Simulation with Soft Potato
wf = sp.technique.Sweep(Eini=-0.5, Efin=0.5, sr=sr[0])
sim = sp.simulate.E(wf, A=A, E0=E0, cOb=0, cRb=C, DO=D, DR=D)
sim.run() 

plt.figure(1)
plt.plot(cv_exp.E, -cv_exp.i*1e6, label='Experiment')
plt.plot(sim.E, sim.i*1e6, label='Simulation')
sp.plotting.format(xlab='$E$ / V', ylab='$i$ / $\mu$A', legend=[1], show=1)
