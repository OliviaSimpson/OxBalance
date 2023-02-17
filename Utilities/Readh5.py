import h5py
from Loader import DataLoader
import numpy as np
import pandas as pd



class h5_handler():

    def __init__(self, source) -> None:
       self.set_source(source)
       self.open_file()


    def set_source(self, source):
        self.source = source

    def open_file(self):
        self.datafile = h5py.File(self.source, 'r')
        print(list(self.datafile.keys()))
        print(list(self.datafile.keys())[-1])
    
    def close_file(self):
        self.datafile.close()
    
    def get_subject_list(self, key):
        print(self.datafile)
        # hdf = pd.HDFStore(self.source, mode='r')
        subjectlist = pd.read_hdf(self.source, key=list(self.datafile.keys())[-1], mode='r')
        return(subjectlist)


def createdummydata():
    hdf = pd.HDFStore('dummy_h5.h5')
    write_data = pd.DataFrame(np.random.rand(5,3))
    hdf.put('key1', write_data)
    write_2_data = pd.DataFrame(np.random.rand(3,3))
    hdf.put('key2', write_2_data)
    write_3_data = pd.DataFrame(np.random.rand(7,7))
    hdf.put('key3', write_3_data)
    hdf.close()



source = DataLoader().data_file_path

trialdata = h5_handler(source)
print(trialdata.get_subject_list('key1'))
print(trialdata.get_subject_list('key2'))
print(trialdata.get_subject_list('key3'))
trialdata.close_file()
