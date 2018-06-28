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


def test_get_scm_version(monkeypatch):
    """Test SConAPI._get_scm_version method."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    scm_version = '.'.join(PATCH.responses['status'].values())
    sc = steelconnection.SConAPI('some.realm')
    assert sc._get_scm_version() == scm_version


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


# Dunder Methods:

def test_scon_bool_returns_true(monkeypatch):
    """Test __bool__ returns True when reponse is OK."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response.ok = True
    assert bool(sc) == True


def test_scon_bool_returns_false(monkeypatch):
    """Test __bool__ returns False when reponse is not OK."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response.ok = False
    assert bool(sc) == False


def test_scon_repr(monkeypatch):
    """Test __repr__ returns a proper string."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    realm = 'MYREALM'
    scm_version = '.'.join(PATCH.responses['status'].values())
    api_version = 999
    pkg_version = steelconnection.__version__
    expected = (
        "SConAPI(controller: '{0}', scm version: '{1}', "
        "api version: '{2}', package version: '{3}')"
    ).format(realm, scm_version, api_version, pkg_version)
    sc = steelconnection.SConAPI(realm, api_version=api_version)
    assert repr(sc) == expected


# Helper Functions:

def test_error_string():
    """Test _error_string generates a properly formatted string."""
    url = 'MYREALM'
    status_code = 600
    response = PATCH.Fake_Response(url, status_code, {'no': 'data'})
    expected = "{0} - Failed\nURL: {1}\nData Sent: {2}".format(
        status_code, url, repr(response.text)
    )
    error = steelconnection.steelconnection._error_string(response)
    assert error == expected


# Alternate Classes:

def test_raise_exception_when_disabled(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPIwithoutExceptions('some.realm')
    response = PATCH.Fake_Response('', 502, {})
    sc._raise_exception(response) == None

