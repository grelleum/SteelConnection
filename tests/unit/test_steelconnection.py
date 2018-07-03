# coding: utf-8

import getpass
import json
import sys
import pytest
import requests
import steelconnection
import steelconnection.__main__  # for coverage sake.
import fake_requests


# Primary Methods:

def test_scon_get(monkeypatch):
    """Test SConAPI.get method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.get('orgs') == fake_requests.responses['orgs']['items']
    assert sc.get('org') == fake_requests.responses['org']
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


def test_scon_getstatus(monkeypatch):
    """Test SConAPI.getstatus method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.getstatus('orgs') == fake_requests.responses['orgs']['items']
    assert sc.getstatus('org') == fake_requests.responses['org']
    assert sc.response.ok
    assert '/api/scm.reporting/' in sc.response.url


def test_scon_delete(monkeypatch):
    """Test SConAPI.delete method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.delete('orgs') == fake_requests.responses['orgs']['items']
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


def test_scon_post(monkeypatch):
    """Test SConAPI.post method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    data = fake_requests.responses['org']
    assert sc.post('org', data=data) == data
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


def test_scon_put(monkeypatch):
    """Test SConAPI.put method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    data = fake_requests.responses['org']
    assert sc.put('org', data=data) == data
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


# Primary Methods can generate exceptions:

def test_scon_get_exception(monkeypatch):
    """Test SConAPI.get method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    with pytest.raises(RuntimeError):
        sc.get('nonesuch')


def test_scon_getstatus_exception(monkeypatch):
    """Test SConAPI.getstatus method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    with pytest.raises(RuntimeError):
        sc.getstatus('nonesuch')


def test_scon_delete_exception(monkeypatch):
    """Test SConAPI.delete method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    with pytest.raises(RuntimeError):
        sc.delete('nonesuch')


def test_scon_put_exception(monkeypatch):
    """Test SConAPI.put method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    data = fake_requests.responses['org']
    with pytest.raises(RuntimeError):
        sc.put('nonesuch', data=data)


def test_scon_post_exception(monkeypatch):
    """Test SConAPI.post method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    data = fake_requests.responses['org']
    with pytest.raises(RuntimeError):
        sc.post('nonesuch', data=data)


# Helper methods:

def test_scon_url(monkeypatch):
    """Test SConAPI.url method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('NO.REALM', api_version='999')
    assert sc.url('FAKE', 'PATH') == 'https://NO.REALM/api/scm.FAKE/999/PATH'


def test_scm_version(monkeypatch):
    """Test SConAPI.scm_version method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    scm_version = '.'.join(fake_requests.responses['status'].values())
    sc = steelconnection.SConAPI('some.realm')
    assert sc.scm_version == scm_version


def test_savefile(monkeypatch):
    """Test SConAPI.savefile method."""
    filename = 'delete.me'
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.content = b'ABCDEFG1234567890'
    sc.savefile(filename)
    with open(filename, 'rb') as f:
        contents = f.read()
    assert sc.response.content == contents


# Get Results:

def test_scon_get_result_not_ok(monkeypatch):
    """Test SConAPI._get_result method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    _ = sc.scm_version
    sc.response.ok = False
    assert sc._get_result(sc.response) is None
    sc.response.text = 'Queued'
    assert sc._get_result(sc.response) == fake_requests.responses['status']


def test_scon_get_result_octet_stream(monkeypatch):
    """Test SConAPI._get_result method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.headers = {'Content-Type': 'application/octet-stream'}
    assert sc._get_result(sc.response) == {'status': ' '.join(
        "Binary data returned.\n"
        "Use '.savefile(filename)' method or access using '.response.content'."
    )}


def test_scon_get_result_no_json(monkeypatch):
    """_get_results should return an empty dict when .json returns False."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.data = False
    assert sc._get_result(sc.response) == {}


def test_scon_get_result_no_items(monkeypatch):
    """_get_results should return a dict when 'items' is not in response."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = fake_requests.Fake_Response('', 200, {'A': 'B'})
    assert sc._get_result(response) == {'A': 'B'}


def test_scon_get_result_with_items(monkeypatch):
    """_get_results should return a list when 'items' is in response."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = fake_requests.Fake_Response('', 200, {'items': [1, 2, 3]})
    assert sc._get_result(response) == [1, 2, 3]


# Raise Exceptions:

def test_raise_exception_no_exception(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = fake_requests.Fake_Response('', 201, {})
    sc._raise_exception(response) == None


def test_raise_exception_RuntimeError(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = fake_requests.Fake_Response('', 777, {})
    with pytest.raises(RuntimeError):
        sc._raise_exception(response)


def test_raise_exception_BadRequest(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = fake_requests.Fake_Response('', 400, {})
    with pytest.raises(steelconnection.exceptions.BadRequest):
        sc._raise_exception(response)


def test_raise_exception_AuthenticationError(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = fake_requests.Fake_Response('', 401, {})
    with pytest.raises(steelconnection.exceptions.AuthenticationError):
        sc._raise_exception(response)


def test_raise_exception_InvalidResource(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = fake_requests.Fake_Response('', 404, {})
    with pytest.raises(steelconnection.exceptions.InvalidResource):
        sc._raise_exception(response)


def test_raise_exception_APINotEnabled(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    response = fake_requests.Fake_Response('', 502, {})
    with pytest.raises(steelconnection.exceptions.APINotEnabled):
        sc._raise_exception(response)


# Authentication Methods:


# Challenge here is to make first FAKE request fail, due to lack of auth.

# def test_authenticate_without_providing_auth(monkeypatch):
#     """_authenticate should prompt for user and password when netrc fails."""
#     if sys.version_info.major < 3:
#         monkeypatch.setattr('__builtin__.raw_input', lambda x: 'SteelConnect')
#     else:
#         monkeypatch.setattr('builtins.input', lambda x: 'SteelConnect')
#     monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
#     monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
#     sc = steelconnection.SConAPI('some.realm')
#     assert sc.username == 'SteelConnect'
#     assert sc.password == 'mypassword'


def test_ask_for_auth_with_netrc(monkeypatch):
    """_ask_for_auth should not prompt when netrc file exists."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.get('netrc') == fake_requests.netrc


# def test_get_auth_without_netrc(monkeypatch):
#     """_get_auth should prompt for both user and password."""
#     if sys.version_info.major < 3:
#         monkeypatch.setattr('__builtin__.raw_input', lambda x: 'SteelConnect')
#     else:
#         monkeypatch.setattr('builtins.input', lambda x: 'SteelConnect')
#     monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
#     monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
#     sc = steelconnection.SConAPI('some.realm')
#     assert sc.get('netrc401') == fake_requests.netrc
#     assert sc.username, sc.password == ('SteelConnect', 'mypassword')


def test_ask_for_auth_when_not_provided(monkeypatch):
    """_ask_for_auth should prompt for both user and password."""
    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', lambda x: 'SteelConnect')
    else:
        monkeypatch.setattr('builtins.input', lambda x: 'SteelConnect')
    monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc._SConAPI__ask_for_auth()
    assert sc._SConAPI__auth == ('SteelConnect', 'mypassword')


def test_ask_for_auth_username_provided(monkeypatch):
    """_ask_for_auth should prompt for password only when username is provided."""
    monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm', username='A')
    sc._SConAPI__ask_for_auth()
    assert sc._SConAPI__auth == ('A', 'mypassword')


def test_ask_for_auth_passwd_provided(monkeypatch):
    """_ask_for_auth should prompt for username only when password is provided."""
    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', lambda x: 'SteelConnect')
    else:
        monkeypatch.setattr('builtins.input', lambda x: 'SteelConnect')
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm', password='B')
    sc._SConAPI__ask_for_auth()
    assert sc._SConAPI__auth == ('SteelConnect', 'B')


def test_ask_for_auth_both_provided(monkeypatch):
    """_ask_for_auth should return user/pass when both are provided."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm', username='A', password='B')
    sc._SConAPI__ask_for_auth()
    assert sc._SConAPI__auth == ('A', 'B')


# Dunder Methods:

def test_scon_returns_true(monkeypatch):
    """Test object returns True when reponse is OK."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.ok = True
    assert bool(sc)


def test_scon_returns_false(monkeypatch):
    """Test object returns False when reponse is not OK."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.ok = False
    assert not bool(sc)


def test_scon_bool_returns_true(monkeypatch):
    """Test __bool__ returns True when reponse is OK."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.ok = True
    assert sc.__bool__()


def test_scon_bool_returns_false(monkeypatch):
    """Test __bool__ returns False when reponse is not OK."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.ok = False
    assert not sc.__bool__()


def test_scon_nonzero_returns_true(monkeypatch):
    """Test __bool__ returns True when reponse is OK."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.ok = True
    assert sc.__nonzero__()


def test_scon_nonzero_returns_false(monkeypatch):
    """Test __bool__ returns False when reponse is not OK."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.ok = False
    assert not sc.__nonzero__()


def test_scon_repr(monkeypatch):
    """Test __repr__ returns a proper string."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    realm = 'MYREALM'
    scm_version = '.'.join(fake_requests.responses['status'].values())
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
    response = fake_requests.Fake_Response(url, status_code, {'no': 'data'})
    expected = "{0} - Failed\nURL: {1}\nData Sent: {2}".format(
        status_code, url, repr(response.text)
    )
    error = steelconnection.steelconnection._error_string(response)
    assert error == expected


# Alternate Classes:

def test_raise_exception_when_disabled(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConWithoutExceptions('some.realm')
    response = fake_requests.Fake_Response('', 502, {})
    sc._raise_exception(response) == None

def test_raise_exception_when_exit_on_error(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    monkeypatch.setattr('sys.exit', lambda x: 'EXIT')
    sc = steelconnection.SConExitOnError('some.realm')
    response = fake_requests.Fake_Response('', 502, {})
    sc._raise_exception(response) == None

