#! /usr/bin/env python

# Basic Cache Errors
class CacheError(Exception):
    pass

class CacheKeyError(CacheError):
    pass

class CacheDatetimeError(CacheError):
    pass


# DiskCache Errors
class DiskCacheError(CacheError):
    pass


class DiskCacheNotAFileError(DiskCacheError):
    pass

class DiskCacheFileNotFoundError(DiskCacheError):
    pass

class DiskCacheDirectoryNotFoundError(DiskCacheError):
    pass

class DiskCacheLoadError(DiskCacheError):
    pass

class DiskCacheStoreError(DiskCacheError):
    pass
