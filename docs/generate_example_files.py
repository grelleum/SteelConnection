#!/usr/bin/env python

"""Generate reStructured text files from example scripts."""

from glob import glob
import os
import sys


def get_files(startdir):
    for filepath in glob(os.path.join(startdir, "*.py")):
        path, filename = os.path.split(filepath)
        if filename.startswith("test_") or filename.startswith("SKIP"):
            continue
        rstfile = "example_" + filename.replace(".py", ".rst")
        yield filepath, filename, rstfile


files = sorted(list(get_files("../examples")))
for filepath, filename, rstfile in files:
    # out_filename = os.path.join('source', rstfile)
    out_filename = rstfile
    print(filepath, filename, rstfile, out_filename)
    with open(filepath, "rt") as infile, open(out_filename, "wt") as outfile:
        outfile.write(filename + "\n")
        outfile.write("=" * len(filename))
        outfile.write("\n\n.. code:: python\n\n")
        for line in infile:
            outfile.write("   " + line)
        outfile.write("   \n")

contents = """
Examples
========

Examples scripts to get you started.

.. toctree::
   :maxdepth: 1

""".lstrip()

# rst_filename = os.path.join('source', 'examples.rst')
rst_filename = "examples.rst"
with open(rst_filename, "wt") as outfile:
    outfile.write(contents)
    for filepath, filename, rstfile in files:
        outfile.write("   {}\n".format(rstfile))
    outfile.write("\n")
