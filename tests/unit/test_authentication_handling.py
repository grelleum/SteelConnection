# coding: utf-8

import sys
import requests
import steelconnection
import fake_requests


# Authentication Methods:

def test_ask_for_auth_with_netrc(monkeypatch):
    """_ask_for_auth should not prompt when netrc file exists."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConnect('some.realm', connection_attempts=0)
    assert sc.get('netrc') == fake_requests.netrc


def test_interactive_login_session_auth_defined():
    """Verify _interactive_login returns if session.auth is defined."""
    sc = steelconnection.SConnect('some.realm', 'USER', 'PW')
    assert sc._interactive_login('A', 'B', 0) == 'defined'


def test_interactive_login_IOError(capsys, monkeypatch):
    """Verify _interactive_login returns if session.auth is defined."""
    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', lambda x: 'xXyYzZ')
    else:
        monkeypatch.setattr('builtins.input', lambda x: 'xXyYzZ')
    monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConnect('timeout', connection_attempts=1)
    captured = capsys.readouterr()
    assert 'Cannot connect to realm:' in captured.out
    assert sc.realm == 'xXyYzZ'


def test_interactive_login_InvalidResource(capsys, monkeypatch):
    """Verify _interactive_login returns if session.auth is defined."""
    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', lambda x: 'xXyYzZ')
    else:
        monkeypatch.setattr('builtins.input', lambda x: 'xXyYzZ')
    monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConnect('InvalidResource', connection_attempts=1)
    captured = capsys.readouterr()
    assert 'does not appear to be a SteelConnect Manager.' in captured.out
    assert sc.realm == 'xXyYzZ'


def test_interactive_login_AuthenticationError(capsys, monkeypatch):
    """Verify _interactive_login returns if session.auth is defined."""
    monkeypatch.setattr('getpass.getpass', lambda x: 'mypassword')
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConnect(
        'AuthenticationError', 'USER', connection_attempts=1
    )
    captured = capsys.readouterr()
    assert captured.out == 'Authentication Failed\n'
    assert sc.session.auth == ('USER', 'mypassword')
