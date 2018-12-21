#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from disutils.core import setup

setup(
    name='pyextras',
    version='0.0.2',
    description='Extra Python utilities.',
    author='Dante Spencer',
    author_email='dantespe@umich.edu',
    install_requires=[
        'pyaes'
    ],
    packages=['pyextras', 'pyextras.cache',]
)
