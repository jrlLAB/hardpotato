class Test:
    '''
    '''
    def __init__(self):
        print('Test from chi1205b translator')


class Info:
    '''
        Pending:
        * Calculate dE, sr, dt, ttot, mins and max
    '''
    def __init__(self):
        self.tech = ['CV', 'CA', 'LSV', 'OCP']

        self.E_min = -2.4
        self.E_max = 2.4
        self.sr_min = 0.000001
        self.sr_max = 10
        #self.dE_min = 
        #self.sr_min = 
        #self.dt_min = 
        #self.dt_max = 
        #self.ttot_min = 
        #self.ttot_max = 

    def limits(self, val, low, high, label, units):
        if val < low or val > high:
            raise Exception(label + ' should be between ' + str(low) + ' ' +\
                            units  + ' and ' + str(high) + ' ' + units +\
                            '. Received ' + str(val) + ' ' + units)

    def techniques(self):
        print('Model: CH Instruments 1205b (chi1205b)')
        print('Techiques available:', self.tech)

    def specifications(self):
        print('Specifications list')


class CV:
    def __init__(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens, 
                 folder, fileName, header, path_lib, qt=2, resistance=0):
        self.fileName = fileName
        self.folder = folder
        self.text = '' 

        self.validate(Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens)

        # correcting parameters:
        Ei = Eini
        if Ev1 > Ev2:
            eh = Ev1
            el = Ev2
            pn = 'p'
        else:
            eh = Ev2
            el = Ev1
            pn = 'n'
        #nSweeps = nSweeps + 1 # final e from chi is enabled by default

        # building macro:
        self.head = 'c\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=cv\nei=' + str(Ei) + '\neh=' + str(eh) + '\nel=' + \
                    str(el) + '\npn=' + pn + '\ncl=' + str(nSweeps) + \
                    '\nefon\nef=' + str(Efin) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nv=' + str(sr) + '\nsens=' + str(sens)
        if resistance: # In case IR compensation is required
            self.body2 = self.body + '\nmir=' + str(resistance) + \
                         '\nircompon\nrun\nircompoff\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        else:
            self.body2 = self.body + '\nrun\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def validate(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens):
        info = Info()
        info.limits(Eini, info.E_min, info.E_max, 'Eini', 'V')
        info.limits(Ev1, info.E_min, info.E_max, 'Ev1', 'V')
        info.limits(Ev2, info.E_min, info.E_max, 'Ev2', 'V')
        info.limits(Efin, info.E_min, info.E_max, 'Efin', 'V')
        info.limits(sr, info.sr_min, info.sr_max, 'sr', 'V/s')
        #info.limits(dE, info.dE_min, info.dE_max, 'dE', 'V')
        #info.limits(sens, info.sens_min, info.sens_max, 'sens', 'A/V')
        print('All the parameters are valid')


class LSV:
    '''
    '''
    def __init__(self, Eini, Efin, sr, dE, sens, folder, fileName, header,
                 path_lib, qt=2):
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        self.validate(Eini, Efin, sr, dE, sens)

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=lsv\nei=' + str(Eini) + '\nef=' + str(Efin) + \
                    '\nv=' + str(sr) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nsens=' + str(sens) 
        self.body2 = self.body + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def validate(self, Eini, Efin, sr, dE, sens):
        info = Info()
        info.limits(Eini, info.E_min, info.E_max, 'Eini', 'V')
        info.limits(Efin, info.E_min, info.E_max, 'Efin', 'V')
        info.limits(sr, info.sr_min, info.sr_max, 'sr', 'V/s')
        #info.limits(dE, info.dE_min, info.dE_max, 'dE', 'V')
        #info.limits(sens, info.sens_min, info.sens_max, 'sens', 'A/V')
        print('All the parameters are valid')



class CA:
    '''
    '''
    def __init__(self, Estep, dt, ttot, sens, folder, fileName, header, 
                 path_lib, qt=2):
        self.fileName = fileName
        self.folder = folder
        self.text = ''
        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=i-t\nei=' + str(Estep) + '\nst=' + str(ttot) + \
                    '\nsi=' + str(dt) + '\nqt=' + str(qt) + \
                    '\nsens=' + str(sens) 
        self.body2 = self.body + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

        self.validate(Estep, dt, ttot, sens)


    def validate(self, Estep, dt, ttot, sens):
        info = Info()
        info.limits(Estep, info.E_min, info.E_max, 'Estep', 'V')
        #info.limits(dt, info.dt_min, info.dt_max, 'dt', 's')
        #info.limits(ttot, info.ttot_min, info.ttot_max, 'ttot', 's')
        #info.limits(sens, info.sens_min, info.sens_max, 'sens', 'A/V')
        print('All the parameters are valid')



class OCP:
    '''
        Assumes OCP is between +- 10 V
    '''
    def __init__(self, ttot, dt, folder, fileName, header, path_lib):
        self.ttot = ttot
        self.dt = dt

        self.validate(ttot, dt)

        self.fileName = fileName
        self.folder = folder
        self.text = ''
        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=ocpt\nst=' + str(ttot) + '\neh=5' + \
                    '\nel=-5' + '\nsi=' + str(dt) + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\nforcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot

    def validate(self, ttot, dt):
        info = Info()
        #info.limits(dt, info.dt_min, info.dt_max, 'dt', 's')
        #info.limits(ttot, info.ttot_min, info.ttot_max, 'ttot', 's')
        print('All the parameters are valid')

