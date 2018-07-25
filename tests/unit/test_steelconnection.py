# coding: utf-8

import getpass
import json
import sys
import pytest
import responses
import steelconnection


class NameSpace():
    def __init__(self):
        pass


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
    with pytest.raises(RuntimeError):
        sc.post('nonesuch', data={})


@responses.activate
def test_scon_put_exception():
    """Test SConAPI.put method."""
    responses.add(responses.PUT, 'https://some.realm/api/scm.config/1.0/nonesuch', status=404)
    sc = steelconnection.SConAPI('some.realm')
    with pytest.raises(RuntimeError):
        sc.put('nonesuch', data={})


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


@responses.activate
def test_scm_version_invalid():
    """Test SConAPI.scm_version method."""
    responses.add(responses.GET, 'https://old.school/api/scm.config/1.0/status', status=404)
    sc = steelconnection.SConAPI('old.school')
    assert sc.scm_version == 'unavailable'


def test_savefile():
    """Test SConAPI.savefile method."""
    filename = 'delete.me'
    sc = steelconnection.SConAPI('some.realm')
    sc.response = NameSpace()
    sc.response.content = b'ABCDEFG1234567890'
    sc.savefile(filename)
    with open(filename, 'rb') as f:
        contents = f.read()
    assert contents == sc.response.content


# Get Results:

@responses.activate
def test_scon_get_result_not_ok():
    """Test SConAPI.__get_result method."""
    responses.add(responses.GET, 'https://some.realm/api/scm.config/1.0/nonesuch', status=404)
    sc = steelconnection.SConAPI('some.realm')
    try:
        sc.get('nonesuch')
    except RuntimeError:
        pass
    assert sc._get_result(sc.response) is None


@responses.activate
def test_scon_get_result_not_ok_with_body():
    """Test SConAPI.__get_result method."""
    responses.add(responses.GET, 'https://some.realm/api/scm.config/1.0/Queued', body='{"error":{"message":"Queued","code":404}}', status=404)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('Queued')
    assert sc._get_result(sc.response) == json.loads(sc.response.text)


@responses.activate
def test_scon_get_result_octet_stream():
    """Test SConAPI._get_result method."""
    responses.add(responses.GET, 'https://some.realm/api/scm.config/1.0/image', headers={'Content-Type': 'application/octet-stream'}, body=b'B', status=200)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('image')
    assert sc._get_result(sc.response) == {'status': ' '.join((
        "Binary data returned.",
        "Use '.savefile(filename)' method or access using '.response.content'."
    ))}


@responses.activate
def test_scon_get_result_no_json():
    """_get_results should return an empty dict when .json returns False."""
    responses.add(responses.DELETE, 'https://some.realm/api/scm.config/1.0/org/org-12345', json={}, status=200)
    sc = steelconnection.SConAPI('some.realm')
    sc.delete('org/org-12345')
    assert sc._get_result(sc.response) == {}


@responses.activate
def test_scon_get_result_no_items():
    """_get_results should return a dict when 'items' is not in response."""
    responses.add(responses.GET, 'https://some.realm/api/scm.config/1.0/node/node-12345', json=db['nodes']['items'][0], status=200)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('node/node-12345')
    assert isinstance(sc._get_result(sc.response), dict)
    assert sc._get_result(sc.response) == db['nodes']['items'][0]


@responses.activate
def test_scon_get_result_with_items():
    """_get_results should return a list when 'items' is in response."""
    responses.add(responses.GET, 'https://some.realm/api/scm.config/1.0/nodes', json=db['nodes'], status=200)
    sc = steelconnection.SConAPI('some.realm')
    sc.get('nodes')
    assert isinstance(sc._get_result(sc.response), list)
    assert sc._get_result(sc.response) == db['nodes']['items']
