#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from glob import glob
from setuptools import find_packages, setup


with open("README.rst") as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()
history = ""

requirements = [
    "Click>=6.0",
    "numpy>=1.17.0",
    "tqdm>=4.32.2",
    "h5py>=2.10.0",
    "matplotlib>=3.1.2",
    "Pillow>=7.0.0",
    "moviepy>=1.0.1",
    "vapory>=0.1.1",
    "nptyping>=1.0.1",
    "numba>=0.48.0",
]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Juan David Alzate Cardona",
    author_email="jdalzatec@unal.edu.co",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Python package to solve the LLG equation by using the Heun scheme.",
    entry_points={"console_scripts": ["llg=llg.cli:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="llg",
    name="llg",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jdalzatec/llg",
    version="1.0.1",
    zip_safe=False,
)
