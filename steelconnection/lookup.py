# coding: utf-8

"""SteelConnection

Convienience object for ID value lookups based on common criteria.

Should be instantiated within a steelconnection object.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys


class _LookUp(object):
    """Provide convienience tools to lookup objects."""

    def __init__(self, sconnection):
        """Obtain access to SteelConect Manager."""
        self.sconnection = sconnection
        self._deprecated = 'lookup.{0}id deprecated: use lookup.{0} instead'

    def _lookup(self, domain, value, key, return_value='id'):
        """Generic lookup function."""
        items = self.sconnection.get(domain)
        for item in items:
            item_value = item.get(key, '')
            if item_value and value in item_value:
                self.sconnection.result = item.get(return_value, '')
                return self.sconnection.result, item

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

    # Methods below are deprecated.

    def nodeid(self, serial, key='serial'):
        """deprecated:
        Return node id that matches appliance serial number provided.
        """
        print(self._deprecated.format('node'), file=sys.stderr)
        result, _details = self._lookup(domain='nodes', value=serial, key=key)
        return result

    def orgid(self, name, key='name'):
        """deprecated:
        Return org id that matches organization short name provided.
        """
        print(self._deprecated.format('org'), file=sys.stderr)
        result, _details = self._lookup(domain='orgs', value=name, key=key)
        # self.sconnection.org.details = details
        return result

    def siteid(self, name, orgid=None, key='name'):
        """deprecated:
        Return site id that matches site short name
        based on the organization provided.
        """
        print(self._deprecated.format('site'), file=sys.stderr)
        if not orgid:
            raise ValueError('orgid required when looking up a site.')
        resource = '/'.join(('org', orgid, 'sites'))
        result, _details = self._lookup(domain=resource, value=name, key=key)
        return result
