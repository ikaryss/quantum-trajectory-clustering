import os.path
import h5py
import numpy as np
from typing import Iterable


def write_waveform(filename: str, data: Iterable, folder: str):
    """
    writes a 1d or 2d arrays to hdf file
    :param filename: path for the file (example.h5 or example.hdf5)
    :param data: 1d or 2d numpy array
    """

    data = np.array(data)

    mode = "w" if not os.path.isfile(filename) else "r+"

    # Special datatype for HDF5 that supports collecting arrays with different length
    dt = h5py.special_dtype(vlen=np.dtype("int32"))

    # writing 2d arrays
    if isinstance(data[0], Iterable):
        with h5py.File(filename, mode) as f:
            if mode == "w":
                # if 2d array has a shape M x N instead of M x 1 we need to create a preallocate array
                # of specific shape
                if len(data.shape) > 1:
                    data = np.array(data, dtype=int)
                    pre_alloc = np.empty((data.shape[0],), dtype=object)
                    for i in range(data.shape[0]):
                        pre_alloc[i] = data[i]
                    data = np.copy(pre_alloc)

                f.create_dataset(
                    folder, data=data, dtype=dt, chunks=True, maxshape=10_000_000
                )

            else:
                if folder in f:
                    f[folder].resize((f[folder].shape[0] + data.shape[0]), axis=0)
                    f[folder][-data.shape[0] :] = data
                else:
                    # if 2d array has a shape M x N instead of M x 1 we need to create a preallocate array
                    # of specific shape
                    if len(data.shape) > 1:
                        data = np.array(data, dtype=int)
                        pre_alloc = np.empty((data.shape[0],), dtype=object)
                        for i in range(data.shape[0]):
                            pre_alloc[i] = data[i]
                        data = np.copy(pre_alloc)
                    f.create_dataset(
                        folder, data=data, dtype=dt, chunks=True, maxshape=10_000_000
                    )

    # writing 1d arrays
    else:
        with h5py.File(filename, mode) as f:
            if mode == "w":
                # if 2d array has a shape M x N instead of M x 1 we need to create a preallocate array
                # of specific shape
                pre_alloc = np.empty((1,), dtype=object)
                pre_alloc[0] = data
                f.create_dataset(
                    folder, data=pre_alloc, dtype=dt, chunks=True, maxshape=10_000_000
                )
            else:
                if folder in f:
                    f[folder].resize((f[folder].shape[0] + 1), axis=0)
                    f[folder][-1:] = data
                else:
                    pre_alloc = np.empty((1,), dtype=object)
                    pre_alloc[0] = data
                    f.create_dataset(
                        folder,
                        data=pre_alloc,
                        dtype=dt,
                        chunks=True,
                        maxshape=10_000_000,
                    )
