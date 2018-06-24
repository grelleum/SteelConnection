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


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import getpass
import json
import requests
import sys
import traceback

from .__version__ import __version__
from .lookup import _LookUp
from .input_tools import get_username, get_password



class SConAPI(object):
    """Make REST API calls to Riverbed SteelConnect Manager."""

    def __init__(
        self,
        controller,
        username=None,
        password=None,
        api_version='1.0',
        exit_on_error=False,
        raise_on_failure=True,
    ):
        """Initialize attributes."""
        if not controller.endswith('.cc'):
            raise ValueError("SteelConnect Manager's name must end with '.cc'")
        self.api_version = api_version
        self.controller = controller
        self.exit_on_error = exit_on_error
        self.raise_on_failure = raise_on_failure
        self.username = get_username() if username is None else username
        self.password = get_password() if password is None else password
        self.session = requests.Session()
        self.result = None
        self.response = None
        self.headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }
        self.lookup = _LookUp(self)
        self.__version__ = __version__

    def __bool__(self):
        """Return the success of the last request."""
        return False if self.response is None else self.response.ok 

    def __repr__(self):
        """Return a string consisting of class name, controller, and api."""
        details = ', '.join([
            "controller: '{0}'".format(self.controller),
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
        return self._request(
            request_method=self.session.get,
            api='config',
            resource=resource,
            params=params,
        )

    def getstatus(self, resource, params=None):
        r"""Send a GET request to the SteelConnect.Reporting API.

        :param str resource: api resource to get.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        return self._request(
            request_method=self.session.get,
            api='reporting',
            resource=resource,
            params=params,
        )

    def delete(self, resource, data=None, params=None):
        r"""Send a DELETE request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        return self._request(
            request_method=self.session.delete,
            api='config',
            resource=resource,
            data=data, 
        )

    def post(self, resource, data=None):
        r"""Send a POST request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        return self._request(
            request_method=self.session.post,
            api='config',
            resource=resource,
            data=data, 
        )

    def put(self, resource, data=None, params=None):
        r"""Send a PUT request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        return self._request(
            request_method=self.session.put,
            api='config',
            resource=resource,
            data=data, 
        )

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
    
    def _request(self, request_method, api, resource, data=None, params=None):
        """Send request to controller and handle response."""
        self.response = self._make_request(
            request_method=request_method,
            api=api,
            resource=resource,
            data=data, 
            params=params,
        )
        if not self.response.ok:
            # work-around for bug in get:'/node/{node_id}/image_status' response
            if self.response.text and 'Queued' in self.response.text:
                return self.response.json()
            error = _error_string(self.response)
            if self.exit_on_error:
                print(error, file=sys.stderr)
                sys.exit(1)
            elif self.raise_on_failure:
                self._tb = traceback.extract_stack()
                raise RuntimeError(error)
            return {'error': error}
        if self.response.headers['Content-Type'] == 'application/octet-stream':
            return {
                'status': (
                    "Binary data returned.  "
                    "Use '.savefile(filename)' method "
                    "or access using '.response.content'."
                )
            }
        if not self.response.json():
            self.result = {}
        elif 'items' in self.response.json():
            self.result = self.response.json()['items']
        else:
            self.result = self.response.json()
        return self.result

    def _make_request(self, request_method, api, resource, data=None, params=None):
        """Send HTTP request to SteelConnect manager."""
        if data and isinstance(data, dict):
            data = json.dumps(data)
        try:
            response = request_method(
                url=self.url(api, resource),
                auth=(self.username, self.password),
                headers=self.headers,
                params=params,
                data=data,
            )
        except Exception as e:
            if self.exit_on_error:
                error = 'Connection to SteelConnect Manager failed:'
                print(error, file=sys.stderr)
                print(e, file=sys.stderr)
                sys.exit(1)
            else:
                raise e
        return response


def _error_string(response):
    """Summarize error conditions and return as a string."""
    details = ''
    if response.text:
        try:
            details = response.json()
            details = details.get('error', {}).get('message', '')
        except ValueError:
            pass
    error = '\t{0} - {1}{2}\nURL:      \t{3}\nData Sent:\t{4}'.format(
        response.status_code,
        response.reason,
        '\nDetails:\t' + details if details else '',
        response.url,
        repr(response.request.body),
    )
    return error
