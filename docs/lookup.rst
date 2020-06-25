
Lookup
======

Lookup methods provide simplified ways of finding objects.

The SteelConnect CX Manager stores resources in a database with a uniquie
identifier (id). Many API calls require that you know the id number of
the resource you are interested in, which you might not know off hand.
SteelConnection provides a collection of ``lookup`` functions to look
up the resources based on known values. These functions return the
actual resouce.

These are the available lookup functions:

.. code:: python

   <object>.lookup.org(org_short_name)
   <object>.lookup.node(serial)
   <object>.lookup.site(site_name, org['id'])
   <object>.lookup.wan(wan_name, org['id'])
   <object>.lookup.model(model)

These functions are accessed directly from the object you created and
are specific to the SteelConnect CX API.


Lookup Organization
-------------------

Many REST API calls require that you know the org id of your
organization. You can provide the organization short name to the
function and it will return the org object, which includes the ‘id’ as a
field.

.. code:: python

   >>> org = sc.lookup.org('Spacely')
   >>> org['id']
   'org-Spacely-0a0b1cbadb33f34'
   >>>


Lookup Node
-----------

Similarly, the ``lookup.node`` method exists to provide the node object
when you supply the commonly known appliance serial number.

.. code:: python

   >>> node = sc.lookup.node('XN00012345ABCDEF')
   >>> node['id']
   'node-56f1968e222ab789'
   >>>


Lookup Site
-----------

The site id can be found in a similar way, but since the same site name
could exist in multiple organizations, the org_id is also required.

.. code:: python

   >>> site = sc.lookup.site('Skypad', orgid='org-Spacely-0a501e7f27b2c03e')
   >>> site['id']
   'site-Skypad-884b9071141e4bc0'
   >>>


Lookup WAN
----------

The site id can be found in a similar way, but since the same site name
could exist in multiple organizations, the org_id is also required.

.. code:: python

   >>> wan = sc.lookup.site('MPLS', orgid='org-Spacely-0a501e7f27b2c03e')
   >>> wan['id']
   'wan-MPLS-f26c9eb4f80a868b'
   >>>


Lookup Model
------------

The ``lookup.model()`` method is simply a translation service to map
model code names to standard model names. It can also be used to make
the opposite translations:

.. code:: python

   >>> sc.lookup.model('panda')
   'SDI-130'
   >>> sc.lookup.model('SDI-1030')
   'grizzly'
   >>>
