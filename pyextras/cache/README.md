# pyextras.cache

## Installation
```
$ pip install pyextras
```

## Introduction
There are three types of caches currently implemented:

  1. `Cache`: A simple time-based cache implemented as dictionary. Data "expires" after a default 1-day.

  * `DiskCache`: A descendent of `cache` that allows you to store and load the cache from files. This data is unencrypted and should never trust data from untrusted sources.

  * `EncryptedDiskCache`: A descendent of `DiskCache` that allows encrypts the stored files with AES256 (using `pyaes`).


## Usage
### `Cache`

Here is an example of using the simple, time-based `Cache`.
```python
#! /usr/bin/env python
from pyextras.cache import Cache
from datetime import datetime
from datetime import timedelta as td
c = Cache()

# Create a key-value pair in the cache with key "key" and value: '{"data": 5}'.
# The key-value pair will expire in 1 hour.
c.add("key", value={"data": 5}, timedelta=td(hours=1))

# This would output 1
len(c)

# This would output True
"key" in c

# This would raise pyextras.cache.errors.CacheKeyError
c.remove("notFoundKey")

# This would not.
c.remove("notFoundKey", raiseError=False)

# To check if the key has expired
c.isExpired("key")
False

# Add expired data
c.add("expired", value=10, timedelta=td(hours=-1))

# outputs True
c.isExpired("expired")

# Equivalent to c.add(100, value=10)
c[100] = 10

# Equivalent to c.get(100)
c[100]
```


### `DiskCache`

Here is an example of how to use `store` and `load` functionality of `DiskCache`.
```python
#! /usr/bin/env python
from pyextras.cache import DiskCache

# DiskCache() has the same interface as
# `Cache` for adding/removing/checking
# expiration
d = DiskCache()

# This will store the entire cache, d, into the file ".mycaches/filename".
# The path must exist.
d.store('filename', directory=".mycaches")


# Attempt to load the cache from a file into
# memory.
e = DiskCache()
e.load('filename', directory=".mycaches")

# Evaluates as True
# Provided that the path exist and has been unmodified.
print(e == d)
```

### `EncryptedDiskCache`

Here is an example of how to use the `EncryptedDiskCache`.

By default, to protect your encryption keys from being exposed in the source code, encryption keys read from your environment variables. To use a key directly, set the `direct=True`.

When you use an encryption key directly, a `EncryptedDiskCacheWarning` is raised. You can suppress these warnings using `suppress_warnings=True` or by setting the environment variable `PYEXTRAS_NO_WARNINGS=True`.

```python
#! /usr/bin/env python
from pyextras.cache import EncryptedDiskCache

e = EncryptedDiskCache("OS_ENVIRON_VAR")

e_warning_raised = EncryptedDiskCache("uJ9xwCwI77tBSBA3", direct=True)

e_no_warning = EncryptedDiskCache("EncryptedDiskCache", direct=True, suppress_warnings=True)
```

From here, the `EncryptedDiskCache` works the same as `DiskCache`.
