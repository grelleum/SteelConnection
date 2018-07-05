# coding: utf-8

import getpass
import json
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
    sc._raise_exception(response) == None

def test_raise_exception_when_exit_on_error(monkeypatch):
    """_raise_exception should raise the correct exceptions based on status."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    monkeypatch.setattr('sys.exit', lambda x: 'EXIT')
    sc = steelconnection.SConExitOnError('some.realm')
    response = fake_requests.Fake_Response('', 502, {})
    sc._raise_exception(response) == None
