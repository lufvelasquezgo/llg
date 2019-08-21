#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages
from numpy.distutils.core import setup
from numpy.distutils.core import Extension

ffunctions = Extension(name='llg.ffunctions',
                       sources=['fortran-src/signature.pyf', 'fortran-src/mag_functions.f90'])


with open('README.rst') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()
history = ""

requirements = ['Click>=6.0', 'numpy==1.17.0']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Juan David Alzate Cardona",
    author_email='jdalzatec@unal.edu.co',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python package to solve the LLG equation by using the Heun scheme.",
    entry_points={
        'console_scripts': [
            'llg=llg.cli:main',
        ],
    },
    ext_modules=[ffunctions],
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='llg',
    name='llg',
    package_dir={'llg': 'src'},
    packages=[
        "llg"
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jdalzatec/llg',
    version='0.1.0',
    zip_safe=False,
)
