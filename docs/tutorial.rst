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
