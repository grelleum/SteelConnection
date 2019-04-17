from setuptools import setup
import re

import steelconnection


name = steelconnection.__name__
description = steelconnection.__description__
version = steelconnection.__version__
copyright = steelconnection.__copyright__

info = {
    "description": description,
    "version": version,
    "author": steelconnection.__author__,
    "author_email": steelconnection.__author_email__,
    "license": steelconnection.__license__,
    "project_urls": {
        "Documentation": steelconnection.__documentation__,
        "Source": steelconnection.__url__,
    },
    "long_description_content_type": "text/x-rst",
    "install_requires": ["requests>=2.12.1"],
    "keywords": ["SteelConnect", "REST", "API", "Riverbed", "Grelleum"],
    "packages": ["steelconnection"],
    "classifiers": [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
}


def read_and_update_readme(filename):
    with open(filename, "rt") as f:
        readme = f.read()
    long_description = re.sub(
        r"   version \d+\.[\d\.]+[a-z]?", "   version " + info["version"], readme
    )
    with open(filename, "wt") as f:
        f.write(long_description)
    return long_description


print("VERSION:", info["version"])
# if '.tox' not in '-'.join(sys.argv):
#     _ = read_and_update_readme('docs/index.rst')
long_description = read_and_update_readme("README.rst")
info["long_description"] = long_description
setup(name=name, **info)
