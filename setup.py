#!/usr/bin/env python3

"""
Pip setup file used to create a package for testexecutor.

Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE file
"""

import setuptools
import os

VERSION=""

current_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_path, 'VERSION')) as version_file:
    VERSION = version_file.read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testexecutor",
    version=VERSION,
    description="A python UI library for the execution and control of device tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'testexecutor': ['ui/*.qml', 'ui/*.ico']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3-Clause License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PySide2>=5.13',
    ],
    python_requires='>=3.6',
)

# python -m pip install --user --upgrade setuptools wheel
# python setup.py sdist bdist_wheel
