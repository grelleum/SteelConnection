# coding: utf-8

import pytest
import requests
import steelconnection
import fake_requests


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
    scm_version = '.'.join((
        fake_requests.responses['status']['scm_version'],
        fake_requests.responses['status']['scm_build'],
    ))
    api_version = 999
    pkg_version = steelconnection.__version__
    expected = (
        "SConAPI(controller: '{0}', scm version: '{1}', "
        "api version: '{2}', package version: '{3}')"
    ).format(realm, scm_version, api_version, pkg_version)
    sc = steelconnection.SConAPI(realm, api_version=api_version)
    assert repr(sc) == expected
