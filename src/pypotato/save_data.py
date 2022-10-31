import numpy as np
import softpotato as sp
import palmsens.mscript

class Test:
    '''
    '''
    def __init__(self):
        print('Test from save_data module')



class Save:
    '''
    '''
    def __init__(self, data, fileName, header, model, technique):
        self.fileName = fileName
        self.data_array = 0
        if technique == 'CV':
            header = header + '\nt/s, E/V, i/A\n' 
            self.data_array = CV(fileName, data, model).save()
        elif technique == 'IT':
            header = header + '\nt/s, E/V, i/A\n'
            self.data_array = IT(fileName, data, model).save()
        np.savetxt(fileName, self.data_array, delimiter=',', header=header)


class CV(Save):
    '''
    '''
    def __init__(self, fileName, data, model):
        self.fileName = fileName
        self.data = data
        self.model = model
        data_array = 0

    def save(self):
        if self.model == 'emstatpico':
            t = palmsens.mscript.get_values_by_column(self.data,0)
            E = palmsens.mscript.get_values_by_column(self.data,1)
            i = palmsens.mscript.get_values_by_column(self.data,2)
            data_array = np.array([t,E,i]).T
            #sp.plotting.plot(E,i,fileName=self.fileName.replace('.txt',''))
        return data_array


class IT(Save):
    '''
    '''
    def __init__(self, fileName, data, model):
        self.fileName = fileName
        self.data = data
        self.model = model
        data_array = 0

    def save(self):
        if self.model == 'emstatpico':
            t = palmsens.mscript.get_values_by_column(self.data,0)
            E = palmsens.mscript.get_values_by_column(self.data,1)
            i = palmsens.mscript.get_values_by_column(self.data,2)
            data_array = np.array([t,E,i]).T
            #sp.plotting.plot(t,i,xlab='$t$ / s',fileName=self.fileName.replace(
            #                '.txt',''))
        return data_array
