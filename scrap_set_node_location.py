#!/opt/support/bin/python3


"""Update SteelConnect nodes within a specified Org
by copying the site name to the location field
for those nodes where the location is unset.

Designed to work with both Python2 and Python3.
Requires the Requests library to be installed.

USAGE:
    scrap_set_node_location.py scm.riverbed.cc organization

"""


from __future__ import print_function
import argparse
import getpass
import json
import requests
import sys


def main(argv):
    """Update nodes."""
    args = arguments(argv)

    scm, organization = args.cloud_controller, args.organization
    if organization.endswith('.cc') and not scm.endswith('.cc'):
        scm, organization = organization, scm
    baseurl = 'https://' + scm + '/api/scm.config/1.0/'

    username = args.username if args.username else get_username()
    password = args.password if args.password else get_password(username)
    auth = (username, password)

    org_id = find_org(baseurl, auth, organization)
    sites = find_sites(baseurl, auth, organization, org_id)
    nodes = find_nodes(baseurl, auth, organization, org_id)
    return update_nodes(nodes, baseurl, auth, organization, org_id, sites)


def update_nodes(nodes, baseurl, auth, organization, org_id, sites):
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
        payload = json.dumps({
            'id': node['id'],
            'org': node['org'],
            'site': node['site'],
            'serial': node['serial'],
            'model': node['model'],
            'location': site['name'],
        })
        url = baseurl + 'node/' + node['id']
        response = put(url, payload=payload, auth=auth)
        print('Response:', response.status_code, response.reason)
        print(response.text)


def find_org(baseurl, auth, organization):
    """Find the org id for the target organization."""
    print('\nFinding organization:')
    orgs = get(baseurl + 'orgs', auth=auth)
    org_found = [org for org in orgs if org['name'] == organization]
    if not org_found:
        org_found = [org for org in orgs if org['longname'] == organization]
    if not org_found:
        print("Could not find and org with name '{0}'".format(organization))
        return 1
    org = org_found[0]
    org_id = org['id']
    print('* id:', org["id"])
    print('* name:', org["name"])
    print('* longname:', org["longname"])
    return org_id


def find_sites(baseurl, auth, organization, org_id):
    """Get list of sites for specified organization."""
    print('\nGathering Sites:')
    sites = get(baseurl + 'sites', auth=auth)
    sites = [site for site in sites if site['org'] == org_id]
    print(status('site', sites, "in '{0}'".format(organization)))
    return sites


def find_nodes(baseurl, auth, organization, org_id):
    """Get nodes that require modification."""
    print('\nGathering Nodes:')

    nodes = get(baseurl + 'nodes', auth=auth)
    print(status('node', nodes, 'in Total'))

    nodes = [node for node in nodes if node['org'] == org_id]
    print(status('node', nodes, "in '{0}'".format(organization)))

    nodes = [node for node in nodes if node['site']]
    print(status('node', nodes, 'assigned to a site'))

    nodes = [node for node in nodes if not node['location']]
    print(status('node', nodes, 'with no specified location'))
    return nodes


def status(category, values, suffix=''):
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
        'cloud_controller',
        type=str,
        help='Domain name of SteelConnect Manager',
    )
    parser.add_argument(
        'organization',
        type=str,
        help='Name of target organization',
    )
    parser.add_argument(
        '-u',
        '--username',
        help='Username for SteelConnect Manager: prompted if not supplied',
    )
    parser.add_argument(
        '-p',
        '--password',
        help='Password for SteelConnect Manager: prompted if not supplied',
    )
    return parser.parse_args()


def get_username():
    """Get username in a Python 2/3 compatible way."""
    prompt = 'Enter SCM username: '
    try:
        username = raw_input(prompt)
    except NameError:
        username = input(prompt)
    finally:
        return username


def get_password(username, password=None):
    """Get password from terminal with discretion."""
    prompt = 'Enter SCM password for {0}:'.format(username)
    while not password:
        verify = False
        while password != verify:
            if verify:
                print('Passwords do not match. Try again', file=sys.stderr)
            password = getpass.getpass(prompt)
            verify = getpass.getpass('Retype password: ')
    return password


def get(url, auth):
    """Return the items request from the SC REST API."""
    try:
        response = requests.get(url, auth=auth)
    except requests.RequestException as e:
        print(e)
        sys.exit(1)
    else:
        if response.status_code == 200:
            return response.json()['items']
        else:
            print('=' * 79, file=sys.stderr)
            print('Access to SteelConnect Manager failed:', file=sys.stderr)
            print(response, response.reason, file=sys.stderr)
            print('=' * 79, file=sys.stderr)
            sys.exit(1)


def send(url, payload, auth, method):
    """Send to the SC REST API using either the put or post method."""
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
    }
    try:
        response = method(url, auth=auth, headers=headers, data=payload)
    except requests.RequestException as e:
        print(e)
        sys.exit(1)
    else:
        return response


def put(url, payload, auth):
    """Send to the SC REST API using the PUT method."""
    return send(url, payload, auth, requests.put)


def post(url, payload, auth):
    """Send to the SC REST API using the PUT method."""
    return send(url, payload, auth, requests.post)


if __name__ == '__main__':
    result = main(sys.argv[1:])
