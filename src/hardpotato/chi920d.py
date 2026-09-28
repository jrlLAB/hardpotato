class Test:
    '''
    '''
    def __init__(self):
        print('Test from chi920d translator')

class Info:
    '''
        Pending:
        * Calculate dE, sr, dt, ttot, mins and max
    '''
    def __init__(self):
        self.tech = ['CV', 'CA', 'LSV', 'OCP']
        self.secmTech = ['MOVE', 'CV', 'PAC', 'PSC']
        self.options = [
                        'Quiet time in s (qt)', 
                        'Resistance in ohms (resistance)'
                        ]

        self.E_min = -10
        self.E_max = 10
        self.sr_min = 0.000001
        self.sr_max = 10000
        #self.dE_min = 
        #self.sr_min = 
        #self.dt_min = 
        #self.dt_max = 
        #self.ttot_min = 
        #self.ttot_max = 
        self.freq_min = 0.00001
        self.freq_max = 1000000

    def limits(self, val, low, high, label, units):
        if val < low or val > high:
            raise Exception(label + ' should be between ' + str(low) + ' ' +\
                            units  + ' and ' + str(high) + ' ' + units +\
                            '. Received ' + str(val) + ' ' + units)

    def specifications(self):
        print('Model: CH Instruments 920D (chi920d)')
        print('Techniques available:', self.tech)
        print('SECM techniques avaible:', self.secmTech)
        print('Options available:', self.options)

class CV:
    '''
        **kwargs:
            qt # s, quite time
            resistance # ohms, solution resistance
    '''
    def __init__(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens, 
                 folder, fileName, header, path_lib, **kwargs):
        self.fileName = fileName
        self.folder = folder
        self.text = '' 

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0

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
        nSweeps = nSweeps + 1 # final e from chi is enabled by default

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

    def bipot(self, E, sens):
        # Validate bipot:
        info = Info()
        info.limits(E, info.E_min, info.E_max, 'E2', 'V')
        #info.limits(sens, info.senC:\Users\oliverrz\Desktop\CHI\chi920ds_min, info.sens_max, 'sens', 'A/V')

        self.body2 = self.body + \
                    '\ne2=' + str(E) + '\nsens2=' + str(sens) + '\ni2on' + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
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

class CA:
    '''
    '''
    def __init__(self, Estep, dt, ttot, sens, folder, fileName, header, 
                 path_lib, **kwargs):
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=i-t\nei=' + str(Estep) + '\nst=' + str(ttot) + \
                    '\nsi=' + str(dt) + '\nqt=' + str(qt) + \
                    '\nsens=' + str(sens) 
        if resistance: # In case IR compensation is required
            self.body2 = self.body + '\nmir=' + str(resistance) + \
                         '\nircompon\nrun\nircompoff\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        else:
            self.body2 = self.body + '\nrun\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

        self.validate(Estep, dt, ttot, sens)


    def validate(self, Estep, dt, ttot, sens):
        info = Info()
        info.limits(Estep, info.E_min, info.E_max, 'Estep', 'V')
        #info.limits(dt, info.dt_min, info.dt_max, 'dt', 's')
        #info.limits(ttot, info.ttot_min, info.ttot_max, 'ttot', 's')
        #info.limits(sens, info.sens_min, info.sens_max, 'sens', 'A/V')

    def bipot(self, E, sens):
        # Validate bipot:
        info = Info()
        info.limits(E, info.E_min, info.E_max, 'E2', 'V')
        #info.limits(sens, info.sens_min, info.sens_max, 'sens2', 'A/V')
        self.body2 = self.body + \
                    '\ne2=' + str(E) + '\nsens2=' + str(sens) + '\ni2on' + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

class LSV:
    '''
        **kwargs:
            qt # s, quiet time
            resistance # ohms, solution resistance
    '''
    def __init__(self, Eini, Efin, sr, dE, sens, folder, fileName, header,
                 path_lib, **kwargs):
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0
        
        self.validate(Eini, Efin, sr, dE, sens)

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=lsv\nei=' + str(Eini) + '\nef=' + str(Efin) + \
                    '\nv=' + str(sr) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nsens=' + str(sens) 
        if resistance: # In case IR compensation is required
            self.body2 = self.body + '\nmir=' + str(resistance) + \
                         '\nircompon\nrun\nircompoff\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName
        else:
            self.body2 = self.body + '\nrun\nsave:' + self.fileName + \
                         '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def bipot(self, E, sens):
        # Validate bipot:
        info = Info()
        info.limits(E, info.E_min, info.E_max, 'E2', 'V')
        #info.limits(sens, info.sens_min, info.sens_max, 'sens', 'A/V')

        self.body2 = self.body + \
                    '\ne2=' + str(E) + '\nsens2=' + str(sens) + '\ni2on' + \
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

class OCP:
    '''
        Assumes OCP is between +- 10 V
    '''
    def __init__(self, ttot, dt, folder, fileName, header, path_lib, **kwargs):
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0 

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=ocpt\nst=' + str(ttot) + '\neh=10' + \
                    '\nel=-10' + '\nsi=' + str(dt) + '\nqt=' + str(qt) +\
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\nforcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot

        self.validate(ttot, dt)

    def validate(self, ttot, dt):
        info = Info()
        #info.limits(dt, info.dt_min, info.dt_max, 'dt', 's')
        #info.limits(ttot, info.ttot_min, info.ttot_max, 'ttot', 's')

class SECM:
    '''
    Permits to creat .mcr file with option of move commends
    SECM.MOVE('step', x=10)
    SECM.CV()
    SECM.RUN()

    or

    CV()
    run()
    '''

    def __init__(self):
        global model_pstat
        global folder_save

    def MOVE(self, motor = 'step', x=0, y=0, z=0):
        text = ''
        if motor == 'step':
            text = 'x=' + str(x) +  '\ny=' + str(y) + '\nz=' + str(z) + '\n'
        elif motor == 'piezo':
            text = 'xx=' + str(x) + '\nyy=' + str(y) + '\nzz=' + str(z) + '\n'
        return text
    
    def CV(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens,
           fileName, **kwargs):
        self.fileName = fileName
        text = ''
        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2

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
        nSweeps = nSweeps + 1 # final e from chi is enabled by default

        # building macro:
        self.body = 'tech=cv\nei=' + str(Ei) + '\neh=' + str(eh) + '\nel=' + \
                    str(el) + '\npn=' + pn + '\ncl=' + str(nSweeps) + \
                    '\nefon\nef=' + str(Efin) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nv=' + str(sr) + '\nsens=' + str(sens)
        if 'resistance' in kwargs: # In case IR compensation is required
            resistance = kwargs.get('resistance')
            self.body += '\nmir=' + str(resistance) + \
                         '\nircompon'
        if 'E2' and 'sens2' in kwargs:
            E2 = kwargs.get('E2')
            sens2 = kwargs.get('sens2')
            self.body += '\ne2=' + str(E2) + '\nsens2=' + str(sens2) + \
                         '\ne2on\ni2on'
        else:
            pass
        runTurnOffSave = '\nrun\ne2off\ni2off\nircompoff\nsave:' + self.fileName + '\ntsave:' + self.fileName
        text = self.body + runTurnOffSave
        return text

    def CA(self, Estep, dt, ttot, sens,
           fileName, **kwargs):
        self.fileName = fileName
        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=i-t\nei=' + str(Estep) + '\nst=' + str(ttot) + \
                    '\nsi=' + str(dt) + '\nqt=' + str(qt) + \
                    '\nsens=' + str(sens) 
        if 'resistance' in kwargs: # In case IR compensation is required
            resistance = kwargs.get('resistance')
            self.body += '\nmir=' + str(resistance) + \
                         '\nircompon'
        if 'E2' and 'sens2' in kwargs:
            E2 = kwargs.get('E2')
            sens2 = kwargs.get('sens2')
            self.body += '\ne2=' + str(E2) + '\nsens2=' + str(sens2) + \
                         '\ne2on\ni2on'
        else:
            pass
        runTurnOffSave = '\nrun\ne2off\ni2off\nircompoff\nsave:' + self.fileName + '\ntsave:' + self.fileName
        text = self.body + runTurnOffSave
        return text

    def LSV(self, Eini, Efin, sr, dE, sens,
            fileName, **kwargs):
        self.fileName = fileName
        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0
        
        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=lsv\nei=' + str(Eini) + '\nef=' + str(Efin) + \
                    '\nv=' + str(sr) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nsens=' + str(sens) 
        if resistance: # In case IR compensation is required
            resistance = kwargs.get('resistance')
            self.body += '\nmir=' + str(resistance) + \
                         '\nircompon'
        if 'E2' and 'sens2' in kwargs:
            E2 = kwargs.get('E2')
            sens2 = kwargs.get('sens2')
            self.body += '\ne2=' + str(E2) + '\nsens2=' + str(sens2) + \
                         '\ne2on\ni2on'
        else:
            pass
        runTurnOffSave = '\nrun\ne2off\ni2off\nircompoff\nsave:' + self.fileName + '\ntsave:' + self.fileName
        text = self.body + runTurnOffSave
        return text

    def OCP(self, ttot, dt,
            fileName, **kwargs):
        self.fileName = fileName
        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        if 'resistance' in kwargs:
            resistance = kwargs.get('resistance')
        else:
            resistance = 0 

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=ocpt\nst=' + str(ttot) + '\neh=10' + \
                    '\nel=-10' + '\nsi=' + str(dt) + '\nqt=' + str(qt) 
        runTurnOffSave = '\nrun\ne2off\ni2off\nircompoff\nsave:' + self.fileName + '\ntsave:' + self.fileName
        text = self.body + runTurnOffSave
        return text
    
    def PSC(self, E1, dir, dist, sens, incrdist, incrtime,
            fileName, **kwargs):
        self.fileName = fileName
        text = ''
        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        self.body = 'tech=psc\nei=' + str(E1) + '\ndir=' + str(dir) + '\ndist=' + str(dist) + '\nsens=' + \
            str(sens) + '\nincrdist=' + str(incrdist) + '\nincrtime=' + str(incrtime) + \
            '\nqt=' + str(qt)
        if 'resistance' in kwargs: # In case IR compensation is required
            resistance = kwargs.get('resistance')
            self.body += '\nmir=' + str(resistance) + \
                         '\nircompon'
        if 'E2' and 'sens2' in kwargs:
            E2 = kwargs.get('E2')
            sens2 = kwargs.get('sens2')
            self.body += '\ne2=' + str(E2) + '\nsens2=' + str(sens2) + \
                         '\ne2on\ni2on'
        else:
            pass
        runTurnOffSave = '\nrun\ne2off\ni2off\nircompoff\nsave:' + self.fileName + '\ntsave:' + self.fileName
        text = self.body + runTurnOffSave
        return text

    def PAC(self, E1, iratio, sens, maxincr, withdraw,
            fileName, **kwargs):
        self.fileName = fileName
        text = ''
        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        self.body = 'tech=pac\nei=' + str(E1) + '\niratio=' + str(iratio) + '\nsens=' + \
            str(sens) + '\nmaxincr=' + str(maxincr) + '\nwithdraw=' + str(withdraw) + '\nqt=' + str(qt)
        if 'resistance' in kwargs: # In case IR compensation is required
            resistance = kwargs.get('resistance')
            self.body += '\nmir=' + str(resistance) + \
                         '\nircompon'
        if 'E2' and 'sens2' in kwargs:
            E2 = kwargs.get('E2')
            sens2 = kwargs.get('sens2')
            self.body += '\ne2=' + str(E2) + '\nsens2=' + str(sens2) + \
                         '\ne2on\ni2on'
        else:
            pass
        runTurnOffSave = '\nrun\ne2off\ni2off\nircompoff\nsave:' + self.fileName + '\ntsave:' + self.fileName
        text = self.body + runTurnOffSave
        return text

    def SECM(self, secmmode, E1, sens, xdist, ydist, incrdist, incrtime,
             fileName, **kwargs):
        self.fileName = fileName
        text = ''
        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2
        self.body = 'tech=secm\nei=' + str(E1) + '\nsens=' + str(sens) + \
            '\nsecmmode='+ str(secmmode) + '\nxdist=' + str(xdist) + '\nydist=' + str(ydist) + \
            '\nincrdist=' + str(incrdist) + '\nincrtime=' + str(incrtime) + \
            '\nqt=' + str(qt) + '\noriginon'
        if 'resistance' in kwargs: # In case IR compensation is required
            resistance = kwargs.get('resistance')
            self.body += '\nmir=' + str(resistance) + \
                         '\nircompon'
        if 'E2' and 'sens2' in kwargs:
            E2 = kwargs.get('E2')
            sens2 = kwargs.get('sens2')
            self.body += '\ne2=' + str(E2) + '\nsens2=' + str(sens2) + \
                         '\ne2on\ni2on'
        else:
            pass
        runTurnOffSave = '\nrun\ne2off\ni2off\nircompoff\nsave:' + self.fileName + '\ntsave:' + self.fileName
        text = self.body + runTurnOffSave
        return text