from setuptools import setup
import re


name = "steelconnection"
description = "Simplify access to the Riverbed SteelConnect CX REST API."
version = "1.1.8"
author = "Greg Mueller"
author_email = "steelconnection@grelleum.com"
copyright = "Copyright 2018-2020 Greg Mueller"
license = "MIT"
project_home = "https://github.com/grelleum/SteelConnection"
documentation = "https://steelconnection.readthedocs.io/"


readme = "README.rst"
with open(readme, "rt") as fh:
    long_description = fh.read()

setup(
    name=name,
    description=description,
    version=version,
    author=author,
    author_email=author_email,
    license=license,
    url=project_home,
    long_description_content_type="text/x-rst",
    long_description=long_description,
    install_requires=["requests>=2.12.1"],
    keywords=["SteelConnect CX", "REST", "API", "Riverbed", "Grelleum"],
    packages=["steelconnection"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
