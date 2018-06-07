# coding: utf-8

"""SteelConnection

Convienience objects for making REST API calls
to Riverbed SteelConnect Manager.

Usage:
    sconnect = steelconnection.SConAPI(scm_name, username, password)

    Option keyword version can be used to specify an API version number.
    Currently there is only one API version: '1.0'.

    Once you have instantiated an object as shown above,
    you can use the object to make calls to the REST API.

    For example, to get all nodes in the realm, or in a specifc org:
    nodes = sconnect.config.get('nodes')
    nodes = sconnect.config.get(f'/org/{orgid}/nodes')  # where orgid is predefined.

    Any call that does not result in a success (HTTP status code 200)
    will raise an exception, so calls should be wrapped in a try/except pair.
"""


from __future__ import print_function
import getpass
import json
import requests
import sys

from requests import HTTPError


class SConAPI(object):
    """Make REST API calls to Riverbed SteelConnect Manager."""

    def __init__(
        self,
        controller,
        username=None,
        password=None,
        version='1.0',
        exit_on_error = False,
    ):
        """Initialize attributes."""
        if not controller.endswith('.cc'):
            raise ValueError("SteelConnect Manager's name must end with '.cc'")
        self.version = version
        self.controller = controller
        self.exit_on_error = exit_on_error
        self.username = get_username() if username is None else username
        self.password = get_password() if password is None else password
        self.session = requests.Session()
        self.response = None
        self.headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }
        self.lookup = _LookUp(self)
        # self.org = Org()

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

    def get(self, resource, data=None):
        """Make an HTTP GET request for the API resource."""
        return self._request(self.session.get, 'config', resource)

    def getstatus(self, resource, data=None):
        """Make an HTTP GET request for the API resource."""
        return self._request(self.session.get, 'reporting', resource)

    def delete(self, resource, data=None):
        """Make an HTTP DELETE request for the API resource."""
        return self._request(self.session.delete, 'config', resource)

    def post(self, resource, data=None):
        """Make an HTTP POST request for the API resource."""
        return self._request(self.session.post, 'config', resource, data)

    def put(self, resource, data=None):
        """Make an HTTP PUT request for the API resource."""
        return self._request(self.session.put, 'config', resource, data)

    def url(self, api, resource):
        """Combine attributes and resource as a url string."""
        resource = resource[1:] if resource.startswith('/') else resource
        return 'https://{0}/api/scm.{1}/{2}/{3}'.format(
            self.controller, api, self.version, resource,
        )

    def _request(self, request_method, api, resource, data=None):
        """Send HTTP request to SteelConnect manager."""
        kwargs = self._request_kwargs(api, resource, data)
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
            self.response.data = {}
        elif 'items' in self.response.json():
            self.response.data = self.response.json()['items']
        else:
            self.response.data = self.response.json()
        return self.response

    def _request_kwargs(self, api, resource, data):
        """Return a dictionary with the request keyword arguments."""
        kwargs = {
            'url': self.url(api, resource),
            'auth': (self.username, self.password),
            'headers': self.headers,
        }
        if data:
            if isinstance(data, dict):
                data = json.dumps(data)
            kwargs['data'] = data
        return kwargs


# class Org(object):
#     """Store Org ID and name in SConAPI object as attributes."""

#     def __init__(self):
#         """Initialize the organization."""
#         self.details = {}

#     @property
#     def id(self):
#         return self.details.get('id', None)

#     @property
#     def name(self):
#         return self.details.get('name', None)

#     @property
#     def longname(self):
#         return self.details.get('longname', None)


class _LookUp(object):
    """Provide convienience tools to lookup objects."""

    def __init__(self, sconnection):
        """Obtain access to SteelConect Manager."""
        self.sconnection = sconnection

    def _lookup(self, domain, value, key, return_value='id'):
        """Generic lookup function."""
        items = self.sconnection.get(domain).data
        valid_items = (item for item in items if item[key])
        matches = [item for item in valid_items if value in item[key]]
        details = max(matches) if matches else ''
        result = details[return_value]
        return result, details

    def nodeid(self, serial, key='serial'):
        """Return node id that matches appliance serial number provided."""
        result, details = self._lookup(domain='nodes', value=serial, key=key)
        return result

    def orgid(self, name, key='name'):
        """Return org id that matches organization short name provided."""
        result, details = self._lookup(domain='orgs', value=name, key=key)
        # self.sconnection.org.details = details
        return result

    def siteid(self, name, orgid=None, key='name'):
        """Return site id that matches site short name within the organization provided."""
        if not orgid:
            raise ValueError('orgid required when looking up a site.')
        resource = '/'.join(('org', orgid, 'sites'))
        result, details = self._lookup(domain=resource, value=name, key=key)
        return result


def get_input(prompt=''):
    """Get input in a Python 2/3 compatible way."""
    try:
        data = raw_input(prompt)
    except NameError:
        data = input(prompt)
    finally:
        return data


def get_username(prompt=''):
    return get_input('Enter username: ')


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