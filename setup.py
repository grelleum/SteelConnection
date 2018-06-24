import re
import setuptools

from steelconnection.__version__ import __author__, __author_email__
from steelconnection.__version__ import __copyright__, __description__
from steelconnection.__version__ import __license__, __title__
from steelconnection.__version__ import __url__, __version__


keywords = ['SteelConnect', 'REST', 'API', 'Riverbed', 'Grelleum']
base_url = 'https://github.com/grelleum/SteelConnection/archive/'

classifiers=(
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
)

with open('README.md', 'rt') as f:
    long_description = f.read()

download_url = base_url + __version__ + '.tar.gz'

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=__url__,
    download_url=download_url,
    keywords = keywords,
    packages=setuptools.find_packages(),
    classifiers=classifiers
)

# setuptools.setup(
#     name=name,
#     version=version,
#     author=author,
#     author_email=author_email,
#     description=description,
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     url=url,
#     download_url=download_url,
#     keywords = keywords,
#     packages=setuptools.find_packages(),
#     classifiers=classifiers
# )