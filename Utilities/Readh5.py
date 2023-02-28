import h5py
from Loader import DataLoader
import numpy as np
import pandas as pd



class h5_handler():

    def __init__(self, source,verbose=False) -> None:
        self.verbose = verbose
        self.set_source(source)
        self.subjectlist = None
        self.ActiveTestInfo = None

    def set_source(self, source):
        self.source = source
        self.HDFfile = pd.HDFStore(source, mode='r')
    
    def get_subject_list(self):
        self.subjectlist = self.HDFfile.get("/subject_list")
        return(self.subjectlist)
    
    def subject_code_from_index(self, index, setSubject=False):
        if type(self.subjectlist) == None:
            self.get_subject_list()
        if self.verbose is True:
            print('sub')
            print(type(self.subjectlist))
            print('sub[index]')
            print(type(self.subjectlist.iloc[index]))
            # print(self.subjectlist.iloc[index])
            print(f"Subject code: {self.subjectlist.iloc[index]}")
        subjectCode = self.subjectlist.iloc[index]
        if type(subjectCode) is not str:
            subjectCode = subjectCode.to_string(index = False)
        return subjectCode
    
    def getActiveTestInfo(self, subjectID):
        self.ActiveTestInfo = self.HDFfile.get(f"/{subjectID}/active_test_info")
        return self.ActiveTestInfo
    
    def selectTestID(self, subjectID, testType, compleation = True):
        # if self.ActiveTestInfo == None:
        ati = self.getActiveTestInfo(subjectID)
        if compleation == True:
            ati = ati.loc[ati['status'] == 'COMPLETE']
        elif compleation == False:
            ati = ati.loc[ati['status'] != 'COMPLETE']
        selectedtests  = ati.loc[ati['type'] == testType]
        return selectedtests['id'].to_list()


        

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
    testid = [10,11,15,20]
    begin = [0,0,0,0]
    testtype = ["BALANCE__NATURAL_STANCE_EYES_OPEN",
            "BALANCE__NATURAL_STANCE_EYES_CLOSED",
            "BALANCE__LEFT_FOOT_EYES_OPEN",
            "BALANCE__LEFT_FOOT_EYES_OPEN"]
    teststatus = ["COMPLETE", "COMPLETE", "COMPLETE", "COMPLETE"]
    hdf.put('abcd/active_test_info', pd.DataFrame(list(zip(testid, begin, testtype, teststatus)), columns=["id", "begin", "type", "status"]))
    location = ["belt_back", "belt_front", "pocket_back_right", "pocket_back_left", "pocket_front_right", "pocket_front_left"]
    tag = ["000", "001", "002", "003", "004","005"]
    hdf.put('abcd/smartphone_device_location', pd.DataFrame(list(zip(location, tag)), columns=["location", "device_id"]))
    hdf.put('abcd/smartphone/10/000/acc', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/10/000/gyr', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/10/000/mag', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/15/000/acc', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/15/000/gyr', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/15/000/mag', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/20/000/acc', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/20/000/gyr', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/smartphone/20/000/mag', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/vicon/10/', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/vicon/15/', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('abcd/vicon/20/', pd.DataFrame(np.random.rand(100,3)))
    hdf.put('efgh', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('ijkl', pd.DataFrame(np.random.rand(3,3)))
    hdf.put('mnop', pd.DataFrame(np.random.rand(3,3)))
    slist = pd.DataFrame(['abcd', 'efgh', 'ijkl', 'mnop'])
    hdf.put('subject_list', slist)
    hdf.close()

### development ###
createdummydata()

    
source = DataLoader().data_file_path

trialdata = h5_handler(source, verbose=True)
print(trialdata.get_subject_list())
subjectid = trialdata.subject_code_from_index(0)
print(f"subjectID:{subjectid}")
print(trialdata.getActiveTestInfo(subjectid))

# trialids = trialdata.selectTestID(subjectid, "BALANCE__NATURAL_STANCE_EYES_OPEN")
trialids = trialdata.selectTestID(subjectid, "BALANCE__LEFT_FOOT_EYES_OPEN")
print(trialids)
for currentTrialID in trialids:
    print(currentTrialID)
    print(trialdata.getVicon(subjectid, currentTrialID))
    # deviceid = trialdata.getDeviceLocations(subjectid, currentTrialID, 'belt_back')
    # print(trialdata.getSmartphoneData(subjectid, currentTrialID, deviceid))