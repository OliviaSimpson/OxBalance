import h5py
from Loader import DataLoader


# with h5py.File(data_source.data_file_path, "r") as datafile:
#     print("Keys: %s" % datafile.keys())
#     a_group_key = list(datafile.keys())[0]

#     print(type(datafile[a_group_key])) 

#     data = list(datafile[a_group_key])
#     print(data)

class h5_handler():

    def __init__(self, source) -> None:
       self.set_source(source)
       self.open_file()


    def set_source(self, source):
        self.source = source

    def open_file(self):
        datafile = h5py.File(self.source, 'r')

    def get_keys(self):
        print(f"Keys: {self.datafile.keys()}")


data_source = DataLoader()
dataset = h5_handler(data_source.data_file_path)
dataset.get_keys()