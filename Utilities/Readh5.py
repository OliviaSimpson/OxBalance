import h5py
filename = "file.hdf5"

with h5py.File(filename, "r") as f:
    print("Keys: %s" % f.keys())
    a_group_key = list(f.keys())[0]

    print(type(f[a_group_key])) 

    data = list(f[a_group_key])
    print(data)
    # ds_obj = f[a_group_key]      # returns as a h5py dataset object
    # ds_arr = f[a_group_key][()]  # returns as a numpy array