# -*- coding: utf-8 -*-

#    ______          _______                       __  _
#   / __/ /____ ___ / / ___/__  ___  ___  ___ ____/ /_(_)__  ___
#  _\ \/ __/ -_) -_) / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
# /___/\__/\__/\__/_/\___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/


"""
SteelConnection:
Simplify access to the Riverbed SteelConnect REST API.

Usage:

import steelconnection
sc = steelconnection.SConnect('REALM.riverbed.cc', username, password)
org = sc.lookup.org('MyOrgName')
nodes = sc.get('org/' + org_id + '/nodes')

Full documentation available at https://pypi.org/project/steelconnection/

:copyright: (c) 2018 by Greg Mueller.
:license: MIT, see LICENSE for more details.
"""


__all__ = (
    "SConnect",
    "SConAPI",
    "SConWithoutExceptions",
    "SConExitOnError",
    "ConnectionError",
    "RequestException",
    "AuthenticationError",
    "APINotEnabled",
    "BadRequest",
    "InvalidResource",
    "ResourceGone",
    "get_input",
    "get_username",
    "get_password",
    "ASCII_ART",
)


import logging

from requests import ConnectionError, RequestException

from .api import SConnect, ASCII_ART
from .api import SConAPI, SConWithoutExceptions, SConExitOnError
from .exceptions import AuthenticationError, APINotEnabled
from .exceptions import BadRequest, InvalidResource, ResourceGone
from .input_tools import get_input, get_username, get_password
from .lookup import LookUp
from .__version__ import __author__, __author_email__
from .__version__ import __copyright__, __description__
from .__version__ import __license__, __title__
from .__version__ import __url__, __documentation__, __version__


def about():
    return "\n".join(
        (
            __author__,
            __author_email__,
            __copyright__,
            __description__,
            __license__,
            __title__,
            __documentation__,
            __url__,
            __version__,
        )
    )


logging.getLogger(__name__).addHandler(logging.NullHandler())
