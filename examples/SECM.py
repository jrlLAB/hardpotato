import hardpotato as hp
import softpotato as sp

# select the potentiostat model to use:
model = 'chi920d'

# Path to the chi software, including  extension .exe
path = 'C:/Users/parasita/Downloads/chi920d/chi920d.exe'

# Folder where to save the datam it needs to be created previusly
folder = './data/tests/SECM_test'

# Setup hardpotato:
hp.potentiostat.Setup(model, path, folder)
# Setup SECM mode:
secm = hp.potentiostat.SECM()

# Approach paramenters:
E1PAC = 0.4          # V, Potential in working electrode 1 (UME)
iratio = 60          # %, Current ratio threshold
sensPAC = 1e-9       # A/V, Current sensitivity of the working electrode 1 (UME)
maxincr = 1          # um/s, Approach speed
withdraw = 0         # um, Probe withdraw distance before probe approach
fileNamePAC = 'PAC'  # base file name for probe approach curve
# SECM parameters:
secmmode = 'i'       # 'i' current, 'e' potential, 'ci' constant current, 'imp' impedance
E1SECM = -0.1        # V, Potential in working electrode 1 (UME)
sens1SECM = 1e-9     # A/V, Currente sesitivity of working electrode 1 (UME)
E2SECM = 0.4         # V, Potential in working electrode 2 (Substrate)
sens2SECM = 1e-9     # A/V, Currente sesitivity of working electrode 2 (Substrate)
x = 10               # um, Displacement in X 
y = 20               # um, Displacement in Y 
incrdist = 0.05      # um, probe increment distance
incrtime = 0.05      # s, increment time
fileNameSECM = 'SECM' # base file name for probe approach curve

# Experiment:

# approach UME to the substrate
secm.PAC(E1PAC, iratio, sensPAC, maxincr, withdraw, fileNamePAC)
secm.RUN()
secm.MOVE('step', z=-5) # retract to avoid colision with the substrate
# NOTE: To enable bipot is necessary to explicit declare E2= AND sens2=
secm.SECM(secmmode, E1SECM, sens1SECM, x, y, incrdist, incrtime, fileNameSECM, E2=E2SECM, sens2=sens2SECM)
secm.RUN()
