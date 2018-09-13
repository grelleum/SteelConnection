API Guide
=========

The Riverbed SteelConnect REST API allows HTTPS access to the
SteelConnect Manager (SCM) via the use of GET, POST, PUT, and DELETE
commands. SteelConneciton (this module) acts to simplify coding by
providing an object that remembers your realm, version, and
authentication and builds the HTTPS requests based on that information.
A ``requests.session`` object is used to allow a single TCP connection
to be re-used for all subsequent API requests.

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

Available Methods:
''''''''''''''''''

| SteelConneciton provides the ``.get``, ``.getstatus``, ``.post``,
  ``.put``, and ``.delete`` methods to simplify access to the API.
| These methods will build the request to include api version, auth,
  etc, so you onlu need to specify the resource you are interrested in.

-  get: Used for retrieving information about a resource. Expect data to
   be returned.
-  getstatus: Used for retrieving current status about a resource.
   Expect data to be returned.
-  post: Create or deploy a new resource. Requires additional data in
   the payload and returns the newly created object.
-  put: Use to edit or update some existing resource. Requires
   additional data in the payload.
-  delete: Delete an existing resource.

A Tale of Two APIs:
'''''''''''''''''''

| Riverbed divides the REST API into two APIs: \* Config: used to make
  configurations changes and get information about SteelConnect
  resources.
| https://support.riverbed.com/apis/scm_beta/scm-2.10.0/scm.config/index.html
  \* Reporting: used to get current status information about a resource.
| https://support.riverbed.com/apis/scm_beta/scm-2.10.0/scm.reporting/index.html

By nature, the Reporting API only requires the HTTP GET method, where-as
the more commonly used Confg API requires GET, POST, PUT and DELETE.
SteelConnections combines the two APIs by implementing ``.get``,
``.post``, ``.put``, and ``.delete`` methods to access to Config API and
the ``.getstatus`` method to access the Reporting API.

For example: Calling ``.get('/port/' + port)`` would retireve
configuration settings on a port, where-as
``.getstatus('/port/' + port)`` would retreive the actual link state,
speed, duplex, etc. for that port.

Crafting your API calls:
''''''''''''''''''''''''

| The Riverbed documentation describes the various REST API calls that
  can be made.
| These take the form: “*HTTP Method*” “*resource path*”.

| Take the network section for example:
| https://support.riverbed.com/apis/scm_beta/scm-2.10.0/scm.config/index.html#!/network:
  \* ``GET`` ``/networks`` List networks. \* ``GET``
  ``/org/:orgid/networks`` Get network for an org. \* ``POST``
  ``/org/:orgid/networks`` Create network within an org. \* ``DELETE``
  ``/networks/:netid`` Delete network. \* ``GET`` ``/networks/:netid``
  Get network. \* ``PUT`` ``/networks/:netid`` Update a network.

Within the resource path, you may see a name preceded by a colon ``:``.
These are considered variables and must be replaced with an actual
value. The ``/networks/:netid`` would require the ``:netid`` be replaced
with the actual network ID for the network you are requesting.

| SteelConnection methods mimic the HTTP Methods and accept the short
  form resource paths.
| To update a network, the documentation lists ``PUT``
  ``/networks/:netid``. With the SteelConnection object, you would call
  the put method as ``sc.put('/network/' +  net_id)``. Note that the
  leading ``/`` in the resource is optional as the SteelConnection
  object will insert it if it is missing.
