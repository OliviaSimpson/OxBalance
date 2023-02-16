import h5py
from Loader import DataLoader

data = DataLoader(verbose=True)



with h5py.File(data.data_file_path, "r") as datafile:
    print("Keys: %s" % datafile.keys())
    a_group_key = list(datafile.keys())[0]

    print(type(datafile[a_group_key])) 

    data = list(datafile[a_group_key])
    print(data)