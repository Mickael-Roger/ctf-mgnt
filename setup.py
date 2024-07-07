#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='ctf-mgnt',
      version='0.1',
      # Modules to import from other scripts:
      packages=find_packages(),
      # Executables
      scripts=["ctf-mgnt.py"],
     )
