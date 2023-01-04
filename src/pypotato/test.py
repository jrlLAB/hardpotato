import potentiostat

model = 'chi760e'
path = '.'
folder = 'data'

#print(potentiostat.models_available)
info = potentiostat.Info(model)
info.specifications()


potentiostat.Setup(model, path, folder)

cv = potentiostat.LSV(Eini=1)
#cv.bipot()
#cv.run()

#lsv = potentiostat.LSV(sr=0.5)
#lsv.bipot()
#lsv.run()

#ca = potentiostat.CA()
#ca.bipot()
#ca.run()

#ocp = potentiostat.OCP()
#ocp.run()
