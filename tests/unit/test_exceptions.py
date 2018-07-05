# coding: utf-8

import sys
import pytest
import requests
import steelconnection
import fake_requests


# Alternate Classes:

def test_raise_exception_without_exceptions(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConWithoutExceptions('some.realm')
    response = fake_requests.Fake_Response('', 502, {})
    try:
        result = sc._raise_exception(response)
    except:
        assert False
    else:
        assert result == None


def test_exit_when_raise_exception_with_exit_on_error(capsys, monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConExitOnError('some.realm')
    response = fake_requests.Fake_Response('', 502, {})
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        result = sc._raise_exception(response)
    captured = capsys.readouterr()
    assert captured.err == "502 - Failed\nURL: \nData Sent: '{}'\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
