# coding: utf-8

import requests
import steelconnection
import fake_requests


def test_lookup_lookup(monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    item = sc.get('orgs')[0]
    key = item['name']
    key_id = item['id']
    result = sc.lookup._lookup(domain='orgs', value=key, key='name')
    assert result == (key_id, item)


def test_lookup_node(monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    item = sc.get('nodes')[0]
    key = item['serial']
    key_id = item['id']
    result = sc.lookup.node(key)
    assert result == (key_id, item)


def test_lookup_org(monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    item = sc.get('orgs')[0]
    key = item['name']
    key_id = item['id']
    result = sc.lookup.org(key)
    assert result == (key_id, item)


def test_lookup_site(monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    item = sc.get('sites')[0]
    key = item['name']
    key_id = item['id']
    org_id = item['org']
    result = sc.lookup.site(key, orgid=org_id)
    assert result == (key_id, item)
