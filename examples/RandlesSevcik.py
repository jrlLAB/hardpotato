import pypotato as pp
import numpy as np
import matplotlib.pyplot as plt
import softpotato as sp
from scipy.optimize import curve_fit

##### Setup
# Select the potentiostat model to use:
# emstatpico, chi1205b, chi760e
#model = 'chi760e'
model = 'chi1205b'
#model = 'emstatpico'

# Path to the chi software, including extension .exe. Negletected by emstatpico
path = 'C:/Users/oliverrz/Desktop/CHI/chi1205b_mini2/chi1205b.exe'
# Folder where to save the data, it needs to be created previously
folder = 'C:/Users/oliverrz/Desktop/data'
# Initialization:
pp.potentiostat.Setup(model, path, folder)


##### Experimental parameters:
Eini = -0.3     # V, initial potential
Ev1 = 0.5       # V, first vertex potential
Ev2 = -0.3      # V, second vertex potential
Efin = -0.3     # V, final potential
dE = 0.001      # V, potential increment
nSweeps = 2     # number of sweeps
sens = 1e-4     # A/V, current sensitivity
header = 'CV'   # header for data file

##### Experiment:
sr = np.array([0.02, 0.05, 0.1, 0.2])          # V/s, scan rate
nsr = sr.size
i = []
for x in range(nsr):
    # initialize experiment:
    fileName = 'CV_' + str(int(sr[x]*1000)) + 'mVs'# base file name for data file
    cv = pp.potentiostat.CV(Eini, Ev1,Ev2, Efin, sr[x], dE, nSweeps, sens, fileName, header)
    # Run experiment:
    cv.run()
    # load data to do the data analysis later
    data = pp.load_data.CV(fileName + '.txt', folder, model)
    i.append(data.i)
i = np.array(i)
i = i[:,:,0].T
E = data.E


##### Data analysis
# Estimation of D with Randles-Sevcik
n = 1       # number of electrons
A = 0.071   # cm2, geometrical area
C = 1e-6    # mol/cm3, bulk concentration

# Showcases how powerful softpotato can be for fitting:
def DiffCoef(sr, D):
    macro = sp.Macro(n, A, C, D)
    rs = macro.RandlesSevcik(sr)
    return rs
    
iPk_an = np.max(i, axis=0)
iPk_ca = np.min(i, axis=0)
iPk = np.array([iPk_an, iPk_ca]).T
popt, pcov = curve_fit(DiffCoef, sr, iPk_an)
D = popt[0]

# Estimation of E0 from all CVs:
EPk_an = E[np.argmax(i, axis=0)]
EPk_ca = E[np.argmin(i, axis=0)]
E0 = np.mean((EPk_an+EPk_ca)/2)

#### Simulation with softpotato
iSim = []
for x in range(nsr):
    wf = sp.technique.Sweep(Eini,Ev1, sr[x])
    sim = sp.simulate.E(wf, n, A, E0, 0, C, D, D)
    sim.run()
    iSim.append(sim.i)
iSim = np.array(iSim).T
print(iSim.shape)
ESim = sim.E

##### Printing results
print('\n\n----------Results----------')
print('D = {:.2f}x10^-6 cm2/s'.format(D*1e6))
print('E0 = {:.2f} mV'.format(E0*1e3))

##### Plotting
srsqrt = np.sqrt(sr)
sp.plotting.plot(E, i*1e6, ylab='$i$ / $\mu$A', fig=1, show=0)
sp.plotting.plot(srsqrt, iPk*1e6, mark='o-', xlab=r'$\nu^{1/2}$ / V$^{1/2}$ s$^{-1/2}$', 
                 ylab='$i$ / $\mu$A', fig=2, show=0)

plt.figure(3)
plt.plot(E, i*1e6)
plt.plot(wf.E, iSim*1e6, 'k--')
plt.title('Experiment (-) vs Simulation (--)')
sp.plotting.format(xlab='$E$ / V', ylab='$i$ / $\mu$A', legend=[0], show=1)
