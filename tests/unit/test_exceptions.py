# coding: utf-8

import sys
import pytest
import requests
import steelconnection
import fake_requests


# Raise Exceptions:

def test_raise_exception_no_exception(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response = fake_requests.Fake_Response('', 201, {})
    sc._raise_exception(sc.response) == None


def test_raise_exception_RuntimeError(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response = fake_requests.Fake_Response('', 777, {})
    with pytest.raises(RuntimeError):
        sc._raise_exception(sc.response)


def test_raise_exception_BadRequest(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response = fake_requests.Fake_Response('', 400, {})
    with pytest.raises(steelconnection.exceptions.BadRequest):
        sc._raise_exception(sc.response)


def test_raise_exception_AuthenticationError(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response = fake_requests.Fake_Response('', 401, {})
    with pytest.raises(steelconnection.exceptions.AuthenticationError):
        sc._raise_exception(sc.response)


def test_raise_exception_InvalidResource(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response = fake_requests.Fake_Response('', 404, {})
    with pytest.raises(steelconnection.exceptions.InvalidResource):
        sc._raise_exception(sc.response)


def test_raise_exception_APINotEnabled(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.response = fake_requests.Fake_Response('', 502, {})
    with pytest.raises(steelconnection.exceptions.APINotEnabled):
        sc._raise_exception(sc.response)


# Alternate Classes:

def test_raise_exception_without_exceptions(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConWithoutExceptions('some.realm')
    sc.response = fake_requests.Fake_Response('', 502, {})
    try:
        result = sc._raise_exception(sc.response)
    except:
        assert False
    else:
        assert result == None


def test_exit_when_raise_exception_with_exit_on_error(capsys, monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConExitOnError('some.realm')
    sc.response = fake_requests.Fake_Response('', 502, {})
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sc._raise_exception(sc.response)
    captured = capsys.readouterr()
    assert captured.err == (
        "Status: 502 - Failed\nError: None\nFAKE: \nData Sent: '{}'\n"
    )
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
