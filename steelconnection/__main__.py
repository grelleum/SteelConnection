# -*- coding: utf-8 -*-

"""Provide version information when imported on command line."""


from __future__ import print_function

import sys

from .__version__ import __documentation__, __url__, __version__
from .api import ASCII_ART

if __name__ == "__main__":
    print(ASCII_ART)
    print("Python version:", ".".join(str(x) for x in sys.version_info[:3]))
    print("SteelConnection version:", __version__)
    print("Documentation:", __documentation__)
    print("Project home: ", __url__)
    print()
