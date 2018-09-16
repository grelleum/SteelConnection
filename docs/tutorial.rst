Tutorial
========

* **This is a work in progress, please check back soon for updates** *

In this tutorial, we are going to create a new site, configure static
IP address on the uplinks and deploy a virtual gateway to that site.

Finding the realm and org name
------------------------------

When you manage an organization in the SteelConnect Manager via a web browser,
the URL will look something like this:

https://<REALM_FQDN>/admin/<ORG_SHORT_NAME>

The <REALM_FQDN> and <ORG_SHORT_NAME> will be unique to your setup and you
will need these to follow the tutorial.


Create the SteelConnection object
---------------------------------

Let's start by creating a SteelConnection object.

- Use the ``steelconnection.SConnect`` constructor to create the object.
- We will assign this new object to the name ``sc``.
- We will provide the name of our realm, as well as the username and
  password we use to login.

.. code:: python

   import steelconnection
   sc = steelconnection.SConnect('myrealm.riverbed.cc', 'admin', 'LetM3in')


Find the ID for our Organization
--------------------------------

We need to know the Org ID for our Organization.  This is easy since we got
the Org short name from the SteelConnect URL.

The ``.lookup.org`` method will return a dictionary representing the org
object.  That dictionary will include a key called ``id`` that holds the
org id.

.. code:: python

   # Replace ORG_SHORT_NAME with your Org's short name.
   org_id = sc.lookup.org('ORG_SHORT_NAME')['id]


Create a new site
-----------------

Create a dictionary that represents the site we want to create.
At a minimum, we must specify the name, longname, city, and country.

| The country specified must be in the standardized two letter format.
  Here is one source for these codes:
| https://www.willmaster.com/blog/misc/country-name-abbreviation.php

| If this site will reside in a timezone that is different from the
  Organization timezone, then you will want to specify the timezone
  for this site.  Timezones must be provided in the same format as the
  'TZ' column in this list:
| https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List

Once we have our new site dictionary created, we can send a POST request
to the resource '/org/<ORG_ID>/sites'.

.. code:: python

   # Dictionary containing the details for the site to be created:
   new_site = {
       'name': 'NYC',
       'city': 'New York',
       'country': 'US',
       'longname': 'New York test lab.',
       'timezone': 'America/New_York',
   }

   # Created site
   resource = '/org/{}/sites'.format(org_id)
   site = sc.post(resource, data=new_site)

The post command will return the newly created site, which we have assigned
to the name 'site'.


Set uplink to static IP
-----------------------

Here we will set the uplink to use a static IP address.  When you create
a new site, it new uplink will be created for that site.  The site object
will include a list of uplinks for that site.  Since our site only has one
uplink, we can access the uplink ID using index zero.

.. code:: python

   # Get the uplink ID from the site object, index 0.
   uplink_id = site['uplinks'][0]

   # Get uplink object from SteelConnect Manager.
   uplink = sc.get('uplink/' + uplink_id)

Next, we will change the uplink type from 'dhcp' to 'static', and configure
an IP address and default gateway.  The change we are making is to the
local dictionary object, so we will need to upload the changes to the
SteelConnect Manager.

.. code:: python

   # Set uplink to static and define IP addresses.
   uplink['type'] = 'static'
   uplink['static_ip_v4'] = '172.30.12.249/29'
   uplink['static_gw_v4'] = '172.30.12.254'

   # Upload modified object to the SCM.
   result = sc.put('uplink/' + uplink_id, data=uplink)


Create virtual gateway
----------------------

Let's create a virtual gateway in the new site we have created.
The virtual gateway has the model name 'yogi' so we need to specify
that model, as well as the site ID.

.. code:: python

   # Create dictionary with minimum required information.
   new_node = { 'site': site['id'], 'model': 'yogi' }

   # POST request to SteelConnect Manager.
   node = sc.post('/org/' + org_id + '/node/virtual/register', data=new_node)


Assign Port to Zone
-------------------

At this point, the virtual gateway should have it's first network interface
assigned to the site uplink.  However, no interfaces will be assigned to
our LAN zones, so we will do that now, before we generate and download
the virtual gateway image.

When we created the new site earlier, a network and a zone were created and
associated with this site.  We want to configure the zone to the third
network interface on our gateway (we are reserving the second interface
for other purposes, like as a second uplink or HA control port).

The site has a 'networks' key that includes the networks at that site.
We need to retreive the network object in order to get the zone ID.
The zone will be assigned to the network interface.

.. code:: python

   # Get network ID from site.
   # Since there is only one network associated to this site,
   # we take the first one (index zero).
   net_id = site['networks'][0]

   # Retreive the network from SteelConnect Manager.
   network = sc.get('/network/' + net_id)

   # Get Zone ID from the network object.
   zone_id = network['zone']

   # Now we can assign this zone to the third network interface.
   # First, we get the port ID from the node.
   # Note that since indexes start at zero, the third port is at index '2'.
   port_id = node['ports'][2]

   # Retreive the port from SteelConnect Manager.
   port = sc.get('/port/' + port_id)

   # Set the 'segment' key to the zone ID.
   port['segment'] = zone_id

   # We can also disable tagging for this port.
   # It should already be disabled, since that it the default state.
   port['tagged'] = 0

   # Upload port to the SteelConnect Manager.
   result = sc.put('/port/' + port_id, data=port)


Download Vritaul Gateway image
------------------------------

SteelConnection provides a convenience method to generate and download
virtual gateway images.

.. code:: python

   # Here we specify the destination filename as 'vgw.zip1',
   # and the type of hypervisor as 'kvm'.

   sc.download_image(save_as='vgw.zip', build='kvm')


Fin
---

This completes the tutorial.  I hope this gets you on your way to
productive use of SteelConnection.
