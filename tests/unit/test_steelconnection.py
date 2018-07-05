# coding: utf-8

import getpass
import json
import sys
import pytest
import requests
import steelconnection
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
    """Test SConAPI.__get_result method."""
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
