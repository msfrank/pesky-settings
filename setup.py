#!/usr/bin/env python

from setuptools import setup

# jump through some hoops to get access to versionstring()
from sys import path
from os.path import abspath, dirname
path.insert(0, abspath(dirname(__file__)))
from pesky.settings import versionstring

with open("README.rst", "r") as f:
    readme = f.read()
    
setup(
    # package description
    name = "pesky-settings",
    version = versionstring(),
    description="Pesky settings handling routines",
    long_description=readme,
    author="Michael Frank",
    author_email="msfrank@syntaxockey.com",
    url="https://github.com/msfrank/pesky-settings",
    # installation dependencies
    install_requires=[
        ],
    # package classifiers for PyPI
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License", 
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        ],
    # package contents
    namespace_packages=[
        "pesky",
        ],
    packages=[
        "pesky",
        'pesky.settings',
        ],
    test_suite="test",
    tests_require=["nose >= 1.3.1"]
)
