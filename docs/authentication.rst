Authentication
==============

SteelConnect REST API version 1.0 uses 'Basic Auth', which requires
a username and password are required for every request made.
The steelconnection object can store the username and pssword for you,
or you can use a .netrc file as detailed below.

Authentication credentials can be prompted for interactively if not
supplied, or they can be supplied at the time of object creation
to prevent the interactive method.  Scripts that need to run unattended
should supply credentials at the time of object creation.


Unattended Mode
---------------

Specifying authentication credentials
'''''''''''''''''''''''''''''''''''''

.. code:: python

   import steelconnection

   sc = steelconnection.SConnect('REALM.riverbed.cc', 'username', 'password')


Using environment variables
'''''''''''''''''''''''''''

It is best practice not to hard-code authentication credentials in your
scripts.  One option is to use operating system environment variables.

Here is an example of using environment variables to store authentication.

.. code:: python

   import os
   import steelconnection

   username = os.environ.get('SCONUSER')
   password = os.environ.get('SCONPASSWD')

   sc = steelconnection.SConnect('REALM.riverbed.cc', username, password)


Using a .netrc file
'''''''''''''''''''

A .netrc file can be used to store credentials on Mac, Unix, and Linux
machines. .netrc is a standard way of storing login credentials for
many network based servers. It works like a hosts file.  Each line in
.netrc specifies a hostname, along with the username and password used
to access that server. The .netrc file is stored in the root of your
home directory.

When using a .netrc file, steelconnection will not have your password,
rather the underlying requests library will be responsible for accessing
the .netrc file.

Since .netrc access performs a lookup on the 'machine' field, you will
still need to specify the realm you want to access, and that hostname
will be passed to requests without credentials. Requests will perform
the lookup in the .netrc file.

On Mac or Linux, you can the commands below to setup a .netrc file,
replacing REALM, USERNAME, and PASSWORD with your actual values.

.. code:: bash

   echo "machine REALM.riverbed.cc login USERNAME password PASSWORD" >> ~/.netrc
   chmod 600 ~/.netrc

To prevent SteelConnection from prompting for authentication credentials,
you must explicitly tell SteelConnection to use the .netrc file.

.. code:: python

   sc = steelconnection.SConnect('REALM.riverbed.cc', use_netrc=True)


Interactive login
-----------------

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


Connection attempts
'''''''''''''''''''

Three connection attempts are allowed by default. After the third attempt
an AuthenticationError exception will be raised.  You can change the number
of allowed login attempts by adding the ``connections_attempts=N`` parameter,
when creating the steelconnection object.  Replace ``N`` with an interger.
Setting ``connections_attempts=0`` will prevent the interactive login
from running.  This is useful in testing and may have other applications.
