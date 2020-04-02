# -*- coding: utf-8 -*-

"""Provide version information when imported on command line."""


from __future__ import print_function

import sys

from .about import documentation, project_home, version
from .api import ASCII_ART

if __name__ == "__main__":
    print(ASCII_ART)
    print("Python version:", ".".join(str(x) for x in sys.version_info[:3]))
    print("SteelConnection version:", version)
    print("Documentation:", documentation)
    print("Project home: ", project_home)
    print()
