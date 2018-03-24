# coding: utf-8

"""SteelConnection

Convienience objects for making REST API calls
to Riverbed SteelConnect Manager.

As there are two SteelConnect APIs: 'config' and 'reporting',
so we provide two object templates for accessing the config and reporting APIs.

Usage:
    sconnect = steelconnection.Config(scm_name, username, password)
    sconnect = steelconnection.Reporting(scm_name, username, password)

    Option keyword version can be used to specify an API version number.
    Currently there is only one API version: '1.0'.

    Once you have instantiated an object as shown above,
    you can use the object to make calls to the REST API.

    For example, to get all nodes in the realm, or in a specifc org:
    nodes = sconnect.get('nodes')
    nodes = sconnect.get(f'/org/{orgid}/nodes')  # where orgid is predefined.

    Any call that does not result in a success (HTTP status code 200)
    will raise an exception, so calls should be wrapped in a try/except pair.
"""


from __future__ import print_function
import getpass
import json
import requests
import sys


class _SteelConnection(object):
    """Make REST API calls to Riverbed SteelConnect Manager."""

    def __init__(
            self,
            controller,
            username=None,
            password=None,
            api=None,
            version='1.0',
            exit_on_error = False,
    ):
        """Initialize attributes."""
        if not controller.endswith('.cc'):
            raise ValueError("SteelConnect Manager's name must end with '.cc'")
        if api not in ('config', 'reporting'):
            raise ValueError("api specified must be 'config' or 'reporting'.")
        self.api = api
        self.version = version
        self.controller = controller
        self.response = None
        self.exit_on_error = exit_on_error
        self.username = get_username() if username is None else username
        self.password = get_password() if password is None else password
        self.headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }

    def get(self, resource, data=None):
        """Make an HTTP GET request for the API resource."""
        return self._request(requests.get, resource)

    def delete(self, resource, data=None):
        """Make an HTTP DELETE request for the API resource."""
        return self._request(requests.delete, resource)

    def post(self, resource, data=None):
        """Make an HTTP POST request for the API resource."""
        return self._request(requests.post, resource, data)

    def put(self, resource, data=None):
        """Make an HTTP PUT request for the API resource."""
        return self._request(requests.put, resource, data)

    def url(self, resource):
        """Combine attributes and resource as a url string."""
        resource = resource[1:] if resource.startswith('/') else resource
        return 'https://{0}/api/scm.{1}/{2}/{3}'.format(
            self.controller, self.api, self.version, resource,
        )

    def _request(self, request_method, resource, data=None):
        """Send HTTP request to SteelConnect manager."""
        kwargs = self._request_kwargs(resource, data)
        try:
            self.response = request_method(**kwargs)
        except Exception as e:
            if self.exit_on_error:
                print('SteelConnect connection failed:', file=sys.stderr)
                print(e, file=sys.stderr)
                sys.exit(1)
            else:
                raise e
        if not self.response.ok:
            if self.exit_on_error:
                text = 'SteelConnect Response: <{0}> {1}'.format(
                    response.status_code, response.reason
                )
                print(text, file=sys.stderr)
                sys.exit(1)
            else:
                self.response.raise_for_status()
            return
        if not self.response.json():
            return self.response
        if 'items' in self.response.json():
            return self.response.json()['items']
        return self.response.json()

    def _request_kwargs(self, resource, data):
        """Return a dictionary with the request keyword arguments."""
        kwargs = {
            'url': self.url(resource),
            'auth': (self.username, self.password),
            'headers': self.headers,
        }
        if data:
            if isinstance(data, dict):
                data = json.dumps(data)
            kwargs['data'] = data
        return kwargs

    def __bool__(self):
        """Return the success of the last request."""
        if self.response is None:
            return False
        return True if self.response.status_code == 200 else False

    def __repr__(self):
        """Return a string consisting of class name, controller, and api."""
        details = ', '.join([
            "controller: '{0}'".format(self.controller),
            "api version: '{0}'".format(self.version),
            "response: '{0}'".format(self.response),
        ])
        return '{0}({1})'.format(self.__class__.__name__, details)


class Config(_SteelConnection):
    """Make config calls via REST API calls to Riverbed SteelConnect Manager."""

    def __init__(
        self,
        controller,
        username=None,
        password=None,
        version='1.0',
        exit_on_error = False,
    ):
        """Invoke parent class initialization with 'config' API."""
        super().__init__(
            controller,
            api='config',
            username=username,
            password=password,
            version=version,
        )


class Reporting(_SteelConnection):
    """Get reporting via REST API calls to Riverbed SteelConnect Manager."""

    def __init__(
        self,
        controller,
        username=None,
        password=None,
        version='1.0',
        exit_on_error = False,
    ):
        """Invoke parent class initialization with 'reporting' API."""
        super().__init__(
            controller,
            api='reporting',
            username=username,
            password=password,
            version=version,
        )


def get_username(prompt=None):
    """Get username in a Python 2/3 compatible way."""
    prompt = 'Enter username: ' if prompt is None else prompt
    try:
        username = raw_input(prompt)
    except NameError:
        username = input(prompt)
    finally:
        return username


def get_password(prompt=None, password=None):
    """Get password from terminal with discretion."""
    prompt = 'Enter password: ' if prompt is None else prompt
    while not password:
        verify = False
        while password != verify:
            if verify:
                print('Passwords do not match. Try again', file=sys.stderr)
            password = getpass.getpass(prompt)
            verify = getpass.getpass('Retype password: ')
    return password
