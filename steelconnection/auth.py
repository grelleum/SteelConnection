# coding: utf-8

"""
auth

Tools for handling credentials.
"""

from __future__ import print_function
import warnings

from requests.utils import get_netrc_auth

from .exceptions import AuthenticationError, InvalidResource
from .input_tools import get_input, get_username, get_password_once


def unattended_mode(realm, username, password, use_netrc):
    if use_netrc:
        # requests will look for .netrc if auth is not provided.
        if not realm:
            raise ValueError('Must supply realm when using .netrc.')
        if username or password:
            error = 'Do not supply username or password when using .netrc.'
            raise ValueError(error)
        return True
    elif realm and username and password:
        return True
    else:
        return False


def get_realm(sconnect, realm, connection_attempts):
    """Prompt user for realm if not already supplied."""
    if realm:
        return realm
    prompt = 'Enter SteelConnect Manager fully qualified domain name: '
    for _ in range(connection_attempts):
        realm = get_input(prompt)
        sconnect.realm = realm
        try:
            sconnect.get('orgs')
        except IOError as e:
            # Could not connect to server.
            print('Error:', e)
            print('Cannot connect to', realm)
        except InvalidResource as e:
            # Connected to a webserver, but not SteelConnect.
            print(e)
            print(realm, 'is not a SteelConnect Manager.')
        except AuthenticationError:
            break  # Success.
        else:
            break  # Success.
    else:
        raise RuntimeError('Could not connect to SteelConnect Manager.')
    return realm


def _get_creds(sconnect, username, password, connection_attempts):
    """Get realm and credentials based on supplied values."""
    if not username and not password:
        username, password = check_netrc(sconnect.realm, username, password)
    if not username or not password:
        provided = username, password
        for _ in range(connection_attempts):
            if not username:
                username = get_username()
            if not password:
                password = get_password_once()
            sconnect.session.auth = (username, password)
            try:
                sconnect.get('orgs')
            except AuthenticationError:
                print('Authentication Failed')
                username, password = provided
            else:
                return username, password
        if connection_attempts:
            raise RuntimeError('Failed to login to realm ' + sconnect.realm)
    if not username or not password:
        return None
    else:
        return username, password


def check_netrc(realm, username, password):
    """Check .netrc file for authentication credentials."""
    result = get_netrc_auth('https://' + realm)
    if result:
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn(
            "Use the 'use_netrc=True' argument when accessing "
            " credentials stored in a '.netrc' file.\n"
            "Future versions will not check '.netrc' without "
            "explicit definition to avoid unexpected results.",
            category=DeprecationWarning,
            stacklevel=2
        )
        warnings.simplefilter('default', DeprecationWarning)
        return result
    else:
        return username, password
