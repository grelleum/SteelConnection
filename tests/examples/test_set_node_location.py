# coding: utf-8

"""
This is a functional test of the script to see if it performs the task required.
Must be run from the examples directory until I figure out a way around that.
"""

import subprocess
import steelconnection


from PRIVATE import REALM_ADMIN, PASSWORD, ORG_2_9, REALM_2_9

script = 'examples/set_node_location.py'


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
