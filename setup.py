from setuptools import setup

# Problem was that I was importing version from steelconnection as her:
# from steelconnection.__version__ import __version__
# this caused pip to try to import steelconnection before installing it
# and it has a dependency on requests that may not yet have been installed.
#
# solution is to have setup.py build the __version__ file,
# such that setup.py is the single source of truth.
#
# Here is the install failing when the dependency is not installed:
#
# Looking in indexes: https://test.pypi.org/simple/
# Collecting steelconnection
#   Downloading https://test-files.pythonhosted.org/packages/0d/3b/323931e1d4379d193be02475497250c40c611eee85b0d51d910d2ef803de/steelconnection-0.9.9.1.tar.gz
#     Complete output from command python setup.py egg_info:
#     Traceback (most recent call last):
#       File "<string>", line 1, in <module>
#       File "/tmp/pip-install-bqu7w8dh/steelconnection/setup.py", line 2, in <module>
#         from steelconnection.__version__ import __version__
#       File "/tmp/pip-install-bqu7w8dh/steelconnection/steelconnection/__init__.py", line 20, in <module>
#         from .steelconnection import SConAPI
#       File "/tmp/pip-install-bqu7w8dh/steelconnection/steelconnection/steelconnection.py", line 29, in <module>
#         import requests
#     ModuleNotFoundError: No module named 'requests'


__version__ = '0.9.9.2'

print('VERSION:', __version__)

with open('README.md', 'rt') as f:
    long_description = f.read()

setup(
    name='steelconnection',
    install_requires=['requests>=2.12.1'],
    version=__version__,
    author='Greg Mueller',
    author_email='steelconnection@grelleum.com',
    description='Simplify access to the Riverbed SteelConnect REST API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/grelleum/SteelConnection',
    keywords=['SteelConnect', 'REST', 'API', 'Riverbed', 'Grelleum'],
    packages=['steelconnection'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
)
