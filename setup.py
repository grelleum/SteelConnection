from setuptools import setup
import re

name = "steelconnection"
description = "Simplify access to the Riverbed SteelConnect REST API."
version = "1.0.5"
copyright = "Copyright 2018 Greg Mueller"

info = {
    "description": description,
    "version": version,
    "author": "Greg Mueller",
    "author_email": "steelconnection@grelleum.com",
    "license": "MIT",
    "project_urls": {
        "Documentation": "https://steelconnection.readthedocs.io/",
        "Source": "https://github.com/grelleum/SteelConnection",
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


def create_version_file(info):
    export_info = {k: v for k, v in info.items()}
    export_info["title"] = name
    export_info["copyright"] = copyright
    keys = [
        "title",
        "description",
        "version",
        "author",
        "author_email",
        "copyright",
        "license",
    ]
    text = '__{}__ = "{}"\n'
    with open(name + "/__version__.py", "wt") as f:
        f.write('"""Provide version and author details."""\n\n\n')
        for key in keys:
            f.write(text.format(key, export_info[key]))
        f.write(text.format("url", info["project_urls"]["Source"]))
        f.write(text.format("documentation", info["project_urls"]["Documentation"]))


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
create_version_file(info)
# if '.tox' not in '-'.join(sys.argv):
#     _ = read_and_update_readme('docs/index.rst')
long_description = read_and_update_readme("README.rst")
info["long_description"] = long_description
setup(name=name, **info)
