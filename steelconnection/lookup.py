# coding: utf-8

"""SteelConnection

Convienience object for ID value lookups based on common criteria.

Should be instantiated within a steelconnection object.
"""


class _LookUp(object):
    """Provide convienience tools to lookup objects."""

    def __init__(self, sconnect):
        """Obtain access to SteelConect Manager."""
        self.sconnect = sconnect
        self._models = model

    def _lookup(self, domain, value, key, return_value='id'):
        """
        Generic lookup function.
        Given a resource type (domain), a value to match, and a key to lookup,
        returns a tuple consisting of an object ID and the actual object.
        """
        items = self.sconnect.get(domain)
        for item in items:
            key_value = item.get(key, '')
            if key_value and value in key_value:
                self.sconnect.result = item.get(return_value, '')
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

    def model(self, value, default=None):
        """
        Translates a model code name to real name and visa versa.
        """
        default = default if default else value
        return self._models.get(value, default)


model = {
    'aardvark': 'SDI-S12',
    'baloo': 'SDI-SH',
    'beorn': 'SDI-ZAKSH',
    'booboo': 'SDI-AWS',
    'cx3070': '3070-SD',
    'cx570': '570-SD',
    'cx770': '770-SD',
    'ewok': 'SDI-330',
    'fozzy': 'SDI-USB',
    'grizzly': 'SDI-1030',
    'koala': 'SDI-AP5',
    'kodiak': 'SDI-S48',
    'misha': 'SDI-AZURE-SH',
    'paddington': 'SDI-AZURE',
    'panda': 'SDI-130',
    'panther': 'SDI-5030',
    'raccoon': 'SDI-AP3',
    'sloth': 'SDI-S24',
    'tiger1g': 'SDI-2030',
    'ursus': 'SDI-AP5r',
    'xirrusap': 'Xirrus AP',
    'yogi': 'SDI-VGW'
}

model_reversed = sorted((v, k) for k, v in model.items())
model.update(dict(model_reversed))
