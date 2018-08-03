# coding: utf-8

"""
test_set_node_location.py

Pytest functions intended to validate examples/set_node_location.py.
This relies on a environment variables to complete.
"""

import os
import subprocess
import steelconnection


username = os.environ.get('SCONUSER')
password = os.environ.get('SCONPASSWD')
realm = os.environ.get('SCONREALM')
org_name = os.environ.get('SCONORG')

# dir_path = os.path.dirname(os.path.realpath(__file__))


def test_clear_location_fields():
    sc = steelconnection.SConAPI(realm, username, password)
    org = sc.lookup.org(org_name)
    assert org['id']
    nodes = sc.get('org/' + org['id'] + '/nodes')
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
    org = sc.lookup.org(org_name)
    nodes = sc.get('org/' + org['id'] + '/nodes')
    for node in nodes:
        assert node['location'] is not None
