# coding: utf-8

"""
This is a set of pytest functions intended to validate the examples.
This relies on a PRIVATE import (not supplied) containing personalized details.
"""

import subprocess
import steelconnection


from PRIVATE import REALM_ADMIN, PASSWORD, ORG_2_9, REALM_2_9


# examples/set_node_location.py

def test_clear_location_fields():
    sc = steelconnection.SConAPI(REALM_2_9, REALM_ADMIN, PASSWORD)
    org_id, _ = sc.lookup.org(ORG_2_9)
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
        script, REALM_2_9, ORG_2_9, REALM_ADMIN, PASSWORD,
    )
    output = subprocess.check_output(command, shell=True)
    assert output


def test_populated_location_fields():
    sc = steelconnection.SConAPI(REALM_2_9, REALM_ADMIN, PASSWORD)
    org_id, _ = sc.lookup.org(ORG_2_9)
    nodes =  sc.get('org/' + org_id + '/nodes')
    for node in nodes:
        assert node['location'] is not None
