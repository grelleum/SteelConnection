import re
import setuptools

name = 'steelconnection'
description = 'Simplify REST API access to Riverbed SteelConnect.'
keywords = ['SteelConnect', 'REST', 'API', 'Riverbed', 'Grelleum']
url = 'https://github.com/grelleum/SteelConnection'
author = 'Greg Mueller'
author_email = 'steelconnection@grelleum.com'
base_url = 'https://github.com/grelleum/SteelConnection/archive/'

classifiers=(
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
)

long_description = """SteelConnection

Convienience objects for making REST API calls
to Riverbed SteelConnect Manager.
"""

with open('README.md', 'r') as f:
    readme = f.read()
version = re.findall(r'version (\d+\.\d+\.\d+)', readme)[0]

download_url = base_url + version + '.tar.gz'

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=url,
    download_url=download_url,
    keywords = keywords,
    packages=setuptools.find_packages(),
    classifiers=classifiers
)