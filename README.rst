Welcome to SteelConnection!
===========================
Simplify access to the Riverbed SteelConnect REST API.

.. code::

      ______          _______                       __  _
     / __/ /____ ___ / / ___/__  ___  ___  ___ ____/ /_(_)__  ___
    _\ \/ __/ -_) -_) / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
   /___/\__/\__/\__/_/\___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/

   version 0.94.2
   pip install steelconnection

-  Always crafts a correct URL based on the resource provided.
-  Accepts and returns native Python data: no need to convert to/from JSON.
-  Provides convinience methods for object lookup and image download.
-  Reuses TCP connection for subsequent API requests.

^^^^^^^

| **Beta software:**
| *actively working to simplify; some behavior may change before 1.0.0 release*.


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
