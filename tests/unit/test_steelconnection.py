# coding: utf-8

import requests
import steelconnection
import PATCH
import json
import pytest


# Primary Methods:

def test_scon_get(monkeypatch):
    """Test SConAPI.get method."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.get('orgs') == PATCH.responses['orgs']['items']
    assert sc.get('org') == PATCH.responses['org']
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


def test_scon_getstatus(monkeypatch):
    """Test SConAPI.getstatus method."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.getstatus('orgs') == PATCH.responses['orgs']['items']
    assert sc.getstatus('org') == PATCH.responses['org']
    assert sc.response.ok
    assert '/api/scm.reporting/' in sc.response.url


def test_scon_delete(monkeypatch):
    """Test SConAPI.delete method."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.delete('orgs') == PATCH.responses['orgs']['items']
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


def test_scon_put(monkeypatch):
    """Test SConAPI.put method."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    data = PATCH.responses['org']
    assert sc.put('org', data=data) == data
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


def test_scon_post(monkeypatch):
    """Test SConAPI.post method."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    data = PATCH.responses['org']
    assert sc.post('org', data=data) == data
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


# Helper methods:

def test_scon_url(monkeypatch):
    """Test SConAPI.url method."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('NO.REALM', api_version='999')
    assert sc.url('FAKE', 'PATH') == 'https://NO.REALM/api/scm.FAKE/999/PATH'


#     def savefile(self, filename):
#         r"""Save binary return data to a file.
#         :param str filename: Where to save the response.content.
#         """       
#         with open(filename, 'wb') as f:
#             f.write(self.response.content)


# Get Results:

def test_scon_get_result_not_ok(monkeypatch):
    """Test SConAPI._get_result method."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response.ok = False
    assert sc._get_result(sc.response) is None
    sc.response.text = 'Queued'
    assert sc._get_result(sc.response) == PATCH.responses['status']


def test_scon_get_result_octet_stream(monkeypatch):
    """Test SConAPI._get_result method."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response.headers = {'Content-Type': 'application/octet-stream'}
    assert sc._get_result(sc.response) == {'status': ' '.join(
        "Binary data returned."
        "Use '.savefile(filename)' method"
        "or access using '.response.content'."
    )}


def test_scon_get_result_no_json(monkeypatch):
    """_get_results should return an empty dict when .json returns False."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response.data = False
    assert sc._get_result(sc.response) == {}


def test_scon_get_result_no_items(monkeypatch):
    """_get_results should return a dict when 'items' is not in response."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = PATCH.Fake_Response('', 200, {'A': 'B'})
    assert sc._get_result(response) == {'A': 'B'}


def test_scon_get_result_with_items(monkeypatch):
    """_get_results should return a list when 'items' is in response."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = PATCH.Fake_Response('', 200, {'items': [1, 2, 3]})
    assert sc._get_result(response) == [1, 2, 3]


# Raise Exceptions:

def test_raise_exception_no_exception(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = PATCH.Fake_Response('', 201, {})
    sc._raise_exception(response) == None


def test_raise_exception_RuntimeError(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = PATCH.Fake_Response('', 777, {})
    with pytest.raises(RuntimeError):
        sc._raise_exception(response)


def test_raise_exception_BadRequest(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = PATCH.Fake_Response('', 400, {})
    with pytest.raises(steelconnection.exceptions.BadRequest):
        sc._raise_exception(response)


def test_raise_exception_AuthenticationError(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = PATCH.Fake_Response('', 401, {})
    with pytest.raises(steelconnection.exceptions.AuthenticationError):
        sc._raise_exception(response)


def test_raise_exception_InvalidResource(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = PATCH.Fake_Response('', 404, {})
    with pytest.raises(steelconnection.exceptions.InvalidResource):
        sc._raise_exception(response)


def test_raise_exception_APINotEnabled(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = PATCH.Fake_Response('', 502, {})
    with pytest.raises(steelconnection.exceptions.APINotEnabled):
        sc._raise_exception(response)


# Authentication Methods:


#     def _authenticate(self, username=None, password=None):
#         r"""Attempt authentication.
#         Makes GET request against 'orgs' (because 'status' was introduced 
#         in 2.9).  If neither username or password are provided,
#         will make the request without auth, to see if requests package
#         can authenticate using .netrc.
#         :param str username: (optional) Admin account name.
#         :param str password: (optional) Admin account password.
#         :returns: None.
#         :rtype: None
#         """
#         attempt_netrc_auth = username is None and password is None
#         if attempt_netrc_auth:
#             try:
#                 self.get('orgs')
#             except AuthenticationError:
#                 pass
#             else:
#                 return
#         self.username, self.password = self._get_auth(username, password)
#         self.get('orgs')



#     def _get_auth(self, username=None, password=None):
#         """Prompt for username and password if not provided.

#         :param str username: (optional) Admin account name.
#         :param str password: (optional) Admin account password.
#         :returns: Tuple of strings as (username, password).
#         :rtype: (str, str)
#         """
#         username = get_username() if username is None else username
#         password = get_password_once() if password is None else password 
#         return username, password

#     def _get_scm_version(self):
#         """Get version and build number of SteelConnect Manager.

#         :returns: SteelConnect Manager version and build number.
#         :rtype: str
#         """
#         try:
#             status = self.get('status')
#         except InvalidResource:
#             return 'unavailable'
#         else:
#             scm_version = status.get('scm_version'), status.get('scm_build')
#             return '.'.join(s for s in scm_version if s)

#     def __bool__(self):
#         """Return the success of the last request.

#         :returns: True of False if last request succeeded.
#         :rtype: bool
#         """
#         return False if self.response is None else self.response.ok 

#     def __repr__(self):
#         """Return a string consisting of class name, controller, and api.

#         :returns: Information about this object.
#         :rtype: str
#         """
#         details = ', '.join([
#             "controller: '{0}'".format(self.controller),
#             "scm version: '{0}'".format(self.scm_version),
#             "api version: '{0}'".format(self.api_version),
#             "package version: '{0}'".format(self.__version__),
#         ])
#         return '{0}({1})'.format(self.__class__.__name__, details)


# def test_error_string():
#     sc = steelconnection.SConAPI(REALM_2_10, REALM_ADMIN, PASSWORD)
#     items = sc.get('orgs')
#     items = (item for item in items if 'name' in item)
#     item = next(items)
#     key = item['name']
#     key_id = item['id']
#     result = sc.lookup._lookup(domain='orgs', value=key, key='name')
#     assert result == (key_id, item)
# def _error_string(response):
#     r"""Summarize error conditions and return as a string.

#     :param requests.response response: Response from HTTP request.
#     :returns: A multiline string summarizing the error.
#     :rtype: str
#     """
#     details = ''
#     if response.text:
#         try:
#             details = response.json()
#             details = details.get('error', {}).get('message', '')
#         except ValueError:
#             pass
#     error = '{0} - {1}{2}\nURL: {3}\nData Sent: {4}'.format(
#         response.status_code,
#         response.reason,
#         '\nDetails: ' + details if details else '',
#         response.url,
#         repr(response.request.body),
#     )
#     return error


# class SConAPIwithoutExceptions(SConAPI):
#     r"""Make REST API calls to Riverbed SteelConnect Manager.

#     This version of the class does not raise exceptions
#     when an HTTP response has a non-200 series status code.
    
#     :param str controller: hostname or IP address of SteelConnect Manager.
#     :param str username: (optional) Admin account name.
#     :param str password: (optional) Admin account password.
#     :param str api_version: (optional) REST API version.
#     :returns: Dictionary or List of Dictionaries based on request.
#     :rtype: dict, or list
#     """    

#     def _raise_exception(self, response):
#         r"""Return None to short-circuit the exception process.

#         :param requests.response response: Response from HTTP request.
#         :returns: None.
#         :rtype: None
#         """
#         return None
