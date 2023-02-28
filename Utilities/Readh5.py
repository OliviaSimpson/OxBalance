import h5py
from Loader import DataLoader
import numpy as np
import pandas as pd



class h5_handler():

    def __init__(self, source,verbose=False) -> None:
        self.verbose = verbose
        self.set_source(source)
        # self.open_file()
        self.subjectlist = None

    def set_source(self, source):
        self.source = source
        self.HDFfile = pd.HDFStore(source, mode='r')

    # def open_file(self):
    #     self.datafile = h5py.File(self.source, 'r')
    
    # def close_file(self):
    #     self.datafile.close()
    
    def get_subject_list(self):
        # hdf = pd.HDFStore(self.source, mode='r')
        self.subjectlist = self.HDFfile.get("/subject_list")
        return(self.subjectlist)
    
    def subject_code_from_index(self, index, setSubject=False):
        """
        Broken?
        """

        if type(self.subjectlist) == None:
            self.get_subject_list()
        if self.verbose is True:
            print('sub')
            print(type(self.subjectlist))
            print('sub[index]')
            print(type(self.subjectlist.iloc[index]))
            # print(self.subjectlist.iloc[index])
            print(f"Subject code: {self.subjectlist.iloc[index].tolist()}")
        
        return self.subjectlist.iloc[index].tolist()[0]
    
    def getActiveTestInfo(self, subjectID):
        self.ActiveTestInfo = self.HDFfile.get(f"/{subjectID}/active_test_info")
        return self.ActiveTestInfo

    def getVicon(self, subjectID, testID):
        return self.HDFfile.get(f"/{subjectID}/vicon/{testID}")
    

    def getSmartphoneData(self, subjectID, trialID, deviceID, axisToggle = {'acc':True, 'gyr':True, 'mag':True }):

        outputDict = {}

        if type(axisToggle) == list:
            axisToggle['acc'] = axisToggle[0]
            axisToggle['gyr'] = axisToggle[1]
            axisToggle['mag'] = axisToggle[2]


        if axisToggle['acc'] is True:
            outputDict.update({'acc':self.HDFfile.get(f"/{subjectID}/smartphone/{trialID}/{deviceID}/acc")})
        if axisToggle['gyr'] is True:
            outputDict.update({'gyr':self.HDFfile.get(f"/{subjectID}/smartphone/{trialID}/{deviceID}/gyr")})
        if axisToggle['mag'] is True:
            outputDict.update({'mag':self.HDFfile.get(f"/{subjectID}/smartphone/{trialID}/{deviceID}/mag")})

        return outputDict
    
    def getDeviceLocations(self, subjectID, TrialID, Position):

        deviceLocations = (self.HDFfile.get(f'/{subjectID}/smartphone_device_location'))
        selecteddevice = deviceLocations.loc[deviceLocations['location'] == Position]
        return selecteddevice["device_id"].to_string(index=False)




def createdummydata():
    hdf = pd.HDFStore('dummy_h5.h5', mode='w')
    hdf.put('abcd', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('abcd/active_test_info', pd.DataFrame(np.random.rand(2,1)))
    location = ["belt_back", "belt_front", "pocket_back_right", "pocket_back_left", "pocket_front_right", "pocket_front_left"]
    tag = ["000", "001", "002", "003", "004","005"]
    hdf.put('abcd/smartphone_device_location', pd.DataFrame(list(zip(location, tag)), columns=["location", "device_id"]))
    hdf.put('abcd/smartphone/10/000/acc', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/10/000/gyr', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/10/000/mag', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/11/000/acc', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/11/000/gyr', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/11/000/mag', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/vicon/10/', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/vicon/11/', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('efgh', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('ijkl', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('mnop', pd.DataFrame(np.random.rand(3,3)))
    slist = pd.DataFrame(['abcd', 'efgh', 'ijkl', 'mnop'], columns=['subject'])
    hdf.put('subject_list', slist)
    hdf.close()

### development ###
createdummydata()

    
source = DataLoader().data_file_path

trialdata = h5_handler(source, verbose=True)
print(trialdata.get_subject_list())
subjectid = trialdata.subject_code_from_index(0)
# print(f"subject 'abcd' index:{trialdata.subject_index_from_code(subjectid)}")
#trialdata.loadIMU('abcd')
print(f"subjectID:{subjectid}")
print(trialdata.getActiveTestInfo(subjectid))

trialid = 10
print(trialdata.getVicon(subjectid, trialid))
deviceid = trialdata.getDeviceLocations(subjectid, trialid, 'belt_back')
print(trialdata.getSmartphoneData(subjectid, trialid, deviceid))
#print(trialdata.getTestIDs(subjectid))

# trialdata.close_file()


# s = subject_data(source, 'abcd')
# print("****")
# s.getsmartphonedata()