#!/usr/bin/env python3
#  Copyright 2020 Direkt, Australia
#  Copyright 2021 Direkt Embedded Pty Ltd
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


"""
Pip setup file used to create a package for testexecutor.
"""

import setuptools
import os

VERSION=""

current_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_path, 'testexecutor', 'VERSION')) as version_file:
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
    package_data={'testexecutor': ['ui/*.qml', 'ui/*.ico', 'ui/selector/*.qml', 'VERSION']},
    url="https://www.direktembedded.com",
    license_files=("LICENSE", "NOTICE"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache-2.0",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PySide6>=6.2',
    ],
    python_requires='>=3.6',
)

# python -m pip install --user --upgrade setuptools wheel
# python setup.py sdist bdist_wheel
