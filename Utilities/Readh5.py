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
        # print(list(self.datafile.keys()))
        # print(list(self.datafile.keys())[-1])
        # print(list(self.datafile[subjectID].keys()))
        # print(list(self.datafile[subjectID]['smartphone'].keys()))
    
    def close_file(self):
        self.datafile.close()
    
    def get_subject_list(self):
        print(self.datafile)
        # hdf = pd.HDFStore(self.source, mode='r')
        self.subjectlist = pd.read_hdf(self.source, key=list(self.datafile.keys())[-1], mode='r')
        return(self.subjectlist)
    
    def subject_code_from_index(self, index, setSubject=False):
        """
        Broken?
        """
        if type(self.subjectlist) == None:
            self.get_subject_list()
        if self.verbose is True:
            print(f"Subject code: {self.subjectlist.iloc[index].tolist()}")
        
        return self.subjectlist.iloc[index].tolist()[0]
    

    
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
    

    def getTestIDs(self, subjectID):
        self.TestIDs = list(self.datafile[subjectID]['smartphone'].keys())
        return self.TestIDs
    
    def getActiveTestInfo(self, subjectID):
        self.ActiveTestInfo = pd.read_hdf(self.source, key=f'/{subjectID}/active_test_info')
        return self.ActiveTestInfo


        
# class subject_data():
#     def __init__(self, source, subject_ID) -> None:
#         self.source = source
#         self.id = subject_ID
#         self.tests = pd.read_hdf(self.source, key=f'/{self.id}/active_test_info')
#         print(self.tests)

#     def getsmartphonedata(self):
#         self.device = 'device_id:a'
#         print(pd.read_hdf(self.source, key=f'/{self.id}/smartphone/*/{self.device}'))




# class test_data():

#     def loadIMU(self, subject=None, test_id=None, device_id=None, channles=['acc', 'gyr', 'mag']):
#         if subject == None:
#             subject = self.currentsubject
#         if test_id == None:
#             test_id == self.currenttest_id
#         if device_id == None:
#             device_id == self.currentdevice_id


#         if 'acc' in channles:
#             accSelected = True
#             print(pd.read_hdf(self.source, key=f'/{subject}/smartphone/testid:0/device_id:a/acc'))
#         if 'gyr' in channles:
#             gyrSelected = True
#             print(pd.read_hdf(self.source, key=f'/{subject}/smartphone/testid:0/device_id:a/gyr'))
#         if 'mag' in channles:
#             accSelected = True
#             print(pd.read_hdf(self.source, key=f'/{subject}/smartphone/testid:0/device_id:a/mag'))



def createdummydata():
    hdf = pd.HDFStore('dummy_h5.h5')
    hdf.put('abcd', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('abcd/active_test_info', pd.DataFrame(np.random.rand(2,1)))
    hdf.put('abcd/smartphone/testid:0/device_id:a/acc', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/testid:0/device_id:a/gyr', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/testid:0/device_id:a/mag', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/testid:1/device_id:a/acc', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/testid:1/device_id:a/gyr', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/testid:1/device_id:a/mag', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('efgh', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('ijkl', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('mnop', pd.DataFrame(np.random.rand(3,3)))
    slist = pd.DataFrame(['abcd', 'efgh', 'ijkl', 'mnop'], columns=['subject'])
    hdf.put('subjectlist', slist)
    hdf.close()


createdummydata()
source = DataLoader().data_file_path

trialdata = h5_handler(source, verbose=True)
print(trialdata.get_subject_list())
subjectid = trialdata.subject_code_from_index(0)
# print(f"subject 'abcd' index:{trialdata.subject_index_from_code(subjectid)}")
#trialdata.loadIMU('abcd')
print(f"subjectID:{subjectid}")
print(trialdata.getActiveTestInfo(subjectid))
print(trialdata.getTestIDs(subjectid))

trialdata.close_file()


# s = subject_data(source, 'abcd')
# print("****")
# s.getsmartphonedata()