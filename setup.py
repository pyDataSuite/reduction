from setuptools import setup, find_packages
from Cython.Build import cythonize
from pathlib import Path
import numpy

with open( "README.md", "r" ) as f:
    long_description = f.read()

setup(
    name="reduction",
    version="0.0.1",
    packages=find_packages(),
    description="A package that specializes in representing larger datasets with smaller ones",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyDataSuite/reduction",
    author="Joey",
    author_email="josephameadows@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    ext_modules=cythonize( [ "reduction/**/*.pyx" ], annotate=True ),
    include_dirs=[ numpy.get_include( ) ]
)