create_site.py
==============

.. code:: python

   # coding: utf-8
   
   #         ______          __
   #        / __/ /____ ___ / /
   #    ____\ \/ __/ -_) -_) /      __  _
   #   / _____/\__/\__/\__/_/_ ____/ /_(_)__  ___
   #  / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
   #  \___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/
   #
   # SteelConnection
   # Simplify access to the Riverbed SteelConnect CX REST API.
   #
   # https://pypi.org/project/steelconnection
   # https://github.com/grelleum/SteelConnection
   
   
   from __future__ import print_function
   from pprint import pprint
   
   import steelconnection
   
   # Change the below values to match the realm and org
   # as seen in the URL for your SteelConnect CX Manager.
   # for example:  https://realm.riverbed.cc/admin/TestLab
   scm_name = "realm.riverbed.cc"
   org_name = "TestLab"
   
   # Details for the site to be created:
   new_site = {
       "name": "NYC",
       "city": "New York",
       "country": "US",
       "longname": "New York test lab.",
       "timezone": "America/New_York",
   }
   
   
   def main():
       # Initialize the steelconnection object.
       sc = steelconnection.SConnect(scm_name)
   
       # Get the org ID for your organization.
       org = sc.lookup.org(org_name)
       print("Org name: {},  Org id: {}".format(org["longname"], org["id"]))
   
       # API resource for posting.
       resource = "/org/{}/sites".format(org["id"])
   
       # Make the post request.
       result = sc.post(resource, data=new_site)
   
       # Display response.
       print("Response:", sc.response.status_code, sc.response.reason)
       pprint(result)
   
   
   if __name__ == "__main__":
       main()
   
