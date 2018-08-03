# -*- coding: utf-8 -*-

#    ______          _______                       __  _
#   / __/ /____ ___ / / ___/__  ___  ___  ___ ____/ /_(_)__  ___
#  _\ \/ __/ -_) -_) / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
# /___/\__/\__/\__/_/\___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/


"""
SteelConnection:
Simplify access to the Riverbed SteelConnect REST API.

usage:

import steelconnection
sc = steelconnection.SConAPI('REALM.riverbed.cc')
org = sc.lookup.org('MyOrgName')
nodes = sc.get('org/' + org_id + '/nodes')

Full documentation available at https://pypi.org/project/steelconnection/

:copyright: (c) 2018 by Greg Mueller.
:license: MIT, see LICENSE for more details.
"""

from .steelconnection import SConAPI, SConWithoutExceptions, SConExitOnError
from .exceptions import AuthenticationError, APINotEnabled
from .exceptions import BadRequest, InvalidResource
from .input_tools import get_input, get_username
from .input_tools import get_password, get_password_once
from .__version__ import __author__, __author_email__
from .__version__ import __copyright__, __description__
from .__version__ import __license__, __title__
from .__version__ import __url__, __version__

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = (
    'SConAPI',
    'SConWithoutExceptions',
    'SConExitOnError',
    'AuthenticationError',
    'APINotEnabled',
    'BadRequest',
    'InvalidResource',
    'get_input',
    'get_username',
    'get_password',
)
