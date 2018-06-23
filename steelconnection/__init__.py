# -*- coding: utf-8 -*-

"""
SteelConnection:
Simplify access to the Riverbed REST API.

usage:

import steelconnection
sconnect = steelconnection.SConAPI('REALM.riverbed.cc')
org_id, org = sconnect.lookup.org('MyOrgName')
nodes = sconnect.get('org/' + org_id + '/nodes')

Full documentation available at https://pypi.org/project/steelconnection/

:copyright: (c) 2018 by Greg Mueller.
:license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .steelconnection import SConAPI
from .input_tools import get_input
from .input_tools import get_username
from .input_tools import get_password

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

from .__version__ import __author__, __author_email__
from .__version__ import __copyright__, __description__
from .__version__ import __license__, __title__
from .__version__ import __url__, __version__


__all__ = (
    'SConAPI',
    'get_input',
    'get_username',
    'get_password',
)
