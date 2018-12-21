#! /usr/bin/env python

class BaseCacheError(Exception):
    pass

class CacheKeyError(BaseCacheError):
    pass

class CacheDatetimeError(BaseCacheError):
    pass
