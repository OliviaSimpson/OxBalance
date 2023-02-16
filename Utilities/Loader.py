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

        # set class variables
        self.data_file_path = None
        self.verbose = verbose

        
        if (input_path != None) and ('.h5' in input_path): # if a path is given and it contains the .h5 extension
                self.data_file_path = input_path
        if self.data_file_path == None:     # if data file path is still uset, find the data file from the locator
            self.find_data_file_from_locator(input_path)
        
        # test data file path
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
            data_locator_path = os.path.join('data_locator.txt')  # set to defult path
            self.data_file_path = os.path.normpath(data_locator_path)   # convert to os.path normal path 

        # ELSE (if path not None) use passed path)
        
        try:
            # Open Data locator and read path to data file
            data_location = open(data_locator_path, "r")     
            abspath = os.path.abspath(data_location.readline())
            self.data_file_path = os.path.normpath(abspath)
            data_location.close()

        except FileNotFoundError:
            # If file not found present error message
            raise Exception(f"Data locator file not found at the path: \"{data_locator_path}\"")

    def test_data_file(self):
        """Tests data file

        Tests that the file path for the data file exists and that the data file can be opened and closed.

        Args:
            

        Returns:
            Bool: True if file exists and can be opened, False if path does not exist or file causes error when opening

        Raises:
            Data File: {self.data_file_path} does not exist
            Data File: {self.data_file_path} does not  open
            Unexpected test result combination: {passingtests}
        """
        passingtests = []   # array variable to hold the results of file path and file open tests
        passingtests.append(os.path.exists(self.data_file_path)) # Test if file path exists

        # If path does not exist
        if passingtests[0] == False:
            if self.verbose:
                print("DATA FILE TEST FAIL: Data file path existance test Failed")
            raise Exception(f"Data File: {self.data_file_path} does not exist")

        # If path exists
        else:
            if self.verbose:
                print("DATA FILE TEST PASS: Data ffile path existance test PASSED")

            # Test opening/closing file
            try:
                    data_file = open(self.data_file_path, "r")
                    data_file.close()
                    passingtests.append(True)
            except:
                # If opening/closing file causes error
                passingtests.append(False)
                if self.verbose:
                    print("DATA FILE TEST FAIL: Data file Open/Close test Failed")
                raise Exception(f"Data File: {self.data_file_path} does not  open")
                return False
            
            # Both Tests Passing            
            if passingtests == [True, True]:
                if self.verbose:
                    print("DATA FILE TEST PASS: Data file Open/Close test PASSED")
                return True
            else:
                # This situation should never occore
                raise Exception(f"Unexpected test result combination: {passingtests}")
                
    def toggle_verbose(self, newstate = None):
        """Toggles dataloader verbose

        Switches between verbose and not verbose, if given a new state (bool) will switch verbose to be the given state.

        Args:
            newstate=None: (optional) if provided this will change the classe's verboseness to match this value

        Returns:

        Raises:

        """
        # if new state is given set verbose to new state:
        if type(newstate) == "bool":
            self.verbose = newstate
        # if a new state is not given toggle verbose
        else:
            self.verbose ^= self.verbose

    # def change_data_file(input_path=None,):
    #     if (input_path != None) and ('.h5' in input_path): # if a path is given and it contains the .h5 extension
    #             self.data_file_path = input_path
    #     if self.data_file_path == None:     # if data file path is still uset, find the data file from the locator
    #         self.find_data_file_from_locator(input_path)
        
    #     # test data file path
    #     if self.test_data_file() is True:
    #         if self.verbose == True:
    #             print(f"Data File Path: {self.data_file_path}")

# junk code
# print(type(True))
# data = DataLoader(verbose=True)
# # data.show_data_file_path()
