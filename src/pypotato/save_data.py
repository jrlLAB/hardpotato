import numpy as np
import softpotato as sp
import pypotato.mscript as mscript

class Test:
    '''
    '''
    def __init__(self):
        print('Test from save_data module')



class Save:
    '''
    '''
    def __init__(self, data, fileName, header, model, technique, bpot=0):
        self.fileName = fileName
        self.data_array = 0
        if technique == 'CV' or technique == 'LSV':
            header = header + '\nt/s, E/V, i/A\n' 
            self.data_array = CV(fileName, data, model, bpot).save()
        elif technique == 'IT' or technique == 'CA':
            header = header + '\nt/s, E/V, i/A\n'
            self.data_array = IT(fileName, data, model, bpot).save()
        elif technique == 'OCP':
            header = header + '\nt/s, E/V\n'
            self.data_array = OCP(fileName, data, model).save()
        np.savetxt(fileName, self.data_array, delimiter=',', header=header)


class CV:
    '''
    '''
    def __init__(self, fileName, data, model, bpot):
        self.fileName = fileName
        self.data = data
        self.model = model
        self.bpot = bpot
        data_array = 0

    def save(self):
        if self.model == 'emstatpico':
            t = mscript.get_values_by_column(self.data,0)
            E = mscript.get_values_by_column(self.data,1)
            i = mscript.get_values_by_column(self.data,2)
            data_array = np.array([t,E,i]).T
            if self.bpot:
                i2 = mscript.get_values_by_column(self.data,3)
                data_array = np.array([t,E,i,i2]).T

        return data_array



class IT:
    '''
    '''
    def __init__(self, fileName, data, model, bpot):
        self.fileName = fileName
        self.data = data
        self.model = model
        self.bpot = bpot
        data_array = 0

    def save(self):
        if self.model == 'emstatpico':
            t = mscript.get_values_by_column(self.data,0)
            E = mscript.get_values_by_column(self.data,1)
            i = mscript.get_values_by_column(self.data,2)
            data_array = np.array([t,E,i]).T
            if self.bpot:
                i2 = mscript.get_values_by_column(self.data,3)
                data_array = np.array([t,E,i,i2]).T
        return data_array


class OCP:
    '''
    '''
    def __init__(self, fileName, data, model):
        self.fileName = fileName
        self.data = data
        self.model = model
        data_array = 0

    def save(self):
        if self.model == 'emstatpico':
            t = mscript.get_values_by_column(self.data,0)
            E = mscript.get_values_by_column(self.data,1)
            #i = mscript.get_values_by_column(self.data,2)
            data_array = np.array([t,E]).T
        return data_array

