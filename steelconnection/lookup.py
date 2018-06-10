# coding: utf-8

"""SteelConnection

Convienience object for ID value lookups based on common criteria.

Should be instantiated within a steelconnection object.
"""


class _LookUp(object):
    """Provide convienience tools to lookup objects."""

    def __init__(self, sconnection):
        """Obtain access to SteelConect Manager."""
        self.sconnection = sconnection

    def _lookup(self, domain, value, key, return_value='id'):
        """Generic lookup function."""
        items = self.sconnection.get(domain).data
        valid_items = (item for item in items if item[key])
        # NEED better handling when item not found.
        matches = [item for item in valid_items if value in item[key]]
        details = max(matches) if matches else ''
        result = details[return_value]
        return result, details

    def nodeid(self, serial, key='serial'):
        """Return node id that matches appliance serial number provided."""
        result, _details = self._lookup(domain='nodes', value=serial, key=key)
        return result

    def orgid(self, name, key='name'):
        """Return org id that matches organization short name provided."""
        result, _details = self._lookup(domain='orgs', value=name, key=key)
        # self.sconnection.org.details = details
        return result

    def siteid(self, name, orgid=None, key='name'):
        """Return site id that matches site short name
        based on the organization provided.
        """
        if not orgid:
            raise ValueError('orgid required when looking up a site.')
        resource = '/'.join(('org', orgid, 'sites'))
        result, _details = self._lookup(domain=resource, value=name, key=key)
        return result
