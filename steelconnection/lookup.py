# coding: utf-8

"""SteelConnection

Convienience object for ID value lookups based on common criteria.

Should be instantiated within a steelconnection object.
"""

import sys
import warnings


class _LookUp(object):
    """Provide convienience tools to lookup objects."""

    def __init__(self, sconnection):
        """Obtain access to SteelConect Manager."""
        self.sconnection = sconnection

    def _lookup(self, domain, value, key, return_value='id'):
        """
        Generic lookup function.
        Given a resource type (domain), a value to match, and a key to lookup,
        returns a tuple consisting of an object ID and the actual object.
        """
        items = self.sconnection.get(domain)
        for item in items:
            key_value = item.get(key, '')
            if key_value and value in key_value:
                self.sconnection.result = item.get(return_value, '')
                return item
        return None

    def node(self, serial, key='serial'):
        """
        Returns a tuple of node_id and node
        matching a provided appliance serial number.
        """
        return self._lookup(domain='nodes', value=serial, key=key)

    def org(self, name, key='name'):
        """
        Returns a tuple of org_id and org
        matching a provided organization short name.
        """
        return self._lookup(domain='orgs', value=name, key=key)

    def site(self, name, orgid=None, key='name'):
        """
        Returns a tuple of site_id and site
        matching a provided site short name and org_id.
        """
        if not orgid:
            raise ValueError('orgid required when looking up a site.')
        resource = '/'.join(('org', orgid, 'sites'))
        return self._lookup(domain=resource, value=name, key=key)
