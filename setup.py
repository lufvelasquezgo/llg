"""The setup script."""

from glob import glob
from setuptools import find_packages, setup


with open("README.md") as readme_file:
    readme = readme_file.read()

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
    author="Luisa Fernanda Velásquez González",
    author_email="lufvelasquezgo@unal.edu.co",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
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
    url="https://github.com/lufvelasquezgo/llg",
    version="1.1.0",
    zip_safe=False,
)
