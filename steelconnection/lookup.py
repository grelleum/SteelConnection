# coding: utf-8

"""SteelConnection

Convienience object for ID value lookups based on common criteria.

Should be instantiated within a steelconnection object.
"""


class LookUp(object):
    """Provide convienience tools to lookup objects."""

    def __init__(self, sconnect):
        """Obtain access to SteelConect Manager."""
        self.sconnect = sconnect
        self._model = model

    def iter_find(self, domain, search):
        """
        Generic search function.
        Given a resource type (domain)
        and a dictionary of {keyword: value} pairs to match,
        returns a gereator of dictionaries matching the search criteria.
        """
        for obj in self.sconnect.get(domain):
            if all(obj[key] == value for key, value in search.items()):
                yield obj

    def find(self, domain, search):
        """
        Generic search function.
        Given a resource type (domain), a value to match, and a key to lookup,
        returns a list of dictionaries matching the search criteria.
        """
        return list(self.iter_find(domain, search))

    def find_one(self, domain, search):
        """
        Generic lookup function.
        Given a resource type (domain), a value to match, and a key to lookup,
        returns a dictionary representing the object.
        """
        try:
            return next(self.iter_find(domain, search))
        except StopIteration:
            return None

    def node(self, pattern, key="serial"):
        """
        Returns a node matching a provided appliance serial number.
        """
        return self.find_one(domain="nodes", search={key: pattern.upper()})

    def org(self, pattern, key="name"):
        """
        Returns a org matching a provided organization short name.
        """
        return self.find_one(domain="orgs", search={key: pattern})

    def site(self, pattern, orgid=None, key="name"):
        """
        Returns a site matching a provided site short name and org_id.
        """
        if not orgid:
            raise ValueError("orgid required when looking up a site.")
        resource = "/".join(("org", orgid, "sites"))
        return self.find_one(domain=resource, search={key: pattern})

    def wan(self, pattern, orgid=None, key="name"):
        """
        Returns a wan matching a provided wan name and org_id.
        """
        if not orgid:
            raise ValueError("orgid required when looking up a wan.")
        resource = "/".join(("org", orgid, "wans"))
        return self.find_one(domain=resource, search={key: pattern})

    def model(self, value, default=None):
        """
        Translates a model code name to real name and visa versa.
        """
        default = default if default else value
        return self._model.get(value, default)


model = {
    "aardvark": "SDI-S12",
    "baloo": "SDI-SH",
    "beorn": "SDI-ZAKSH",
    "booboo": "SDI-AWS",
    "cx3070": "3070-SD",
    "cx570": "570-SD",
    "cx770": "770-SD",
    "ewok": "SDI-330",
    "fozzy": "SDI-USB",
    "grizzly": "SDI-1030",
    "koala": "SDI-AP5",
    "kodiak": "SDI-S48",
    "misha": "SDI-AZURE-SH",
    "paddington": "SDI-AZURE",
    "panda": "SDI-130",
    "panther": "SDI-5030",
    "raccoon": "SDI-AP3",
    "sloth": "SDI-S24",
    "tiger1g": "SDI-2030",
    "ursus": "SDI-AP5r",
    "xirrusap": "Xirrus AP",
    "yogi": "SDI-VGW",
}

model_reversed = sorted((v, k) for k, v in model.items())
model.update(dict(model_reversed))

