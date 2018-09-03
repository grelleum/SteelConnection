# coding: utf-8

"""SteelConnection

Convienience objects for making REST API calls
to Riverbed SteelConnect Manager.

Usage:
    sc = steelconnection.SConnect(scm_name, username, password)

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

import json
import requests
import sys
import warnings

from requests.utils import get_netrc_auth
from .__version__ import __version__
from .exceptions import AuthenticationError, APINotEnabled
from .exceptions import BadRequest, ResourceGone, InvalidResource
from .image_download import _download_image
from .lookup import _LookUp
from .input_tools import get_input, get_username, get_password_once


ASCII_ART = r"""
   ______          _______                       __  _
  / __/ /____ ___ / / ___/__  ___  ___  ___ ____/ /_(_)__  ___
 _\ \/ __/ -_) -_) / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
/___/\__/\__/\__/_/\___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/
"""

BINARY_DATA_MESSAGE = (
    "Binary data returned. "
    "Use '.savefile(filename)' method or access using '.response.content'."
)


class SConnect(object):
    r"""Make REST API calls to Riverbed SteelConnect Manager.

    :param str realm: hostname or IP address of SteelConnect Manager.
    :param str username: (optional) Admin account name.
    :param str password: (optional) Admin account password.
    :param str api_version: (optional) REST API version.
    :returns: Dictionary or List of Dictionaries based on request.
    :rtype: dict, or list
    """

    def __init__(
        self,
        realm=None,
        username=None,
        password=None,
        api_version='1.0',
        proxies=None,
        on_error='raise',
        timeout=(5, 60),
        connection_attempts=3,
    ):
        r"""Create a new steelconnection object.

        :param str realm: hostname or IP address of SteelConnect Manager.
        :param str username: (optional) Admin account name.
        :param str password: (optional) Admin account password.
        :param str api_version: (optional) REST API version.
        :param dict proxies: (optional) Dictionary of proxy servers.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.realm = self._get_realm(realm)
        self.__scm_version = None
        self.__version__ = __version__
        self.api_version = api_version
        self.ascii_art = ASCII_ART
        self.timeout = timeout
        self.result = None
        self.response = None
        self.lookup = _LookUp(self)
        self._raise_exception = self._exception_handling(on_error)
        self.session = requests.Session()
        self.session.proxies = proxies if proxies else self.session.proxies
        self.session.headers.update({'Accept': 'application/json'})
        self.session.headers.update({'Content-type': 'application/json'})
        self.session.auth = self._set_session_auth(username, password)
        if not self.session.auth:
            self._interactive_login(username, password, connection_attempts)

    # Authentication related methods.

    def _get_realm(self, realm):
        """Prompt user for realm if not already supplied.

        :param str realm: hostname or IP address of SteelConnect Manager.
        :rtype: str
        """
        while not realm:
            realm = get_input(
                'Enter SteelConnect Manager fully qualified domain name: '
            )
        return realm

    def _set_session_auth(self, username, password):
        """Return a tuple of username and password
        If both are supplied, return those, otherwise check .netrc file.

        :param str realm: hostname or IP address of SteelConnect Manager.
        :rtype: tuple
        """
        if username and password:
            return username, password
        if not username and not password:
            return get_netrc_auth('https://' + self.realm)

    def _interactive_login(self, username, password, connection_attempts):
        r"""Make a connection to SteelConnect."""

        if self.session.auth:
            return 'defined'
        username_supplied = username
        for attempt in range(connection_attempts):
            if not username:
                username = get_username()
            if not password:
                password = get_password_once()
            self.session.auth = (username, password)
            try:
                self.get('orgs')
            except IOError as e:
                # Could not connect to server.
                print('Error:', e)
                print('Cannot connect to realm: ', self.realm)
                self.realm = self._get_realm(None)
                self.__scm_version = None
            except InvalidResource as e:
                # Connected to a webserver, but not SteelConnect.
                print(e)
                print(
                    "'{}'".format(self.realm),
                    "does not appear to be a SteelConnect Manager."
                )
                self.realm = self._get_realm(None)
                self.__scm_version = None
            except AuthenticationError:
                print('Authentication Failed')
                username = username_supplied
                password = None
            else:
                return self.response.ok

    # Primary methods:

    def get(self, resource, params=None):
        r"""Send a GET request to the SteelConnect.Config API.

        :param str resource: api resource to get.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self._request(
            request_method=self.session.get,
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
            request_method=self.session.get,
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
            request_method=self.session.delete,
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
            request_method=self.session.post,
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
            request_method=self.session.put,
            url=self.make_url('config', resource),
            params=params,
            data=data,
        )
        self.result = self._get_result(self.response)
        if self.result is None:
            self._raise_exception(self.response)
        return self.result

    def stream(self, resource, params=None):
        r"""Send a GET request with streaming binary data.

        :param str resource: api resource to get.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: dict, or list
        """
        self.response = self.session.get(
            url=self.make_url('config', resource),
            params=params,
            stream=True,
        )
        for chunk in self.response.iter_content(chunk_size=65536):
            yield chunk

    # These do the heavy lifting.

    def make_url(self, api, resource):
        r"""Combine attributes and resource as a url string.

        :param str api: api route, usually 'config' or 'reporting'.
        :param str resource: resource path.
        :returns: Complete URL path to access resource.
        :rtype: str
        """
        resource = resource[1:] if resource.startswith('/') else resource
        return 'https://{}/api/scm.{}/{}/{}'.format(
            self.realm, api, self.api_version, resource,
        )

    def _request(self, request_method, url, data=None, params=None):
        r"""Send a request using the specified method.

        :param request_method: requests.session verb.
        :param str url: complete url and path.
        :param dict data: (optional) Dictionary of 'body' data to be sent.
        :param dict params: (optional) Dictionary of query parameters.
        :returns: Dictionary or List of Dictionaries based on request.
        :rtype: object
        """
        data = json.dumps(data) if data and isinstance(data, dict) else data
        response = request_method(
            url=url, params=params, data=data, timeout=self.timeout,
        )
        return response

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

    # These handle binary content.

    def download_image(self, nodeid, save_as=None, build=None, quiet=False):
        r"""Download image and save to file.
        :param str nodeid: The node id of the appliance.
        :param str save_as: The file path to download the image.
        :param str build: Target hypervisor for image.
        :param bool quiet: Disable update printing when true.
        """
        return _download_image(
            sconnect=self,
            nodeid=nodeid,
            save_as=save_as,
            build=build,
            quiet=quiet,
        )

    def savefile(self, filename):
        r"""Save binary return data to a file.

        :param str filename: Where to save the response.content.
        """
        with open(filename, 'wb') as fd:
            fd.write(self.response.content)

    # Property methods that appear like dynamic attributes.

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
    def received(self):
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

    # Error handling and Exception generation.

    def _exception_handling(self, on_error):
        choices = {
            'raise': self._on_error_raise_exception,
            'exit': self._on_error_exit,
        }
        return choices.get(on_error, self._on_error_do_nothing)

    def _on_error_raise_exception(self, response):
        r"""Return an appropriate exception if required.

        :param requests.response response: Response from HTTP request.
        :returns: Exception if non-200 response code else None.
        :rtype: BaseException, or None
        """
        exceptions = {
            400: BadRequest,
            401: AuthenticationError,
            404: InvalidResource,
            410: ResourceGone,
            502: APINotEnabled,
        }
        if not response.ok:
            exception = exceptions.get(response.status_code, RuntimeError)
            raise exception('\n'.join((self.received, self.sent)))

    def _on_error_exit(self, response):
        r"""Display error and exit.

        :param requests.response response: Response from HTTP request.
        :returns: None.
        :rtype: None
        """
        if not response.ok:
            print(
                '\n'.join((self.received, self.sent)),
                file=sys.stderr
            )
            sys.exit(1)

    def _on_error_do_nothing(self, response):
        r"""Return None to short-circuit the exception process.

        :param requests.response response: Response from HTTP request.
        :returns: None.
        :rtype: None
        """
        return None

    # Gratuitous __dunder__ methods.

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
        """Return a string consisting of class name, realm, and api.

        :returns: Information about this object.
        :rtype: str
        """
        scm_version = self.scm_version if self.scm_version else 'unavailable'
        details = ', '.join([
            "realm: '{}'".format(self.realm),
            "scm version: '{}'".format(scm_version),
            "api version: '{}'".format(self.api_version),
            "package version: '{}'".format(self.__version__),
        ])
        return '{}({})'.format(self.__class__.__name__, details)

    def __str__(self):
        """Return a string with information about this object instance.

        :returns: Information about this object.
        :rtype: str
        """
        scm_version = self.scm_version if self.scm_version else 'unavailable'
        details = [
            'SteelConnection:',
            "realm: '{}'".format(self.realm),
            "scm version: '{}'".format(scm_version),
            "api version: '{}'".format(self.api_version),
            "package version: '{}'".format(self.__version__),
        ]
        details.extend(self.sent.splitlines())
        details.extend(self.received.splitlines())
        return '\n>> '.join(details)


# Deprecated classes.

def SConAPI(*args, **kwargs):
    warnings.simplefilter('always', DeprecationWarning)  # Disable filter.
    warnings.warn(
        "'SConAPI' is deprecated, "
        "use steelconnection.SConnect() instead",
        category=DeprecationWarning,
        stacklevel=2
    )
    warnings.simplefilter('default', DeprecationWarning)  # Reset filter.
    return SConnect(*args, **kwargs)


def SConWithoutExceptions(*args, **kwargs):
    warnings.simplefilter('always', DeprecationWarning)  # Disable filter.
    warnings.warn(
        "'SConWithoutExceptions' is deprecated, "
        "use steelconnection.SConnect(on_error=None) instead",
        category=DeprecationWarning,
        stacklevel=2
    )
    warnings.simplefilter('default', DeprecationWarning)  # Reset filter.
    return SConnect(*args, on_error=None, **kwargs)


def SConExitOnError(*args, **kwargs):
    warnings.simplefilter('always', DeprecationWarning)  # Disable filter.
    warnings.warn(
        "'SConExitOnError' is deprecated, "
        "use steelconnection.SConnect(on_error=None) instead",
        category=DeprecationWarning,
        stacklevel=2
    )
    warnings.simplefilter('default', DeprecationWarning)  # Reset filter.
    return SConnect(*args, on_error='exit', **kwargs)
