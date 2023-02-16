import os.path


class DataLoader():
    """
    A class to handel the loading of data from a .h5 file
    ...
    Attributes
    ----------
    data_path_input = None
        Opoptunity to provide an alternitive data locator path (files such as .txt), or the path to the data (files with the extention .h5)

    Methods
    -------
    __init__()
        initiates class and calls find_data_file
    find_data_file()
        Finds the data locator and sets the path to the datafile
    show_data_file_path()
        development tool to check the data file path
    """

    def __init__(self, input_path=None, verbose=False) -> None:

        self.data_file_path = None
        self.verbose = verbose


        if input_path != None:
            if '.h5' in input_path: # if the data file is an h5
                self.data_file_path = input_path
        if self.data_file_path == None:     # if data file path is still uset, find the data file from the locator
            self.find_data_file_from_locator(input_path)
        
        if self.test_data_file() is True:
            if self.verbose == True:
                print(f"Data File Path: {self.data_file_path}")
        


    def find_data_file_from_locator(self, data_locator_path):
        """Locates data file

        Gets the path of the datafile

        Args:
            data_locator_path: If None data will be looked for in defult data locator file location (../data_locator.txt)
                if a path is provided it will search for the data locator file in that location

        Returns:
            os.path normal path string for the location of the 

        Raises:
            FileNotFoundError: An error occurred when loading the locator file
        """

        # Use defult data locator path or custom data locator path

        # IF path is None, use defult path
        if data_locator_path is None:
            data_locator_path = os.path.join('..', 'data_locator.txt')  # set to defult path
            self.data_file_path = os.path.normpath(data_locator_path)   # convert to os.path normal path 

        # ELSE (if path not None) use given path)
        
        try:
            # Open Data locator and read path to data file
            data_locator = open(data_locator_path, "r")     
            abspath = os.path.abspath(data_locator.readline())
            self.data_file_path = os.path.normpath(abspath)
            data_locator.close()

        except FileNotFoundError:
            # If file not found present error message
            raise Exception(f"Data locator file not found at the path: \"{data_locator_path}\"")

        # if os.path.exists(self.data_file_path):
        #     return self.data_file_path
        # else:
        #     data_file = open(self.data_file_path, "r")
        #     print(data_file.readline())
        #     data_file.close()

        #     raise Exception(f"The selected data file (\"{self.data_file_path}\") does not exist")


    # def show_data_file_path(self):
    #     print(self.data_file_path)

    #     data_locator_path = (os.path.join('..', 'data_locator.txt'))
    #     data_locator = open(data_locator_path, "r")
    #     self.data_file_path = os.path.normpath(data_locator.readline())
    #     data_locator.close()
    #     return self.data_file_path

    def test_data_file(self):
        passingtests = []
        passingtests.append(os.path.exists(self.data_file_path))
        try:
                data_file = open(self.data_file_path, "r")
                #     print(data_file.readline())
                data_file.close()
                passingtests.append(True)
        except:
            passingtests.append(False)
            raise Exception(f"Data file: \"{self.data_file_path}\" will not open")
        
        if self.verbose == True:
            if passingtests == [True, True]:
                print(f"Data File: {self.data_file_path} appers good")
            elif passingtests[0] == False:
                print(f"Data File: {self.data_file_path} dosent exist")
            else:
                print(f"Data File: {self.data_file_path} dosent open")

data = DataLoader(verbose=True)
# data.show_data_file_path()
