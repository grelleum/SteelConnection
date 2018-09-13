Authentication
==============

SteelConnect REST API uses Basic Auth, meaning a username and password
are required for authentication for every request made. The
steelconnection object can store the username and pssword for you, or
you can use a .netrc file as detailed below. Choose one of the following
methods:

Interactive login
'''''''''''''''''

If you do not specify a realm, username, or password, and a .netrc file
is not configured, steelconnection will interactively prompt you for
your the missing information. Steelconnection will validate the login by
making a ‘status’ call against the REST API.

.. code:: python

   >>> import steelconnection
   >>> sc = steelconnection.SConnect()
   Enter SteelConnect Manager fully qualified domain name: REALM.riverbed.cc
   Enter username: admin
   Enter password:
   >>>

Three connection attempts are made by default and can be configured with
the ``connections_attempts=N`` parameter, where N is replaced with an
interger.

Using a .netrc file
'''''''''''''''''''

| A .netrc file can be used to store credentials on Mac, Unix, and Linux
  machines. .netrc is a standard way of storing login credentials for
  many network based servers. It works like a hosts file, in that you
  specify servers and the credetials needed to access each server. The
  .netrc file is stored in the root of your home directory. When using a
  .netrc file, steelconnection will never have your password, rather the
  underlying requests library will be responsible for accessing the
  .netrc file. When using .netrc file, you will still need to tell
  steelconnection the realm you want to access, and that hostname will
  be passed to requests without credentials. Requests will then attempt
  to located your realm within the ,netrc file.
| Use the commands below to setup a .netrc file, replacing REALM,
  USERNAME, and PASSWORD with your actual values.

.. code:: bash

   echo "machine REALM.riverbed.cc login USERNAME password PASSWORD" >> ~/.netrc
   chmod 600 ~/.netrc

Specifying username and password
''''''''''''''''''''''''''''''''

| If you prefer to use some other method to obtain the username and
  password, you can supply those as the time of object creation using
  the username and password keywaord argumets.
| For example, if you want to store your credentials in your system
  environment variables you could do something similar to the following:

.. code:: python

   import os
   import steelconnection

   username = os.environ.get('SCONUSER')
   password = os.environ.get('SCONPASSWD')

   sc = steelconnection.SConnect('REALM.riverbed.cc', username=username, password=password)
