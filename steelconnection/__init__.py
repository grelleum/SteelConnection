from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from requests import HTTPError
from steelconnection.steelconnection import SConAPI
from steelconnection.input_tools import get_input
from steelconnection.input_tools import get_username
from steelconnection.input_tools import get_password

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

import steelconnection.version
__version__ = steelconnection.version.__version__

__all__ = (
    'SConAPI',
    'get_input',
    'get_username',
    'get_password',
)
