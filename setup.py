# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kepconfig",
    version="1.0b2.1",
    author="PTC Inc",
    author_email="presales.support@kepware.com",
    description="API package for Kepware Configuration API",
    keywords="Kepware OPC Configuration Thingworx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="TBD",
    project_urls={},
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Manufacturing",
    ],
    python_requires='>=3.6',
)
