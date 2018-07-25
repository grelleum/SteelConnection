# coding: utf-8

import getpass
import sys
import pytest
import responses
import steelconnection

import json
import requests
import fake_requests


db = {
    'status': {
        'fw_versions': {'yogi': '2.10.2.16-yogi'},
        'scm_version': '1.23.4',
        'scm_build': '56',
    },
    'orgs': {
        'items': [{'id': 'org-12345', 'name': 'WineAndCheese'}]
    },
    'sites': {
        'items': [
            {'id': 'site-12345', 'org': 'org-12345', 'city': 'Uptown, US', 'name': 'UP'},
            {'id': 'site-56789', 'org': 'org-56789', 'city': 'Downtown, US', 'name': 'DOWN'},
        ],
    },
    'nodes': {
        'items': [
             {
                'id': 'node-12345', 'org': 'org-12345', 'site': 'site-12345',
                'serial': 'XNABCD0123456789', 'model': 'yogi'
             }
        ],
    }
}

# responses.add(
#     responses.GET,
#     'https://some.realm/api/scm.config/1.0/status',
#     json=db['status'],
#     status=200,
# )

# responses.add(
#     responses.GET,
#     'https://some.realm/api/scm.config/1.0/orgs',
#     json=db['orgs'],
#     status=200,
# )

# responses.add(
#     responses.GET,
#     'https://some.realm/api/scm.config/1.0/sites',
#     json=db['sites'],
#     status=200,
# )

# responses.add(
#     responses.GET,
#     'https://some.realm/api/scm.config/1.0/nodes',
#     json=db['nodes'],
#     status=200,
# )


# codes = {
#     'netrc401': 401,
#     'nonesuch': 404,
# }

# org = {'id': 'not_an_org_id', 'name': 'steelconnection'}
# status = {'scm_version': '2.9.1', 'scm_build': '50'}
# node = {
#     'org': 'not_an_org_id',
#     'site': 'site-mysite',
#     'id': 'node-somenode',
#     'serial': 'XNABCD0123456789',
#     'model': 'yogi',
# }
# site = {
#     'org': 'not_an_org_id',
#     'city': 'Anytown, US',
#     'id': 'site-mysite',
#     'name': 'Anytown',
# }

# netrc = node
# netrc401 = node

# responses = {
#     'org': org,
#     'orgs': {'items': [org]},
#     'status': status,
#     'node': node,
#     'nodes': {'items': [node]},
#     'site': site,
#     'sites': {'items': [site]},
#     'netrc': node,
#     'netrc401': node,
# }



# Primary Methods:


@responses.activate
def test_scon_get():
    """Test SConAPI.get method."""
    responses.add(responses.GET, 'https://some.realm/api/scm.config/1.0/orgs', json=db['orgs'], status=200)
    responses.add(responses.GET, 'https://some.realm/api/scm.config/1.0/node/node-12345', json=db['nodes']['items'][0], status=200)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.get('orgs') == db['orgs']['items']
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url
    assert sc.get('/node/node-12345') == db['nodes']['items'][0]
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


@responses.activate
def test_scon_getstatus():
    """Test SConAPI.getstatus method."""
    responses.add(responses.GET, 'https://some.realm/api/scm.reporting/1.0/node/node-12345', json=db['nodes']['items'][0], status=200)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.getstatus('/node/node-12345') == db['nodes']['items'][0]
    assert sc.response.ok
    assert '/api/scm.reporting/' in sc.response.url


@responses.activate
def test_scon_delete():
    """Test SConAPI.delete method."""
    responses.add(responses.DELETE, 'https://some.realm/api/scm.config/1.0/org/org-12345', json={}, status=200)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.delete('org/org-12345') == {}
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


@responses.activate
def test_scon_post():
    """Test SConAPI.post method."""
    responses.add(responses.POST, 'https://some.realm/api/scm.config/1.0/nodes', json=db['nodes']['items'][0], status=200)
    sc = steelconnection.SConAPI('some.realm')
    data = db['nodes']['items'][0]
    assert sc.post('nodes', data=data) == data
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


@responses.activate
def test_scon_put():
    """Test SConAPI.put method."""
    responses.add(responses.PUT, 'https://some.realm/api/scm.config/1.0/node/node-12345', json=db['nodes']['items'][0], status=200)
    sc = steelconnection.SConAPI('some.realm')
    data = db['nodes']['items'][0]
    assert sc.put('node/node-12345', data=data) == data
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


# Primary Methods can generate exceptions:

@responses.activate
def test_scon_get_exception():
    """Test SConAPI.get method."""
    responses.add(responses.GET, 'https://some.realm/api/scm.config/1.0/nonesuch', status=404)
    sc = steelconnection.SConAPI('some.realm')
    with pytest.raises(RuntimeError):
        sc.get('nonesuch')


@responses.activate
def test_scon_getstatus_exception():
    """Test SConAPI.getstatus method."""
    responses.add(responses.GET, 'https://some.realm/api/scm.reporting/1.0/nonesuch', status=404)
    sc = steelconnection.SConAPI('some.realm')
    with pytest.raises(RuntimeError):
        sc.getstatus('nonesuch')


@responses.activate
def test_scon_delete_exception():
    """Test SConAPI.delete method."""
    responses.add(responses.DELETE, 'https://some.realm/api/scm.config/1.0/nonesuch', status=404)
    sc = steelconnection.SConAPI('some.realm')
    with pytest.raises(RuntimeError):
        sc.delete('nonesuch')


@responses.activate
def test_scon_post_exception():
    """Test SConAPI.post method."""
    responses.add(responses.POST, 'https://some.realm/api/scm.config/1.0/nonesuch', status=404)
    sc = steelconnection.SConAPI('some.realm')
    data = fake_requests.responses['org']
    with pytest.raises(RuntimeError):
        sc.post('nonesuch', data=data)


@responses.activate
def test_scon_put_exception():
    """Test SConAPI.put method."""
    responses.add(responses.PUT, 'https://some.realm/api/scm.config/1.0/nonesuch', status=404)
    sc = steelconnection.SConAPI('some.realm')
    data = fake_requests.responses['org']
    with pytest.raises(RuntimeError):
        sc.put('nonesuch', data=data)


# Helper methods:

def test_scon_url():
    """Test SConAPI.url method."""
    sc = steelconnection.SConAPI('NO.REALM', api_version='999')
    assert sc.url('FAKE', 'PATH') == 'https://NO.REALM/api/scm.FAKE/999/PATH'


@responses.activate
def test_scm_version():
    """Test SConAPI.scm_version method."""
    responses.add(responses.GET, 'https://some.realm/api/scm.config/1.0/status', json=db['status'], status=200)
    scm_version = '1.23.4.56'
    sc = steelconnection.SConAPI('some.realm')
    assert sc.scm_version == scm_version


def test_scm_version_invalid(monkeypatch):
    """Test SConAPI.scm_version method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('old.school')
    assert sc.scm_version == 'unavailable'


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
    sc.response.text = '{"error":{"message":"Queued","code":404}}'
    assert sc._get_result(sc.response) == json.loads(sc.response.text)


def test_scon_get_result_octet_stream(monkeypatch):
    """Test SConAPI._get_result method."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.headers = {'Content-Type': 'application/octet-stream'}
    assert sc._get_result(sc.response) == {'status': ' '.join((
        "Binary data returned.",
        "Use '.savefile(filename)' method or access using '.response.content'."
    ))}


def test_scon_get_result_no_json(monkeypatch):
    """_get_results should return an empty dict when .json returns False."""
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('orgs')
    sc.response.text = '{}'
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
