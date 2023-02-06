import os.path


class DataLoader():
    def __init__(self) -> None:
        data_locator_path = (os.path.join('..', 'pathfile.txt'))
        data_locator = open(data_locator_path, "r")
        self.data_file_path = data_locator.readline()
        data_locator.close()
        
    def printdatafilepath(self):
        print(self.data_file_path)


data = DataLoader()
data.printdatafilepath()
