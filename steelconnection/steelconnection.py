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
import os
import requests
import sys
import time
import traceback
import warnings

from .__version__ import __version__
from .exceptions import AuthenticationError, APINotEnabled
from .exceptions import BadRequest, InvalidResource
from .lookup import _LookUp
from .input_tools import get_username, get_password, get_password_once


BINARY_DATA_MESSAGE = (
    "Binary data returned. "
    "Use '.savefile(filename)' method or access using '.response.content'."
)


class SConAPI(object):
    r"""Make REST API calls to Riverbed SteelConnect Manager.

    :param str controller: hostname or IP address of SteelConnect Manager.
    :param str username: (optional) Admin account name.
    :param str password: (optional) Admin account password.
    :param str api_version: (optional) REST API version.
    :returns: Dictionary or List of Dictionaries based on request.
    :rtype: dict, or list
    """

    def __init__(
        self,
        controller,
        username=None,
        password=None,
        api_version='1.0',
    ):
        r"""Create a new steelconnection object.

        :param str controller: hostname or IP address of SteelConnect Manager.
        :param str username: (optional) Admin account name.
        :param str password: (optional) Admin account password.
        :param str api_version: (optional) REST API version.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.controller = controller
        self.__username = username
        self.__password = password
        self.api_version = api_version
        self.session = requests.Session()
        self.result = None
        self.response = None
        self.headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }
        self.__version__ = __version__
        self.lookup = _LookUp(self)
        self.__scm_version = None

    def get(self, resource, params=None):
        r"""Send a GET request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self._request(
            request_method=self.session.get,
            url=self.url('config', resource),
            params=params,
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            self._raise_exception(self.response)
        return self.result

    def getstatus(self, resource, params=None):
        r"""Send a GET request to the SteelConnect.Reporting API.

        :param str resource: api resource to get.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self._request(
            request_method=self.session.get,
            url=self.url('reporting', resource),
            params=params,
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            self._raise_exception(self.response)
        return self.result

    def delete(self, resource, data=None, params=None):
        r"""Send a DELETE request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self._request(
            request_method=self.session.delete,
            url=self.url('config', resource),
            params=params,
            data=data,
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            self._raise_exception(self.response)
        return self.result

    def post(self, resource, data=None):
        r"""Send a POST request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self._request(
            request_method=self.session.post,
            url=self.url('config', resource),
            data=data,
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            self._raise_exception(self.response)
        return self.result

    def put(self, resource, data=None, params=None):
        r"""Send a PUT request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self._request(
            request_method=self.session.put,
            url=self.url('config', resource),
            params=params,
            data=data,
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            self._raise_exception(self.response)
        return self.result

    def url(self, api, resource):
        r"""Combine attributes and resource as a url string.

        :param str api: api route, usually 'config' or 'reporting'.
        :param str resource: resource path.
        :returns: Complete URL path to access resource.
        :rtype: str
        """
        resource = resource[1:] if resource.startswith('/') else resource
        return 'https://{0}/api/scm.{1}/{2}/{3}'.format(
            self.controller, api, self.api_version, resource,
        )

    def savefile(self, filename):
        r"""Save binary return data to a file.

        :param str filename: Where to save the response.content.
        """
        warnings.simplefilter('always', DeprecationWarning)  # Disable filter.
        warnings.warn(
            "'.savefile' method is deprecated, use '.download_image' instead",
            category=DeprecationWarning,
            stacklevel=2
        )
        warnings.simplefilter('default', DeprecationWarning)  # Reset filter.
        with open(filename, 'wb') as f:
            f.write(self.response.content)

    def download_image(self, nodeid, filepath=None):
        r"""Download image and save to file.

        :param str nodeid: The node id of the appliance.
        :param str filename: The file path to download the image.
        """
        # Check status every second until file is ready.
        while True:
            status = self.get('/node/{}/image_status'.format(nodeid))
            if status.get('status', False):
                break
            time.sleep(1)
        # Get file name and determine destination file path.
        source_file = status['image_file']
        if filepath is None:
            filepath = source_file
        if os.path.isdir(filepath):
            filepath = os.path.join(filepath, source_file)
        # Stream file content and save to disk.
        self.response = self.session.get(
            url=self.url('config', '/node/{}/get_image'.format(nodeid)),
            auth=self.__auth,
            headers=self.headers,
            params={'file': source_file},
            stream=True,
        )
        with open(filepath, 'wb') as fd:
            for chunk in self.response.iter_content(chunk_size=1024):
                fd.write(chunk)
        return self.response

    @property
    def scm_version(self):
        """Return version and build number of SteelConnect Manager.

        :returns: SteelConnect Manager version and build number.
        :rtype: str
        """
        if self.__scm_version is None:
            try:
                status = self.get('status')
            except InvalidResource:
                self.__scm_version = 'unavailable'
            else:
                version = status.get('scm_version')
                build = status.get('scm_build')
                if version and build:
                    self.__scm_version = '.'.join((version, build))
                else:
                    self.__scm_version = 'unavailable'
        return self.__scm_version

    @property
    def __auth(self):
        if self.__username and self.__password:
            return (self.__username, self.__password)
        else:
            return None

    def _request(self, request_method, url, data=None, params=None):
        r"""Send a request using the specified method.

        :param request_method: requests.session verb.
        :param str url: complete url and path.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        data=json.dumps(data) if data and isinstance(data, dict) else data
        if self.__username and not self.__password:
            self._ask_for_auth()
        response = request_method(
            url=url, auth=self.__auth, headers=self.headers,
            params=params, data=data,
        )
        if response.status_code == 401 and self.__auth is None:
            self._ask_for_auth()
            response = request_method(
                url=url, auth=self.__auth, headers=self.headers,
                params=params, data=data,
            )
        return response

    def _ask_for_auth(self):
        """Prompt for username and password if not provided."""
        if self.__username is None:
            self.__username = get_username()
        if self.__password is None:
            self.__password = get_password_once()

    def _get_result(self, response):
        r"""Return response data as native Python datatype.

        :param requests.response response: Response from HTTP request.
        :returns: Dictionary or List of Dictionaries based on response.
        :rtype: dict, list, or None
        """
        if not response.ok:
            if response.text and 'Queued' in response.text:
                # work-around for get:'/node/{node_id}/image_status'
                return response.json()
            else:
                return None
        if response.headers['Content-Type'] == 'application/octet-stream':
            return {'status': BINARY_DATA_MESSAGE}
        if not response.json():
            return {}
        elif 'items' in response.json():
            return response.json()['items']
        else:
            return response.json()

    def _raise_exception(self, response):
        r"""Return an appropriate exception if required.

        :param requests.response response: Response from HTTP request.
        :returns: Exception if non-200 response code else None.
        :rtype: BaseException, or None
        """
        if not response.ok:
            error = _error_string(response)
            if response.status_code == 400:
                raise BadRequest(error)
            elif response.status_code == 401:
                raise AuthenticationError(error)
            elif response.status_code == 404:
                raise InvalidResource(error)
            elif response.status_code == 502:
                raise APINotEnabled(error)
            else:
                raise RuntimeError(error)

    def __bool__(self):
        """Return the success of the last request in Python3.

        :returns: True of False if last request succeeded.
        :rtype: bool
        """
        return False if self.response is None else self.response.ok

    def __nonzero__(self):
        """Return the success of the last request in Python2.

        :returns: True of False if last request succeeded.
        :rtype: bool
        """
        return self.__bool__()

    def __repr__(self):
        """Return a string consisting of class name, controller, and api.

        :returns: Information about this object.
        :rtype: str
        """
        details = ', '.join([
            "controller: '{0}'".format(self.controller),
            "scm version: '{0}'".format(
                self.scm_version if self.scm_version else 'unavailable'
            ),
            "api version: '{0}'".format(self.api_version),
            "package version: '{0}'".format(self.__version__),
        ])
        return '{0}({1})'.format(self.__class__.__name__, details)


class SConWithoutExceptions(SConAPI):
    r"""Make REST API calls to Riverbed SteelConnect Manager.

    This version of the class does not raise exceptions
    when an HTTP response has a non-200 series status code.

    :param str controller: hostname or IP address of SteelConnect Manager.
    :param str username: (optional) Admin account name.
    :param str password: (optional) Admin account password.
    :param str api_version: (optional) REST API version.
    :returns: Dictionary or List of Dictionaries based on request.
    :rtype: dict, or list
    """

    def _raise_exception(self, response):
        r"""Return None to short-circuit the exception process.

        :param requests.response response: Response from HTTP request.
        :returns: None.
        :rtype: None
        """
        return None


class SConExitOnError(SConAPI):
    r"""Make REST API calls to Riverbed SteelConnect Manager.

    This version of the class will exit withou a traceback
    when an HTTP response has a non-200 series status code.

    :param str controller: hostname or IP address of SteelConnect Manager.
    :param str username: (optional) Admin account name.
    :param str password: (optional) Admin account password.
    :param str api_version: (optional) REST API version.
    :returns: Dictionary or List of Dictionaries based on request.
    :rtype: dict, or list
    """

    def _raise_exception(self, response):
        r"""Display error and exit.

        :param requests.response response: Response from HTTP request.
        :returns: None.
        :rtype: None
        """
        if not response.ok:
            error = _error_string(response)
            print(error, file=sys.stderr)
            sys.exit(1)


def _error_string(response):
    r"""Summarize error conditions and return as a string.

    :param requests.response response: Response from HTTP request.
    :returns: A multiline string summarizing the error.
    :rtype: str
    """
    details = ''
    if response.text:
        try:
            details = response.json()
            details = details.get('error', {}).get('message', '')
        except ValueError:
            pass
    error = '{0} - {1}{2}\nURL: {3}\nData Sent: {4}'.format(
        response.status_code,
        response.reason,
        '\nDetails: ' + details if details else '',
        response.url,
        repr(response.request.body),
    )
    return error
