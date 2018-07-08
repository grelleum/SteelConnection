# coding: utf-8

"""
This is a set of pytest functions intended to validate the examples.
This relies on a environment variables to complete.
"""

import os
import subprocess
import sys
import pytest
import steelconnection


username = os.environ.get('SCONUSER')
password = os.environ.get('SCONPASSWD')
realm = os.environ.get('SCONREALM')
org_name = os.environ.get('SCONORG')


# examples/set_node_location.py

def test_clear_location_fields():
    sc = steelconnection.SConAPI(realm, username, password)
    org_id, _ = sc.lookup.org(org_name)
    assert org_id
    nodes = sc.get('org/' + org_id + '/nodes')
    assert nodes
    for node in nodes:
        node['location'] = None
        response = sc.put('node/' + node['id'], data=node)
        assert response['location'] is None


def test_set_node_location():
    script = 'examples/set_node_location.py'
    command = 'python "{}" "{}" "{}" -u="{}" -p="{}"'.format(
        script, realm, org_name, username, password,
    )
    output = subprocess.check_output(command, shell=True)
    assert output


def test_populated_location_fields():
    sc = steelconnection.SConAPI(realm, username, password)
    org_id, _ = sc.lookup.org(org_name)
    nodes =  sc.get('org/' + org_id + '/nodes')
    for node in nodes:
        assert node['location'] is not None


# examples/create_site.py

def test_create_site(monkeypatch):
    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', lambda x: username)
    else:
        monkeypatch.setattr('builtins.input', lambda x: username)
    monkeypatch.setattr('getpass.getpass', lambda x: password)
    import create_site
    create_site.scm_name = realm
    create_site.org_name = org_name
    create_site.new_site = {
        'name': 'pytest',
        'longname': 'pytest',
        'city': 'pytest',
        'country': 'US',
        'timezone': 'America/New_York',
    }
    create_site.main()
    sc = steelconnection.SConAPI(realm, username, password)
    org_id, _ = sc.lookup.org(org_name)
    site_id, site = sc.lookup.site(create_site.new_site['name'], org_id)
    assert site_id
    for key in create_site.new_site:
        assert site[key] == create_site.new_site[key]
    sc.delete('site/' + site_id)
    site_id, _ = sc.lookup.site(create_site.new_site['name'], org_id)
    assert site_id is None



