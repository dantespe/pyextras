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


    def __iter__(self):
        return iter(self._data)


    def __getitem__(self, key):
        return self.get(key)


    def __setitem__(self, key, value):
        return self.add(key, value)


    def __delitem__(self, key):
        return self.remove(key)


    def add(self, key, value=None, expires=None, timeDelta=timedelta(days=1)):
        if expires and not isinstance(expires, datetime):
            raise CacheDatetimeError(
                "`expires` argument must be None or a datetime.datetime object."
            )

        if not isinstance(timeDelta, timedelta):
            raise CacheDatetimeError(
                "`timedelta` is not an instance of datetime.timedelta object."
            )

        self._data[key] = {
            'value': value,
            'expires': expires if expires else datetime.now() + timeDelta
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
