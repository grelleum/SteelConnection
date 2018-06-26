# coding: utf-8

import steelconnection

from PRIVATE import REALM_ADMIN, ORG_ADMIN, PASSWORD
from PRIVATE import REALM_2_8, REALM_2_9, REALM_2_10, REALM_2_11


def test_lookup_lookup():
    sc = steelconnection.SConAPI(REALM_2_10, REALM_ADMIN, PASSWORD)
    items = sc.get('orgs')
    items = (item for item in items if 'name' in item)
    item = next(items)
    key = item['name']
    key_id = item['id']
    result = sc.lookup._lookup(domain='orgs', value=key, key='name')
    assert result == (key_id, item)


def test_lookup_node():
    sc = steelconnection.SConAPI(REALM_2_10, REALM_ADMIN, PASSWORD)
    items = sc.get('nodes')
    items = (item for item in items if 'serial' in item)
    item = next(items)
    key = item['serial']
    key_id = item['id']
    result = sc.lookup.node(key)
    assert result == (key_id, item)


def test_lookup_org():
    sc = steelconnection.SConAPI(REALM_2_10, REALM_ADMIN, PASSWORD)
    items = sc.get('orgs')
    items = (item for item in items if 'name' in item)
    item = next(items)
    key = item['name']
    key_id = item['id']
    result = sc.lookup.org(key)
    assert result == (key_id, item)


def test_lookup_site():
    sc = steelconnection.SConAPI(REALM_2_10, REALM_ADMIN, PASSWORD)
    items = sc.get('sites')
    items = (item for item in items if 'name' in item and 'org' in item)
    item = next(items)
    key = item['name']
    key_id = item['id']
    org_id = item['org']
    result = sc.lookup.site(key, orgid=org_id)
    assert result == (key_id, item)
