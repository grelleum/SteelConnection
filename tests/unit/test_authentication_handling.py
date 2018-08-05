# coding: utf-8

# import getpass
import sys
import requests
import steelconnection
import fake_requests


# Authentication Methods:


# Challenge here is to make first FAKE request fail, due to lack of auth.

# def test_authenticate_without_providing_auth(monkeypatch):
#     """_authenticate should prompt for user and password when netrc fails."""
#     if sys.version_info.major < 3:
#         monkeypatch.setattr('__builtin__.raw_input', lambda x: 'xXyYzZ')
#     else:
#         monkeypatch.setattr('builtins.input', lambda x: 'xXyYzZ')
#     monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
#     monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
#     sc = steelconnection.SConnect('some.realm', connection_attempts=0)
#     assert sc.username == 'xXyYzZ'
#     assert sc.password == 'mypassword'


def test_ask_for_auth_with_netrc(monkeypatch):
    """_ask_for_auth should not prompt when netrc file exists."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConnect('some.realm', connection_attempts=0)
    assert sc.get('netrc') == fake_requests.netrc


# def test_get_auth_without_netrc(monkeypatch):
#     """_get_auth should prompt for both user and password."""
#     if sys.version_info.major < 3:
#         monkeypatch.setattr('__builtin__.raw_input', lambda x: 'xXyYzZ')
#     else:
#         monkeypatch.setattr('builtins.input', lambda x: 'xXyYzZ')
#     monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
#     monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
#     sc = steelconnection.SConnect('some.realm', connection_attempts=0)
#     assert sc.get('netrc401') == fake_requests.netrc
#     assert sc.username, sc.password == ('xXyYzZ', 'mypassword')


def test_ask_for_auth_when_not_provided(monkeypatch):
    """_ask_for_auth should prompt for both user and password."""
    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', lambda x: 'xXyYzZ')
    else:
        monkeypatch.setattr('builtins.input', lambda x: 'xXyYzZ')
    monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConnect('some.realm', connection_attempts=0)
    sc._ask_for_auth()
    sc.get('status')
    assert sc.response.auth == ('xXyYzZ', 'mypassword')


def test_ask_for_auth_username_provided(monkeypatch):
    """
    _ask_for_auth should prompt for password
    when only username is provided.
    """
    monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConnect('some.realm', username='A')
    sc._ask_for_auth()
    sc.get('status')
    assert sc.response.auth == ('A', 'mypassword')


def test_ask_for_auth_passwd_provided(monkeypatch):
    """
    _ask_for_auth should prompt for username
    when only password is provided.
    """
    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', lambda x: 'xXyYzZ')
    else:
        monkeypatch.setattr('builtins.input', lambda x: 'xXyYzZ')
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConnect('some.realm', password='B')
    sc._ask_for_auth()
    sc.get('status')
    assert sc.response.auth == ('xXyYzZ', 'B')


def test_ask_for_auth_both_provided(monkeypatch):
    """_ask_for_auth should return user/pass when both are provided."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConnect('some.realm', username='A', password='B')
    sc._ask_for_auth()
    sc.get('status')
    assert sc.response.auth == ('A', 'B')


def test_request_prompts_password_when_username_provided(monkeypatch):
    """_request should prompt for password only when username is provided."""
    monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConnect('some.realm', username='A')
    assert sc._request(sc.session.get, 'url')
    sc.get('status')
    assert sc.response.auth == ('A', 'mypassword')
