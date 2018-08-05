# coding: utf-8

import pytest
import steelconnection
import fake_requests


# Raise Exceptions:

def test_raise_exception_no_exception():
    """_raise_exception should raise the correct exceptions based on status."""
    sc = steelconnection.SConnect(connection_attempts=0)
    sc.response = fake_requests.Fake_Response('', 201, {})
    sc._raise_exception(sc.response) is None


def test_raise_exception_RuntimeError():
    """_raise_exception should raise the correct exceptions based on status."""
    sc = steelconnection.SConnect(connection_attempts=0)
    sc.response = fake_requests.Fake_Response('', 777, {})
    with pytest.raises(RuntimeError):
        sc._raise_exception(sc.response)


def test_raise_exception_BadRequest():
    """_raise_exception should raise the correct exceptions based on status."""
    sc = steelconnection.SConnect(connection_attempts=0)
    sc.response = fake_requests.Fake_Response('', 400, {})
    with pytest.raises(steelconnection.exceptions.BadRequest):
        sc._raise_exception(sc.response)


def test_raise_exception_AuthenticationError():
    """_raise_exception should raise the correct exceptions based on status."""
    sc = steelconnection.SConnect(connection_attempts=0)
    sc.response = fake_requests.Fake_Response('', 401, {})
    with pytest.raises(steelconnection.exceptions.AuthenticationError):
        sc._raise_exception(sc.response)


def test_raise_exception_InvalidResource():
    """_raise_exception should raise the correct exceptions based on status."""
    sc = steelconnection.SConnect(connection_attempts=0)
    sc.response = fake_requests.Fake_Response('', 404, {})
    with pytest.raises(steelconnection.exceptions.InvalidResource):
        sc._raise_exception(sc.response)


def test_raise_exception_APINotEnabled():
    """_raise_exception should raise the correct exceptions based on status."""
    sc = steelconnection.SConnect(connection_attempts=0)
    sc.response = fake_requests.Fake_Response('', 502, {})
    with pytest.raises(steelconnection.exceptions.APINotEnabled):
        sc._raise_exception(sc.response)


# Alternate Classes:

def test_raise_exception_without_exceptions():
    """_raise_exception should raise the correct exceptions based on status."""
    sc = steelconnection.SConWithoutExceptions(connection_attempts=0)
    sc.response = fake_requests.Fake_Response('', 502, {})
    try:
        result = sc._raise_exception(sc.response)
    except BaseException:
        assert False
    else:
        assert result is None


def test_exit_when_raise_exception_with_exit_on_error(capsys):
    sc = steelconnection.SConExitOnError(connection_attempts=0)
    sc.response = fake_requests.Fake_Response('', 502, {})
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sc._raise_exception(sc.response)
    captured = capsys.readouterr()
    assert captured.err == (
        "Status: 502 - Failed\nError: None\nFAKE: \nData Sent: '{}'\n"
    )
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
