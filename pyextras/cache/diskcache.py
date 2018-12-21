#! /usr/bin/env python
import os
import pickle

from .cache import Cache
from .errors import (
    DiskCacheFileNotFoundError,
    DiskCacheFileNotFoundError,
    DiskCacheDirectoryNotFoundError,
    DiskCacheLoadError,
)


class DiskCache(Cache):
    def __repr__(self):
        return "[DiskCache]: {data}".format(data=str(self._data))


    def _load(self, filename, directory):
        path = os.path.join(directory, filename)

        if not os.path.exists(path):
            raise DiskCacheFileNotFoundError(
                "The provided path is not a file."
            )

        if os.path.isdir(path):
            raise DiskCacheNotAFileError(
                "The provided path is a directory and not a file."
            )

        # path exists and is a valid file
        # Attmpet to load in to memory
        with open(path, 'rb') as obj:
            try:
                self._data = pickle.load(obj)
            except pickle.PickleError:
                raise DiskCacheLoadError(
                    "The provided path was unable to be loaded into memory.\n"
                    "This is common when the file was corrupted."
                )

    def load(self, filename, directory=""):
        self._load(filename, directory)


    def _store(self, filename, directory):
        if directory and not os.path.isdir(path):
            raise DiskCacheDirectoryNotFoundError("The provided directory does not exist.")

        path = os.path.join(directory, filename)

        with open(path, 'wb') as obj:
            try:
                pickle.dump(self._data, obj)
            except pickle.PickleError:
                raise DiskCacheStoreError(
                    "Failed to store to the provided path."
                )

    def store(self, filename, directory=""):
        self._store(filename, directory)
