# coding: utf-8

import sys

import pytest
import requests

import steelconnection
import fake_requests


# Authentication Methods:


def test_ask_for_auth_with_netrc(monkeypatch):
    """_ask_for_auth should not prompt when netrc file exists."""
    monkeypatch.setattr(requests, "Session", fake_requests.Fake_Session)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.get("netrc") == fake_requests.netrc


# def test_auth_get_creds_when_auth_supplied():
#     """Verify auth.get_creds returns if session.auth is defined."""
#     # TODO: review if still valid test.
#     sc = steelconnection.SConnect('some.realm', 'USER', 'PW')
#     assert steelconnection.auth.get_creds(sc, 'A', 'B', 0) == ('A', 'B')


# def test_auth_get_realm_ConnectionError(monkeypatch):
#     """Verify auth.get_realm returns 'Cannot connect for bad server."""
#     realm = 'timeout'
#     if sys.version_info.major < 3:
#         monkeypatch.setattr('__builtin__.raw_input', lambda x: realm)
#     else:
#         monkeypatch.setattr('builtins.input', lambda x: realm)
#     sc = steelconnection.SConnect('A', 'B', 'C')
#     with pytest.raises(RuntimeError):
#         steelconnection.auth.get_realm(sc, None, connection_attempts=1)


# def test_auth_get_realm_InvalidResource(capsys, monkeypatch):
#     """Verify auth.get_realm returns 'Cannot connect for bad server."""
#     realm = 'InvalidResource'
#     if sys.version_info.major < 3:
#         monkeypatch.setattr('__builtin__.raw_input', lambda x: realm)
#     else:
#         monkeypatch.setattr('builtins.input', lambda x: realm)
#     sc = steelconnection.SConnect('A', 'B', 'C')
#     with pytest.raises(RuntimeError):
#         steelconnection.auth.get_realm(sc, None, connection_attempts=1)


# def test_interactive_login_AuthenticationError(capsys, monkeypatch):
#     """Verify _interactive_login returns if session.auth is defined."""
#     monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
#     monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
#     sc = steelconnection.SConnect(
#         'AuthenticationError', 'USER', connection_attempts=1
#     )
#     captured = capsys.readouterr()
#     assert captured.out == 'Authentication Failed\n'
#     assert sc.session.auth == ('USER', 'mypassword')
