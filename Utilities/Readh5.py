import h5py
from Loader import DataLoader
import numpy as np
import pandas as pd



class H5Handler():
    """
    A class to handel the reading of trial sensor data from a .h5 file
    ...
    Attributes
    ----------
    source
        DataLoader class from Loader.py to indicate where the .h5 file is
    verbose = False
        Bool determins if functions print full messages or limited messages
    Methods
    -------
    __init__()
        initiates class and calls find_data_file
    setSource()
        Set or update the source being used and creates pandas hdf store
    getSubjectList()
        
    subjectCodeFromIndex()

    getActiveTestInfo()

    selectTestID()

    getVicon()

    getSmartphoneData()

    getDeviceLocations()
    

    """

    def __init__(self, source,verbose=False) -> None:
        self.verbose = verbose
        self.setSource(source)
        self.subjectList = None
        self.activeTestInfo = None

    def setSource(self, source):
        self.source = source
        self.hdfFile = pd.HDFStore(source, mode='r')
    
    def getSubjectList(self):
        self.subjectList = self.hdfFile.get("/subject_list")
        return(self.subjectList)
    
    def subjectCodeFromIndex(self, index, setSubject=False):
        if type(self.subjectList) == None:
            self.getSubjectList()
        if self.verbose is True:
            print('sub')
            print(type(self.subjectList))
            print('sub[index]')
            print(type(self.subjectList.iloc[index]))
            # print(self.subjectlist.iloc[index])
            print(f"Subject code: {self.subjectList.iloc[index]}")
        subjectCode = self.subjectList.iloc[index]
        if type(subjectCode) is not str:
            subjectCode = subjectCode.to_string(index = False)
        return subjectCode
    
    def getActiveTestInfo(self, subjectID):
        self.activeTestInfo = self.hdfFile.get(f"/{subjectID}/active_test_info")
        return self.activeTestInfo
    
    def selectTestID(self, subjectID, testType, compleation = True):
        # if self.ActiveTestInfo == None:
        ati = self.getActiveTestInfo(subjectID)
        if compleation == True:
            ati = ati.loc[ati['status'] == 'COMPLETE']
        elif compleation == False:
            ati = ati.loc[ati['status'] != 'COMPLETE']
        selectedTests  = ati.loc[ati['type'] == testType]
        return selectedTests['id'].to_list()


        

    def getVicon(self, subjectID, testID):
        return self.hdfFile.get(f"/{subjectID}/vicon/{testID}")
    

    def getSmartphoneData(self, subjectID, trialID, deviceID, axisToggle = {'acc':True, 'gyr':True, 'mag':True }):

        outputDict = {}

        if type(axisToggle) == list:
            axisToggle['acc'] = axisToggle[0]
            axisToggle['gyr'] = axisToggle[1]
            axisToggle['mag'] = axisToggle[2]


        if axisToggle['acc'] is True:
            outputDict.update({'acc':self.hdfFile.get(f"/{subjectID}/smartphone/{trialID}/{deviceID}/acc")})
        if axisToggle['gyr'] is True:
            outputDict.update({'gyr':self.hdfFile.get(f"/{subjectID}/smartphone/{trialID}/{deviceID}/gyr")})
        if axisToggle['mag'] is True:
            outputDict.update({'mag':self.hdfFile.get(f"/{subjectID}/smartphone/{trialID}/{deviceID}/mag")})

        return outputDict
    
    def getDeviceLocations(self, subjectID, TrialID, Position):

        deviceLocations = (self.hdfFile.get(f'/{subjectID}/smartphone_device_location'))
        selectedDevice = deviceLocations.loc[deviceLocations['location'] == Position]
        return selectedDevice["device_id"].to_string(index=False)




def createDummyData():
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
# createDummyData()

    
source = DataLoader().data_file_path

trialdata = H5Handler(source, verbose=True)
print(trialdata.getSubjectList())
subjectid = trialdata.subjectCodeFromIndex(0)
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