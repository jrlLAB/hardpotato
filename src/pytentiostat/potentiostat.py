import os
import pytentiostat.chi760e as chi

# Potentiostat models available: chi760e

# Global variables
folder_save = '.'
model_pstat = 'no pstat'
path_lib = '.'

class Setup:
    def __init__(self, model=0, path='.', folder='.', verbose=1):
        global folder_save
        folder_save = folder
        global model_pstat
        model_pstat = model
        global path
        path_lib = path
        if verbose:
            self.info()

    def info(self):
        print('\n----------')
        print('Potentiostat model: ' + model_pstat)
        print('Potentiostat path: ' + path)
        print('Save folder: ' + folder_save)
        print('----------\n')


class Technique:
    '''
    '''

    def __init__(self, text='', fileName='CV'):
        self.text = text
        self.fileName = fileName
        self.technique = 'Technique'
        self.bpot = False

    def writeToFile(self):
        if model_pstat == 'chi760e':
            file = open(folder_save + '/' + self.fileName + '.mcr', 'wb')
            file.write(self.text.encode('ascii'))
            file.close()

    def run(self):
        if model_pstat == 'chi760e':
            self.message()
            # Write macro:
            self.writeToFile()
            # Run command:
            command = path_lib + '/chi760e.exe'
            param = ' /runmacro:\"' + folder_save + '/' + self.fileName + '.mcr\"'
            os.system(command + param)
            self.message(start=False)
        else:
            print('\nNo potentiostat selected. Aborting.')

    def message(self, start=True):
        if start:
            print('----------\nStarting ' + self.technique)
            if self.bpot:
                print('Running in bipotentiostat mode')
        else:
            print(self.technique + ' finished\n----------\n')

    def bipot(self, E=-0.5, sens=1e-6):
        if self.technique != 'OCP':
            if model_pstat == 'chi760e':
                self.tech.bipot(E, sens)
                self.text = self.tech.text
                self.bpot = True
        else:
            print('OCP does not have bipotentiostat mode')
     

class CV(Technique):
    '''
    '''
    def __init__(self, Eini=-0.2, Ev1=0.2, Ev2=-0.2, Efin=-0.2, sr=0.1,
                 dE=0.001, nSweeps=2, sens=1e-6, 
                 fileName='CV', header='CV'):
        if model_pstat == 'chi760e':
            self.tech = chi.CV(Eini, Ev1, Ev2, Efin, sr, dE, nSweeps, sens,
                          folder_save, fileName, header, path_lib, qt=2)
            Technique.__init__(self, text=self.tech.text, fileName=fileName)
            self.technique = 'CV'
            print('CV')

class NPV(Technique):
    '''
    '''
    def __init__(self, Eini=0.5, Efin=-0.5, dE=0.01, tsample=0.1, twidth=0.05, tperiod=10, sens=1e-6,
                 fileName='NPV', header='NPV performed with CHI760'):
        if model_pstat == 'chi760e':
            self.tech = chi.NPV(Eini, Efin, dE, tsample, twidth, tperiod, sens,
                         folder_save, fileName, header, path_lib, qt=0)
            Technique.__init__(self, text=self.tech.text, fileName=fileName)
            self.technique = 'NPV'
            print('NPV')

    


class LSV(Technique):
    '''
    '''
    def __init__(self, Eini=-0.2, Efin=0.2, sr=0.1, dE=0.001, sens=1e-6,
                 fileName='LSV', header='LSV'):
        if model_pstat == 'chi760e':
            self.tech = chi.LSV(Eini, Efin, sr, dE, sens, folder_save, fileName, 
                                header, path_lib, qt=2)
            Technique.__init__(self, text=self.tech.text, fileName=fileName)
            self.technique = 'LSV'  


class IT(Technique):
    '''
    '''
    def __init__(self, Estep=0.2, dt=0.001, ttot=2, sens=1e-6,
                 fileName='IT', header='IT'):
        if model_pstat == 'chi760e':
            self.tech = chi.IT(Estep, dt, ttot, sens, folder_save, fileName,
                               header, path_lib, qt=2)
            Technique.__init__(self, text=self.tech.text, fileName=fileName)
            self.technique = 'IT'



class OCP(Technique):
    '''
    '''
    def __init__(self, ttot=2, dt=0.01, fileName='OCP', header='OCP'):
        if model_pstat == 'chi760e':
            self.tech = chi.OCP(ttot, dt, folder_save, fileName, header, path_lib)
            Technique.__init__(self, text=self.tech.text, fileName=fileName)
            self.technique = 'OCP'



if __name__ == '__main__':
    sens = 1e-8
    sr = [0.1, 0.2, 0.5]
    folder = 'C:/Users/oliverrz/Desktop/Oliver/Data/220113_PythonMacros'
