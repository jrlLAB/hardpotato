class Test:
    '''
    '''
    def __init__(self):
        print('Test from chi760e module')


class CV:
    def __init__(self, Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens, 
                 folder, fileName, header, path_lib, qt=2):
        self.fileName = fileName
        self.folder = folder
        self.text = '' 
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
        self.body2 = self.body + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def bipot(self, E2, sens2):
        self.body2 = self.body + \
                    '\ne2=' + str(E2) + '\nsens2=' + str(sens2) + '\ni2on' + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot



class LSV:
    '''
    '''
    def __init__(self, Eini, Efin, sr, dE, sens, folder, fileName, header,
                 path_lib, qt=2):
        self.fileName = fileName
        self.folder = folder
        self.text = ''
        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=lsv\nei=' + str(Eini) + '\nef=' + str(Efin) + \
                    '\nv=' + str(sr) + '\nsi=' + str(dE) + \
                    '\nqt=' + str(qt) + '\nsens=' + str(sens) 
        self.body2 = self.body + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot

    def bipot(self, E2, sens2):
        self.body2 = self.body + \
                    '\ne2=' + str(E2) + '\nsens2=' + str(sens2) + '\ni2on' + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot


class NPV():
    def __init__(self, Eini, Efin, dE, tsample, twidth, tperiod, sens,
                 path_lib, folder, fileName, header, qt=0):
        self.fileName = fileName
        self.folder = folder
        self.text = ''
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


class IT:
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

    def bipot(self, E2, sens2):
        self.body2 = self.body + \
                    '\ne2=' + str(E2) + '\nsens2=' + str(sens2) + '\ni2on' + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\n forcequit: yesiamsure\n'
        self.text = self.head + self.body2 + self.foot



class OCP:
    '''
        Assumes OCP is between +- 10 V
    '''
    def __init__(self, ttot, dt, folder, fileName, header, path_lib):
        self.fileName = fileName
        self.folder = folder
        self.text = ''
        self.head = 'C\x02\0\0\nfolder: ' + folder + '\nfileoverride\n' + \
                    'header: ' + header + '\n\n'
        self.body = 'tech=ocpt\nst=' + str(ttot) + '\neh=10' + \
                    '\nel=-10' + '\nsi=' + str(dt) + \
                    '\nrun\nsave:' + self.fileName + '\ntsave:' + self.fileName 
        self.foot = '\nforcequit: yesiamsure\n'
        self.text = self.head + self.body + self.foot



class Read:
    '''
    '''
    def __init__(self, fileName, folder):
        self.fileName = fileName
        self.folder = folder

