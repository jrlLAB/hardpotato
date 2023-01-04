class Test:
    '''
    '''
    def __init__(self):
        print('Test from chi760e translator')

class Info:
    '''
        Pending:
        * Calculate dE, sr, dt, ttot, mins and max
    '''
    def __init__(self):
        self.tech = ['CV', 'CA', 'LSV', 'OCP', 'NPV', 'EIS']
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
        print('Model: CH Instruments 760E (chi760e)')
        print('Techiques available:', self.tech)
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
        #info.limits(sens, info.senC:\Users\oliverrz\Desktop\CHI\chi760es_min, info.sens_max, 'sens', 'A/V')

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



class NPV():
    def __init__(self, Eini, Efin, dE, tsample, twidth, tperiod, sens,
                 path_lib, folder, fileName, header, **kwargs):
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2

        print('NPV technique still in development. Use with caution.')

        self.validate(Eini, Efin, dE, tsample, twidth, tperiod, sens)

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\n' + fileOverride + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=NPV\nei=' + str(Eini) + '\nef=' + str(Efin) + \
                    '\nincre=' + str(dE) + '\npw=' + str(tsample) + \
                    '\nsw=' + str(twidth) + '\nprod=' + str(tperiod) + \
                    '\nqt=' + str(qt) + '\nsens=' + str(sens)
        self.body = self.body + \
                    '\nrun\nsave:' + fileName + '\ntsave:' + fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot

    def validate(self, Eini, Efin, dE, tsample, twidth, tperiod, sens):
        info = Info()
        info.limits(Eini, info.E_min, info.E_max, 'Eini', 'V')
        info.limits(Efin, info.E_min, info.E_max, 'Efin', 'V')
        #info.limits(tsample, info.tsample)
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

class EIS:
    '''
        Pending:
        * Validate parameters
    '''
    def __init__(self, Eini, low_freq, high_freq, amplitude, sens, folder, 
                 fileName, header, path_lib, **kwargs):
        print('EIS technique is still in development. Use with caution.')
        self.fileName = fileName
        self.folder = folder
        self.text = ''

        if 'qt' in kwargs:
            qt = kwargs.get('qt')
        else:
            qt = 2 

        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=imp\nei=' + str(Eini) + '\nfl=' + str(low_freq) + \
                    '\nfh=' + str(high_freq) + '\namp=' + str(amplitude) + \
                    '\nsens=' + str(sens) + '\nqt=' + str(qt) + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\nforcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot


