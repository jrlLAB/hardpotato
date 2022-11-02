import numpy as np
import pypotato.chi760e as chi


class Test:
    '''
    '''
    def __init__(self):
        print('Test from load_data module')

class Read:
    '''
    '''
    def __init__(self):
        self.file_path = self.folder + '/' + self.fileName

    def read(self, text=0, model=0):
        self.delimiter = ','
        if model[0:3] == 'chi':
            self.skiprows = self.search(text)
            if self.skiprows:
                self.data = np.loadtxt(self.file_path, delimiter=self.delimiter, 
                            skiprows=self.skiprows)
                self.E = self.data[:,0]
                self.i = -self.data[:,1:]
            else:
                print('Could not find string \"' + text + '\" to skip rows.' +\
                      ' Data not loaded.')
                self.x = np.array([])
                self.y = np.array([])
        elif model == 'emstatpico':
            #print('pico')
            self.data = np.loadtxt(self.file_path, delimiter=self.delimiter)
            self.t = self.data[:,0]
            self.E = self.data[:,1]
            self.i = self.data[:,2:]
        else:
            self.data = np.loadtxt(self.file_path, delimiter=self.delimiter, 
                        skiprows=self.skiprows)
            self.E = self.data[:,0]
            self.i = self.data[:,1:]

    def search(self, text):
        file = open(self.file_path, 'r')
        count = 0
        flag = 0
        for line in file:
            count += 1
            if text in line:
                return count
        return 0



class XY(Read):
    '''
    '''
    def __init__(self, fileName='file', folder='.', skiprows=0, delimiter=',',
                 model=0): 
        self.fileName = fileName
        self.folder = folder
        Read.__init__(self)
        self.skiprows = skiprows
        self.delimiter = delimiter
        self.read()


class CV(Read):
    '''
    '''
    def __init__(self, fileName='file', folder='.', model=0):
        #print(model)
        self.fileName = fileName
        self.folder = folder
        text = 'Potential/V,'
        Read.__init__(self)
        self.read(text, model)
        #self.E = self.x
        #self.i = self.y


class LSV(Read):
    '''
    '''
    def __init__(self, fileName='file', folder='.', model=0):
        cv = CV(fileName, folder, model) # Same as CV
        self.E = cv.E
        self.i = cv.i


class CA(Read):
    '''
    '''
    def __init__(self, fileName='file', folder='.', model=0):
        self.fileName = fileName
        self.folder = folder
        text = 'Time/sec,'
        Read.__init__(self)
        self.read(text, model)
        self.t = self.E
        #self.E = self.E
        self.i = self.i


class OCP(Read):
    '''
    '''
    def __init__(self, fileName='file', folder='.', model=0):
        ca = CA(fileName, folder, model) # Same as CA
        self.t = ca.t
        self.E = ca.i
