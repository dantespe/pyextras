#! /usr/bin/env python
from hashlib import sha256
import os
import warnings
import pickle
import random

from .diskcache import DiskCache
from .cachewarnings import (
    EncryptedDiskCacheWarning
)
from .errors import (
    DiskCacheError,
    EncryptedDiskCacheError,
    EncryptedDiskCacheDirectoryNotFoundError,
    EncryptedDiskCacheNotAFileError
)

import pyaes

DEFAULT_SALT = "pyextras_not_so_secret_salt"
DEFAULT_INPUT_VARS = "0123456789abcdefghijklmnopqrstuvwxyz"
TEMP_FILENAME_SIZE = 32
TEMP_FIELNAME_EXTENSION = ".tmp"


def create_unique_filename(directory=""):
    if directory and not os.path.isdir(directory):
        raise EncryptedDiskCacheDirectoryNotFoundError(
            "The provided directory does not exist."
        )

    filename = ""
    extension = ".tmp"

    for i in range(0, TEMP_FILENAME_SIZE):
        filename += random.choice(DEFAULT_INPUT_VARS)

    while os.path.exists(os.path.join(directory, filename + extension)):
        filename += random.choice(DEFAULT_INPUT_VARS)

    return filename + extension


def convert_password_to_aes_key(password, salt=DEFAULT_SALT):
    return sha256((password + salt).encode('UTF-8')).digest()


class EncryptedDiskCache(DiskCache):
    def __init__(self, key, direct=False, salt=DEFAULT_SALT, suppress_warnings=False):
        suppress_warnings = suppress_warnings or os.environ.get("PYEXTRAS_NO_WARNINGS", False)

        self._data = {}

        if (direct or not key in os.environ) and not suppress_warnings:
            warnings.warn(
                "You are using a secret key directly. "
                "If you lose this key, you will NOT be able to load encrypted data. "
                "To suppress these warnings, use suppress_warnings=True or "
                "set the environment variable PYEXTRAS_NO_WARNINGS=True.",
                EncryptedDiskCacheWarning
            )

        self._key = key if direct else os.environ.get(key, key)
        self._salt = salt if salt else DEFAULT_SALT

        self._aes_key = convert_password_to_aes_key(self._key, self._salt)

    def __repr__(self):
        return "[EncryptedDiskCache]: {data}".format(data=str(self._data))


    def load(self, filename, directory=""):
        """
            1. Check for valid paramters
            2. Decrypt the file
            3. Call pickle.load(stream)
        """
        encrytedFile = os.path.join(directory, filename)

        if not os.path.isfile(encrytedFile):
            raise EncryptedDiskCacheNotAFileError(
                "The provided path is not a file."
            )

        pickledFile = create_unique_filename(directory=directory)
        mode = pyaes.AESModeOfOperationCTR(self._aes_key)
        errors = []


        # Try to Decrypt
        with open(encrytedFile, 'rb') as robj:
            with open(pickledFile, 'wb') as wobj:
                try:
                    pyaes.decrypt_stream(mode, robj, wobj)
                except Exception as e:
                    os.remove(pickledFile)
                    errors.append(e)
        if errors:
            raise EncryptedDiskCacheError(
                "Failed to decrypt. Are you using the right key?"
            )

        try:
            self._load(pickledFile, directory)
        except DiskCacheError as e:
            os.remove(pickledFile)
            errors.append(e)

        if errors:
            raise EncryptedDiskCacheError(
                "Failed to unpickle. This could happen if the data was corrupted."
            )
        os.remove(pickledFile)


    def store(self, filename, directory=""):
        """
            1. Check for valid paramaters
            2. Pickle self._data
            3. Encrypt PickledFile
            4. Remove Temporary PickledFile
        """
        if directory and not os.path.isdir(directory):
            raise EncryptedDiskCacheDirectoryNotFoundError(
                "The provided directory does not exist."
            )

        if os.path.isdir(os.path.join(directory, filename)):
            raise EncryptedDiskCacheNotAFileError(
                "The provided path is already a directory."
            )

        pickledFile = create_unique_filename(directory=directory)
        encryptedFile = os.path.join(directory, filename)
        mode = pyaes.AESModeOfOperationCTR(self._aes_key)

        # Store the unencrypted Pickle File
        errors = []
        try:
            self._store(pickledFile, directory)
        except DiskCacheError as e:
            errors.append(e)

        if errors:
            raise EncryptedDiskCacheError("Failed to store pickled file.")

        # Try to encrypt the pickle file
        with open(pickledFile, 'rb') as robj:
            with open(encryptedFile, 'wb') as wobj:
                try:
                    pyaes.encrypt_stream(mode, robj, wobj)
                except Exception:
                    errors.append(e)
        if errors:
            raise EncryptedDiskCacheError(
                "Failed to encrypt pickled file."
            )
        os.remove(pickledFile)


    def rekey():
        pass
