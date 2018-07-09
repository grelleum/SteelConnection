# coding: utf-8

import requests
import pytest
import steelconnection
import fake_requests


def test_lookup_lookup_success(monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    item = sc.get('orgs')[0]
    key = item['name']
    result = sc.lookup._lookup(domain='orgs', value=key, key='name')
    assert result == item


def test_lookup_lookup_fails(monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    key = 'DNE'
    result = sc.lookup._lookup(domain='orgs', value=key, key='name')
    assert result is None
    

def test_lookup_node(monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    item = sc.get('nodes')[0]
    key = item['serial']
    result = sc.lookup.node(key)
    assert result == item


def test_lookup_org(monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    item = sc.get('orgs')[0]
    key = item['name']
    result = sc.lookup.org(key)
    assert result == item


def test_lookup_site(monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    item = sc.get('sites')[0]
    key = item['name']
    org_id = item['org']
    result = sc.lookup.site(key, orgid=org_id)
    assert result == item


def test_lookup_site_without_org(monkeypatch):
    monkeypatch.setattr(requests, 'Session', fake_requests.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    item = sc.get('sites')[0]
    key = item['name']
    with pytest.raises(ValueError):
        sc.lookup.site(key)
