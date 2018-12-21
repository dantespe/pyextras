#! /usr/bin/env python

from datetime import datetime, timedelta
from .errors import CacheKeyError, CacheDatetimeError


class Cache:
    def __init__(self):
        self._data = {}


    def __len__(self):
        return len(self._data)


    def __contains__(self, key):
        return key in self._data


    def __str__(self):
        return str(self._data)


    def __repr__(self):
        return "[Cache]: {data}".format(data=str(self._data))


    def __eq__(self, other):
        return self._data == other._data

    def add(self, key, value=None, expires=None, timeDelta=1):
        if expires and not isinstance(expires, datetime):
            raise CacheDatetimeError(
                "`expires` argument must be None or a datetime.datetime object."
            )

        self._data[key] = {
            'value': value,
            'expires': expires if expires else datetime.now() + timedelta(timeDelta)
        }


    def remove(self, key, raiseError=True):
        if key not in self._data and raiseError:
            raise CacheKeyError("{key} was not found in the cache.".format(key=key))
        elif key in self._data:
            return self._data.pop(key)


    def isExpired(self, key, raiseError=True):
        if key not in self._data and raiseError:
            raise CacheKeyError("{key} was not found in the cache.".format(key=key))
        if key not in self._data:
            return True
        else:
            return datetime.now() > self._data[key]['expires']


    def get(self, key, raiseError=True):
        if key not in self._data and raiseError:
            raise CacheKeyError("{key} was not found in the cache.".format(key=key))
        return self._data.get(key)['value'] if self._data.get(key) else None
