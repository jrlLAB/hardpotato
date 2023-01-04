import pypotato as pp

pot = 3

if pot == 1:
    model = 'chi1205b'
    path = 'C:/Users/oliverrz/Desktop/CHI/chi1205b_mini2/chi1205b.exe'
    sens = 1e-4
elif pot == 2:
    model = 'chi760e'
    path = 'C:/Users/oliverrz/Desktop/CHI/chi760e/chi760e.exe'    
    sens = 1e-7
elif pot == 3:
    model = 'emstatpico'
    path = ''
    sens=1e-7    

folder = 'data'

#print(potentiostat.models_available)
info = pp.potentiostat.Info(model)
info.specifications()


pp.potentiostat.Setup(model, path, folder)

fileName = model + '_CV'
cv = pp.potentiostat.CV(sens=sens, fileName=fileName, qt=2, resistance=10)
cv.bipot()
cv.run()

fileName = model + '_LSV'
lsv = pp.potentiostat.LSV(sens=sens, fileName=fileName, qt=2, resistance=10)
lsv.bipot()
lsv.run()

fileName = model + '_CA'
ca = pp.potentiostat.CA(sens=sens, fileName=fileName, qt=2, resistance=10)
ca.bipot()
ca.run()

fileName = model + '_OCP'
ocp = pp.potentiostat.OCP(fileName=fileName, qt=2, resistance=10)
ocp.run()
