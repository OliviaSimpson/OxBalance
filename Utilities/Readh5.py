import h5py
from Loader import DataLoader
import numpy as np
import pandas as pd



class h5_handler():

    def __init__(self, source,verbose=False) -> None:
        self.verbose = verbose
        self.set_source(source)
        self.open_file()
        self.subjectlist = None

    def set_source(self, source):
        self.source = source

    def open_file(self):
        self.datafile = h5py.File(self.source, 'r')
        print(list(self.datafile.keys()))
        print(list(self.datafile.keys())[-1])
    
    def close_file(self):
        self.datafile.close()
    
    def get_subject_list(self):
        print(self.datafile)
        # hdf = pd.HDFStore(self.source, mode='r')
        self.subjectlist = pd.read_hdf(self.source, key=list(self.datafile.keys())[-1], mode='r')
        return(self.subjectlist)
    
    def subject_code_from_index(self, index):
        if type(self.subjectlist) == None:
            self.get_subject_list()
        if self.verbose is True:
            print(f"Subject code: {self.subjectlist.iloc[index].tolist()}")
        return self.subjectlist.iloc[index]
    
    def subject_index_from_code(self, code):
        if type(self.subjectlist) == None:
            self.get_subject_list()
        SubjectIndex = self.subjectlist.index[self.subjectlist['subject'] == code].tolist()
        if self.verbose is True:
            if len(SubjectIndex) == 1:
                print(f"One subject index result: {SubjectIndex}")
            elif len(SubjectIndex) == 0:
                print(f"No subject index results")
            else:
                print(f"Multiple subject index results: {SubjectIndex}")
        return SubjectIndex


def createdummydata():
    hdf = pd.HDFStore('dummy_h5.h5')
    hdf.put('abcd', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('abcd/active_test_info', pd.DataFrame(np.random.rand(2,1)))
    hdf.put('abcd/smartphone_device_location', pd.DataFrame(np.random.rand(6,1)))
    hdf.put('abcd/smartphone:A/testid:0/device_id:a/acc', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('efgh', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('ijkl', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('mnop', pd.DataFrame(np.random.rand(3,3)))
    slist = pd.DataFrame(['abcd', 'key2', 'key3', 'key4'], columns=['subject'])
    hdf.put('subjectlist', slist)
    hdf.close()


createdummydata()
source = DataLoader().data_file_path

trialdata = h5_handler(source, verbose=True)
print(trialdata.get_subject_list())
trialdata.close_file()
trialdata.subject_code_from_index(1)
trialdata.subject_index_from_code('key2')
