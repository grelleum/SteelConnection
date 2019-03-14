set_node_location.py
====================

.. code:: python

   #!/usr/bin/env python
   
   # coding: utf-8
   
   #    ______          _______                       __  _
   #   / __/ /____ ___ / / ___/__  ___  ___  ___ ____/ /_(_)__  ___
   #  _\ \/ __/ -_) -_) / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
   # /___/\__/\__/\__/_/\___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/
   #
   #
   # SteelConnection
   # Simplify access to the Riverbed SteelConnect REST API.
   #
   # https://pypi.org/project/steelconnection
   # https://github.com/grelleum/SteelConnection
   
   
   """Update SteelConnect nodes within a specified Org
   by copying the site name to the location field
   for those nodes where the location is unset.
   
   Works with both Python2 and Python3.
   
   USAGE:
       set_node_location.py REALM.riverbed.cc organization
       set_node_location.py REALM.riverbed.cc organization -u $USER -p $PASSWD
   """
   
   
   from __future__ import print_function
   import argparse
   import sys
   import steelconnection
   
   
   def main(argv):
       """Update nodes."""
       args = arguments(argv)
   
       realm, organization = args.realm, args.organization
       if organization.endswith(".cc") and not realm.endswith(".cc"):
           realm, organization = organization, realm
   
       sc = steelconnection.SConnect(realm, username=args.username, password=args.password)
   
       # Find the target organization.
       org = sc.lookup.org(organization)
       print("\nOrg:", organization, "\tID:", org["id"])
   
       # Get list of all sites in target organization.
       sites = sc.get("org/{}/sites".format(org["id"]))
       print(status("site", sites, "in '{}'".format(organization)))
   
       # Create a map of site id to site name.
       site_names = {site["id"]: site["name"] for site in sites}
   
       # Get list of all nodes in target organization.
       nodes = sc.get("org/{}/nodes".format(org["id"]))
       print(status("node", nodes, "in '{}'".format(organization)))
   
       # Reduce list of nodes to those assigned to a site.
       nodes = [node for node in nodes if node["site"]]
       print(status("node", nodes, "assigned to a site"))
   
       # Reduce list of nodes to those not already assigned a loction.
       nodes = [node for node in nodes if not node["location"]]
       print(status("node", nodes, "with no specified location"))
   
       # Update location for the remaining nodes.
       return update_nodes(nodes, sc, organization, org["id"], site_names)
   
   
   def update_nodes(nodes, sc, organization, org_id, site_names):
       """Loop through nodes and push location to SCM where applicable."""
       for node in nodes:
           print("=" * 75)
           print("Node:", node["id"], node["serial"], node["model"])
           print("org:", node["org"], organization)
           print("site:", node["site"])
           print("location:", node["location"])
   
           site_id = node["site"]
           site_name = site_names[site_id]
           print("\nSetting location to '{}'".format(site_name))
           node["location"] = site_name
           result = sc.put("node/" + node["id"], data=node)
           print("updated location:", result["location"])
           print("Response:", sc.response.status_code, sc.response.reason, "\n")
           print()
   
   
   def status(category, values, suffix=""):
       """Return status in human-readable format."""
       size = len(values)
       pluralization = "" if size == 1 else "s"
       return "* Found {} {}{} {}.".format(size, category, pluralization, suffix)
   
   
   def arguments(argv):
       """Get command line arguments."""
       description = (
           "Update SteelConnect nodes within a specified Org "
           "by copying the site name to the location field "
           "for those nodes where the location is unset."
       )
       parser = argparse.ArgumentParser(description=description)
       parser.add_argument("realm", type=str, help="Domain name of SteelConnect Manager")
       parser.add_argument("organization", type=str, help="Name of target organization")
       parser.add_argument(
           "-u", "--username", help="Username for SteelConnect Manager (optional)"
       )
       parser.add_argument(
           "-p", "--password", help="Password for SteelConnect Manager (optional)"
       )
       return parser.parse_args()
   
   
   if __name__ == "__main__":
       result = main(sys.argv[1:])
   
