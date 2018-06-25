# coding: utf-8

"""SteelConnection

Convienience objects for making REST API calls
to Riverbed SteelConnect Manager.

Usage:
    sconnect = steelconnection.SConAPI(scm_name, username, password)

    Optional keyword api_version can be used to specify an API version number.
    Currently there is only one API version: '1.0'.

    Once you have instantiated an object as shown above,
    you can use the object to make calls to the REST API.

    For example, to get all nodes in the realm:
    nodes = sconnect.config.get('nodes')
    ... or in a specifc org:
    nodes = sconnect.config.get('/org/' + orgid + '/nodes')  
    
    Any call that does not result in a success (HTTP status code 200)
    will raise an exception, so calls should be wrapped in a try/except pair.
"""


from __future__ import print_function

import getpass
import json
import requests
import sys
import traceback
import warnings

from .__version__ import __version__
from .exceptions import AuthenticationError, APINotEnabled, NotFoundError
from .lookup import _LookUp
from .input_tools import get_username, get_password, get_password_once


class SConAPI(object):
    """Make REST API calls to Riverbed SteelConnect Manager."""

    def __init__(
        self,
        controller,
        username=None,
        password=None,
        api_version='1.0',
        raise_on_failure=True,
    ):
        """Initialize attributes."""
        self.controller = controller
        self.username = username
        self.password = password
        self.api_version = api_version
        self.raise_on_failure = raise_on_failure
        self.session = requests.Session()
        self.result = None
        self.response = None
        self.headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }
        self.lookup = _LookUp(self)
        self.__version__ = __version__
        self._authenticate(username, password)
        self.scm_version = self._get_scm_version()

    def _authenticate(self, username=None, password=None):
        """Attempt authentication."""
        attempt_netrc_auth = username is None and password is None
        if attempt_netrc_auth:
            try:
                self.get('orgs')
            except AuthenticationError:
                pass
            else:
                return
        self.username, self.password = self._get_auth(username, password)
        self.get('orgs')

    def _get_scm_version(self, username=None, password=None):
        """Get version and build number of SteelConnect Manager."""
        try:
            status = self.get('status')
        except NotFoundError:
            return '2.8 or earlier.'
        else:
            scm_version = status.get('scm_version'), status.get('scm_build')
            return '.'.join(s for s in scm_version if s)

    def _get_auth(self, username=None, password=None):
        """Prompt for username and password if not provided."""
        username = get_username() if username is None else username
        password = get_password_once() if password is None else password 
        return username, password

    def __bool__(self):
        """Return the success of the last request.

        :returns: True of False if last request succeeded.
        :rtype: bool
        """
        return False if self.response is None else self.response.ok 

    def __repr__(self):
        """Return a string consisting of class name, controller, and api.

        :returns: Information about this object.
        :rtype: str
        """
        details = ', '.join([
            "controller: '{0}'".format(self.controller),
            "scm version: '{0}'".format(self.scm_version),
            "api version: '{0}'".format(self.api_version),
            "response: '{0}'".format(self.response),
        ])
        return '{0}({1})'.format(self.__class__.__name__, details)

    def get(self, resource, params=None):
        r"""Send a GET request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self.session.get(
            url=self.url('config', resource),
            auth=(self.username, self.password) if self.username else None,
            headers=self.headers,
            params=params,
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            exception = self._determine_exception(self.response)
            if self.raise_on_failure:
                raise exception
            else:
               self.result = {'error': str(exception)}
        return self.result

    def getstatus(self, resource, params=None):
        r"""Send a GET request to the SteelConnect.Reporting API.

        :param str resource: api resource to get.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self.session.get(
            url=self.url('reporting', resource),
            auth=(self.username, self.password) if self.username else None,
            headers=self.headers,
            params=params,
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            exception = self._determine_exception(self.response)
            if self.raise_on_failure:
                raise exception
            else:
               self.result = {'error': str(exception)}
        return self.result

    def delete(self, resource, data=None, params=None):
        r"""Send a DELETE request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self.session.delete(
            url=self.url('config', resource),
            auth=(self.username, self.password) if self.username else None,
            headers=self.headers,
            params=params,
            data=_format_body(data),
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            exception = self._determine_exception(self.response)
            if self.raise_on_failure:
                raise exception
            else:
               self.result = {'error': str(exception)}
        return self.result

    def post(self, resource, data=None):
        r"""Send a POST request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self.session.post(
            url=self.url('config', resource),
            auth=(self.username, self.password) if self.username else None,
            headers=self.headers,
            data=_format_body(data),
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            exception = self._determine_exception(self.response)
            if self.raise_on_failure:
                raise exception
            else:
               self.result = {'error': str(exception)}
        return self.result

    def put(self, resource, data=None, params=None):
        r"""Send a PUT request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self.session.put(
            url=self.url('config', resource),
            auth=(self.username, self.password) if self.username else None,
            headers=self.headers,
            params=params,
            data=_format_body(data),
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            exception = self._determine_exception(self.response)
            if self.raise_on_failure:
                raise exception
            else:
               self.result = {'error': str(exception)}
        return self.result

    def url(self, api, resource):
        """Combine attributes and resource as a url string."""
        resource = resource[1:] if resource.startswith('/') else resource
        return 'https://{0}/api/scm.{1}/{2}/{3}'.format(
            self.controller, api, self.api_version, resource,
        )

    def savefile(self, filename):
        """Save binary return data to a file."""
        with open(filename, 'wb') as f:
            f.write(self.response.content)

    def _get_result(self, response):
        if not response.ok:
            if response.text and 'Queued' in response.text:
                # work-around for get:'/node/{node_id}/image_status'
                return response.json()
            return None
        if response.headers['Content-Type'] == 'application/octet-stream':
            message = ' '.join(
                "Binary data returned."
                "Use '.savefile(filename)' method"
                "or access using '.response.content'."
            )
            return {'status': message}
        if not response.json():
            return {}
        elif 'items' in response.json():
            return response.json()['items']
        else:
            return response.json()

    def _determine_exception(self, response):
        if not response.ok:
            error = _error_string(response)
            if response.status_code == 401:
                exception = AuthenticationError(error)
            elif response.status_code == 404:
                exception = NotFoundError(error)
            elif response.status_code == 502:
                exception = APINotEnabled(error)
            else:
                exception = RuntimeError(error)
            return exception


def _error_string(response):
    """Summarize error conditions and return as a string."""
    details = ''
    if response.text:
        try:
            details = response.json()
            details = details.get('error', {}).get('message', '')
        except ValueError:
            pass
    error = '\t{0} - {1}{2}\nURL:\t\t{3}\nData Sent:\t{4}'.format(
        response.status_code,
        response.reason,
        '\nDetails:\t' + details if details else '',
        response.url,
        repr(response.request.body),
    )
    return error


def _format_body(data):
    return json.dumps(data) if data and isinstance(data, dict) else data
