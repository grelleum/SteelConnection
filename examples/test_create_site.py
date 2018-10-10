# coding: utf-8

"""
test_create_site.py

Pytest functions intended to validate examples/create_site.py.
This relies on a environment variables to complete.
"""

import os
import sys
import steelconnection


username = os.environ.get('SCONUSER')
password = os.environ.get('SCONPASSWD')
realm = os.environ.get('SCONREALM')
org_name = os.environ.get('SCONORG')
appliance = os.environ.get('SCONAPPLIANCE')


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
    sc = steelconnection.SConnect(realm, username, password)
    org = sc.lookup.org(org_name)
    site = sc.lookup.site(create_site.new_site['name'], org['id'])
    if site:
        sc.delete('site/' + site['id'])
    create_site.main()
    site = sc.lookup.site(create_site.new_site['name'], org['id'])
    assert site['id']
    for key in create_site.new_site:
        assert site[key] == create_site.new_site[key]
    sc.delete('site/' + site['id'])
    site = sc.lookup.site(create_site.new_site['name'], org['id'])
    assert site is None
