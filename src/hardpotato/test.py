import potentiostat

model = 'chi920d'
path = r"C:\Users\parasita\Downloads\chi920d\chi920d.exe"
folder = 'data'

#print(potentiostat.models_available)
info = potentiostat.Info(model)
info.specifications()

Eini = -0.5     # V, initial potential
Ev1 = 0.5       # V, first vertex potential
Ev2 = -0.5      # V, second vertex potential
Efin = -0.5     # V, final potential
sr = 0.1        # V/s, scan rate
dE = 0.001      # V, potential increment
nSweeps = 2     # number of sweeps
sens = 1e-4     # A/V, current sensitivity
e2 = 0.0        # V, potential of the second working electrode
sens2 = 1e-9    # A/V, current sensitivity of the second working electrode
fileName = 'CV' # base file name for data file
header = 'CV'   # header for data file

potentiostat.Setup(model, path, folder)
secm = potentiostat.SECM()
# secm.MOVE('step', z=-150)
secm.CV(Eini, Ev1,Ev2, Efin, sr, dE, nSweeps, sens, fileName, header, E2=e2, sens2=sens2)
# secm.PAC(E1=0.4, qt = 30, sens=1e-9, maxincr=0.5, iratio=80, fileName='10092026_PAC_before_tests')
secm.RUN()
# stepx = 1
# stepy = 5
# sizex= 3
# sizey= 15
# currentx = 0
# currenty = 0
# for x in range (0,sizex,stepx):
#     for y in range (0, sizey, stepy):
#         dx = x - currentx
#         currentx = x
#         dy = y - currenty
#         currenty = y
#         pacFileName = f'PAC_x{x}_y{y}'
#         secm.MOVE('step', x=dx, y=dy, z=-150)
#         # secm.CV(sr=0.5)
#         secm.PAC(E2=-0.4, sens2=0.3, resistance=100, fileName=pacFileName)
#         secm.RUN()
#         cvFileName = f'CV_x{x}_y{y}'
#         secm.CV(fileName=cvFileName)
#         secm.RUN()
#cv.bipot()


# lsv = potentiostat.LSV(sr=0.5)
# lsv.bipot()
# lsv.run()

# ca = potentiostat.CA()
# ca.bipot()
# ca.run()

#ocp = potentiostat.OCP()
#ocp.run()
