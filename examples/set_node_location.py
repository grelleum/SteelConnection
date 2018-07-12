#!/usr/bin/env python


"""Update SteelConnect nodes within a specified Org
by copying the site name to the location field
for those nodes where the location is unset.

Designed to work with both Python2 and Python3.
Requires the Requests library to be installed.

USAGE:
    set_node_location.py scm.riverbed.cc organization
    set_node_location.py scm.riverbed.cc organization -u $USER -p $PASSWD
"""


from __future__ import print_function
import argparse
import sys
import steelconnection


def main(argv):
    """Update nodes."""
    args = arguments(argv)

    scm, organization = args.cloud_controller, args.organization
    if organization.endswith('.cc') and not scm.endswith('.cc'):
        scm, organization = organization, scm

    sc = steelconnection.SConAPI(
        scm,
        username=args.username,
        password=args.password,
    )

    # Find the target organization.
    org = sc.lookup.org(organization)
    print('\nOrg:', organization, '\tID:', org['id'])

    # Get list of all sites in target organization.
    sites = sc.get('org/{}/sites'.format(org['id']))
    print(status('site', sites, "in '{0}'".format(organization)))

    # Get list of all nodes in target organization.
    nodes = sc.get('org/{}/nodes'.format(org['id']))
    print(status('node', nodes, "in '{0}'".format(organization)))

    # Reduce list of nodes to those assigned to a site.
    nodes = [node for node in nodes if node['site']]
    print(status('node', nodes, 'assigned to a site'))

    # Reduce list of nodes to those not already assigned a loction.
    nodes = [node for node in nodes if not node['location']]
    print(status('node', nodes, 'with no specified location'))

    # Update location for the remaining nodes.
    return update_nodes(nodes, sc, organization, org['id'], sites)


def update_nodes(nodes, sc, organization, org_id, sites):
    """Loop through nodes and push location to SCM where applicable."""
    for node in nodes:
        print('\n' + '=' * 79, '\n')
        print('Node:', node['id'], node['serial'], node['model'])
        print('org:', node['org'], organization)
        print('site:', node['site'])
        print('location:', node['location'])
        found_site = [site for site in sites if site['id'] == node['site']]
        if not found_site:
            print('Could not locate site id:', node['site'])
            continue
        site = found_site[0]
        print("\nSetting location to '{0}'".format(site['name']))
        payload = {
            'id': node['id'],
            'org': node['org'],
            'site': node['site'],
            'serial': node['serial'],
            'model': node['model'],
            'location': site['name'],
        }
        resource = 'node/' + node['id']
        result = sc.put(resource, data=payload)
        response = sc.response
        print('Response:', response.status_code, response.reason, '\n')
        print(result)


def status(category, values, suffix=''):
    """Return status in human-readable format."""
    size = len(values)
    pluralization = '' if size == 1 else 's'
    return '* Found {0} {1}{2} {3}.'.format(
        size,
        category,
        pluralization,
        suffix
    )


def arguments(argv):
    """Get command line arguments."""
    description = (
        'Update SteelConnect nodes within a specified Org '
        'by copying the site name to the location field '
        'for those nodes where the location is unset.'
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'cloud_controller', type=str,
        help='Domain name of SteelConnect Manager',
    )
    parser.add_argument(
        'organization', type=str,
        help='Name of target organization',
    )
    parser.add_argument(
        '-u', '--username',
        help='Username for SteelConnect Manager: prompted if not supplied',
    )
    parser.add_argument(
        '-p', '--password',
        help='Password for SteelConnect Manager: prompted if not supplied',
    )
    return parser.parse_args()


if __name__ == '__main__':
    result = main(sys.argv[1:])
