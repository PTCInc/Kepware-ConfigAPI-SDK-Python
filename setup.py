# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Package Setup Script - run this to build the package
# Usage - python setup.py <build> sdist bdist_wheel
#  Example: python setup.py 1.0.0 sdist bdist_wheel

import setuptools
import pathlib, os

def read(rel_path):
    # type: (str) -> str
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()

def get_version(rel_path):
    # type: (str) -> str
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setuptools.setup(
    name="kepconfig",
    version= get_version("kepconfig/__init__.py"),
    author="PTC Inc",
    description="SDK package for Kepware Configuration API",
    keywords="Kepware, OPC, Configuration, Thingworx",
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PTCInc/Kepware-ConfigAPI-SDK-Python",
    project_urls={},
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.9',
)
