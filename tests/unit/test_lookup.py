# coding: utf-8

import pytest
import responses
import steelconnection


db = {
    "status": {
        "fw_versions": {"yogi": "2.10.2.16-yogi"},
        "scm_version": "1.23.4",
        "scm_build": "56",
    },
    "orgs": {"items": [{"id": "org-12345", "name": "WineAndCheese"}]},
    "sites": {
        "items": [
            {
                "id": "site-12345",
                "org": "org-12345",
                "city": "Uptown, US",
                "name": "UP",
            },
            {
                "id": "site-56789",
                "org": "org-56789",
                "city": "Downtown, US",
                "name": "DOWN",
            },
        ]
    },
    "nodes": {
        "items": [
            {
                "id": "node-12345",
                "org": "org-12345",
                "site": "site-12345",
                "serial": "XNABCD0123456789",
                "model": "yogi",
            }
        ]
    },
}


get_nodes = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/nodes",
    json=db["nodes"],
    status=200,
)

get_sites_from_org = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/org/org-12345/sites",
    json=db["sites"],
    status=200,
)

get_orgs = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/orgs",
    json=db["orgs"],
    status=200,
)


@responses.activate
def test_lookup_lookup_success():
    responses.add(get_orgs)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    item = db["orgs"]["items"][0]
    key = item["name"]
    result = sc.lookup._lookup(domain="orgs", value=key, key="name")
    assert result == item


@responses.activate
def test_lookup_lookup_fails():
    responses.add(get_orgs)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    key = "DNE"
    result = sc.lookup._lookup(domain="orgs", value=key, key="name")
    assert result is None


@responses.activate
def test_lookup_node():
    responses.add(get_nodes)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    item = db["nodes"]["items"][0]
    key = item["serial"]
    result = sc.lookup.node(key)
    assert result == item


@responses.activate
def test_lookup_org():
    responses.add(get_orgs)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    item = db["orgs"]["items"][0]
    key = item["name"]
    result = sc.lookup.org(key)
    assert result == item


@responses.activate
def test_lookup_site():
    responses.add(get_orgs)
    responses.add(get_sites_from_org)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    item = db["sites"]["items"][0]
    key = item["name"]
    org_id = item["org"]
    result = sc.lookup.site(key, orgid=org_id)
    assert result == item


@responses.activate
def test_lookup_site_without_org():
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    item = db["sites"]["items"][0]
    key = item["name"]
    with pytest.raises(ValueError):
        sc.lookup.site(key)


def test_lookup_model():
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.lookup.model("panda") == "SDI-130"
    assert sc.lookup.model("SDI-1030") == "grizzly"
