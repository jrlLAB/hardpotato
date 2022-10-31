import potentiostat

model = 'emstatpico'
path = '.'
folder = 'data'
potentiostat.Setup(model, path, folder)

#cv = potentiostat.CV(sr=0.5)
#cv.bipot()
#cv.run()

lsv = potentiostat.LSV(sr=0.5)
lsv.bipot()
lsv.run()

#ca = potentiostat.CA()
#ca.bipot()
#ca.run()

#ocp = potentiostat.OCP()
#ocp.run()
