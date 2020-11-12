# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import setuptools
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

print("Arguments list: ", str(sys.argv))
if len(sys.argv) < 4:
    print("Not enough arguments. Arguments list: ", str(sys.argv))
else:
    version = sys.argv[1]
    sys.argv.pop(1)
    setuptools.setup(
        name="kepconfig",
        version= version,
        author="PTC Inc",
        # author_email="author@example.com",

        description="SDK package for Kepware Configuration API",
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
