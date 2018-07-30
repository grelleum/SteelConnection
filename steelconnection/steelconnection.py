# coding: utf-8

"""SteelConnection

Convienience objects for making REST API calls
to Riverbed SteelConnect Manager.

Usage:
    sc = steelconnection.SConAPI(scm_name, username, password)

    Optional keyword api_version can be used to specify an API version number.
    Currently there is only one API version: '1.0'.

    Once you have instantiated an object as shown above,
    you can use the object to make calls to the REST API.

    For example, to get all nodes in the realm:
    nodes = sc.config.get('nodes')
    ... or in a specifc org:
    nodes = sc.config.get('/org/' + orgid + '/nodes')

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
from .input_tools import get_input, get_username
from .input_tools import get_password, get_password_once


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
        controller=None,
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
        self.__controller = controller
        self.__username = username
        self.__password = password
        self.api_version = api_version
        self.requests = requests.Session()
        self.result = None
        self.response = None
        self.headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }
        self.__version__ = __version__
        self.lookup = _LookUp(self)
        self.__scm_version = None

    @property
    def controller(self):
        while not self.__controller:
            self.__controller = get_input(
                'Enter SteelConnect Manager fully qualified domain name: '
            )
        return self.__controller

    def get(self, resource, params=None):
        r"""Send a GET request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self._request(
            request_method=self.requests.get,
            url=self.make_url('config', resource),
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
            request_method=self.requests.get,
            url=self.make_url('reporting', resource),
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
            request_method=self.requests.delete,
            url=self.make_url('config', resource),
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
            request_method=self.requests.post,
            url=self.make_url('config', resource),
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
            request_method=self.requests.put,
            url=self.make_url('config', resource),
            params=params,
            data=data,
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            self._raise_exception(self.response)
        return self.result

    def make_url(self, api, resource):
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
        with open(filename, 'wb') as fd:
            fd.write(self.response.content)

    def download_image(self, nodeid, save_as=None, quiet=False):
        r"""Download image and save to file.
        :param str nodeid: The node id of the appliance.
        :param str filename: The file path to download the image.
        """
        status = self._dl_check_status(nodeid, quiet)
        save_as = self._dl_get_file_path(status, save_as, quiet)
        if not quiet:
            print('\nDownloading file as', save_as, end=' ', flush=True)
        # Stream file content and save to disk.
        self.response = self.requests.get(
            url=self.make_url('config', '/node/{}/get_image'.format(nodeid)),
            auth=self.__auth,
            headers=self.headers,
            params={'file': source_file},
            stream=True,
        )
        with open(save_as, 'wb') as fd:
            for index, chunk in enumerate(
                    self.response.iter_content(chunk_size=65536)
                ):
                fd.write(chunk)
                if not quiet and not index % 1000:
                    print('.', end='', flush=True)
        if not quiet:
            print('\nDownload complete.')
        return self.response

    def _dl_check_status(self, nodeid, quiet):
        """Check status every second until file is ready."""
        if not quiet:
            print('Checking availability of image', end=' ', flush=True)
        while True:
            if not quiet:
                print('.', end='', flush=True)
            status = self.get('/node/{}/image_status'.format(nodeid))
            if status.get('status', False):
                break
            time.sleep(1)
        return status

    def _dl_get_file_path(self, status, save_as, quiet):
        """Get file name and determine destination file path."""
        source_file = status['image_file']
        if save_as is None:
            save_as = source_file
        if os.path.isdir(save_as):
            save_as = os.path.join(save_as, source_file)
        return save_as

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
    def sent(self):
        """Return summary of the previous API request.

        :returns: Details regarding previous API request.
        :rtype: str
        """
        return '{}: {}\nData Sent: {}'.format(
            self.response.request.method,
            self.response.request.url,
            repr(self.response.request.body),
        )

    @property
    def answer(self):
        """Return summary of the previous API response.

        :returns: Details regarding previous API request.
        :rtype: str
        """
        error_message = None
        if not self.response.ok and self.response.text:
            try:
                details = self.response.json()
                error_message = details.get('error', {}).get('message')
            except ValueError:
                pass
        return 'Status: {} - {}\nError: {}'.format(
            self.response.status_code,
            self.response.reason,
            repr(error_message),
        )

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
        exceptions = {
            400: BadRequest,
            401: AuthenticationError,
            404: InvalidResource,
            502: APINotEnabled,
        }
        if not response.ok:
            exception = exceptions.get(response.status_code, RuntimeError)
            raise exception('\n'.join((self.answer, self.sent)))

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
        scm_version = self.scm_version if self.scm_version else 'unavailable'
        details = ', '.join([
            "controller: '{0}'".format(self.controller),
            "scm version: '{0}'".format(scm_version),
            "api version: '{0}'".format(self.api_version),
            "package version: '{0}'".format(self.__version__),
        ])
        return '{0}({1})'.format(self.__class__.__name__, details)

    def __str__(self):
        """Return a string with information about this object instance.

        :returns: Information about this object.
        :rtype: str
        """
        scm_version = self.scm_version if self.scm_version else 'unavailable'
        details = [
            'SteelConnection:',
            "controller: '{0}'".format(self.controller),
            "scm version: '{0}'".format(scm_version),
            "api version: '{0}'".format(self.api_version),
            "package version: '{0}'".format(self.__version__),
        ]
        details.extend(self.sent.splitlines())
        details.extend(self.answer.splitlines())
        return '\n>> '.join(details)


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
            print(
                '\n'.join((self.answer, self.sent)),
                file=sys.stderr
            )
            sys.exit(1)
