Welcome to SteelConnection!
===========================
Simplify access to the Riverbed SteelConnect REST API.

.. code::

          ______          __
         / __/ /____ ___ / /
     ____\ \/ __/ -_) -_) /      __  _
    / _____/\__/\__/\__/_/_ ____/ /_(_)__  ___
   / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
   \___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/

   version 1.1.2
   pip install steelconnection

-  Always crafts a correct URL based on the resource provided.
-  Accepts and returns native Python data: no need to convert to/from JSON.
-  Provides convinience methods for object lookup and image download.
-  Reuses TCP connection for subsequent API requests.

^^^^^^^

| **Supports:**
| Python 2.7, 3.4, 3.5, 3.6, 3.7

^^^^^^^

**With** SteelConnection, a request to get a list of all organizations
in the realm would look like this:

.. code:: python

   orgs = sc.get('orgs')

**Without** SteelConnection, the same request would look like this:

.. code:: python

   response = requests.get(
       'https://REALM.riverbed.cc/api/scm.config/1.0/orgs',
       auth=(username, password)
   )
   orgs = response.json()['items']

^^^^^^^

Documentation
-------------

| Full Documentation is available on *Read the Docs*.
| https://steelconnection.readthedocs.io/
