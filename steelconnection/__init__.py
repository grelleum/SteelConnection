# flake8: noqa: F401
# -*- coding: utf-8 -*-

#         ______          __
#        / __/ /____ ___ / /
#    ____\ \/ __/ -_) -_) /      __  _
#   / _____/\__/\__/\__/_/_ ____/ /_(_)__  ___
#  / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
#  \___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/


"""
SteelConnection:
Simplify access to the Riverbed SteelConnect CX REST API.

Usage:

import steelconnection
sc = steelconnection.SConnect('REALM.riverbed.cc', username, password)
org = sc.lookup.org('MyOrgName')
nodes = sc.get('org/' + org_id + '/nodes')

Full documentation available at https://pypi.org/project/steelconnection/

:copyright: (c) 2018-2020 by Greg Mueller.
:license: MIT, see LICENSE for more details.
"""


__all__ = (
    "SConnect",
    "Timer",
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

from .api import SConnect, ASCII_ART, Timer
from .exceptions import AuthenticationError, APINotEnabled
from .exceptions import BadRequest, InvalidResource, ResourceGone
from .input_tools import get_input, get_username, get_password
from .lookup import LookUp

from . import about

version = __version__ = about.version

logging.getLogger(__name__).addHandler(logging.NullHandler())
