# SteelConnection
REST API access to Riverbed SteelConnect Manager.

SteelConnection provides wrapper objects to simplify access to the Riverbed SteelConnect REST API.
The SteelConnection objects store the SCM base URL and authentication so that you only need to pass in the resource and any required data.
The object creates a Request session object, which is sent to the SteelConnect Manager and passes back a response object with an additional 'data' attribute containing any data from the SteelConnect Manager.

Supports Python 2.7, 3.4, 3.5, 3.6


## Requires:
Requests


## Note:
The password entered gets stored in the wrapper object in plain text.  So if you were to query the object attributes you could easily see the password.  This is done for the convienience of not requiring the password to be input or passed everytime an API call is made.


## Official Riverbed SteelConnect REST API Documentation:
**Configuration:**
https://support.riverbed.com/apis/scm_beta/scm-2.10.0/scm.config/index.html

**Reporting:**
https://support.riverbed.com/apis/scm_beta/scm-2.10.0/scm.reporting/index.html


## HOWTO:
#### This section is a work in progress.  Please be patient as I will expand this.
Import steelconnection and create a new object by providing the Fully qualified DNS name or your realm.  The would be your REALM_NAME.riverbed.cc, where REALM_NAME is the name of your realm.
```python
import steelconnection
sconnect = steelconnection.Config('MySteelConnect.riverbed.cc')
```
#### Authentication:
SteelConnect REST API uses username and password authentication.  If a SteelConnection object gets created without a specified username and password, the object will interactively prompt you for your username and password.  

```python
>>> import steelconnection
>>> sconnect = steelconnection.Config('MySteelConnect.riverbed.cc')
Enter username: admin
Enter password: 
Retype password: 
>>> 
```

If you prefer to use some other method to obtain the username and password, you can supply those as the time of object creation using the username and password keywaord argumets.
For example, if you want to store your credentials in your system environment variables you could do something similar to the following:
```python
import os
import steelconnection

username = os.environ.get('SCONUSER')
password = os.environ.get('SCONPASSWD')

sconnect = steelconnection.Config('MySteelConnect.riverbed.cc', username=username, password=password)
```

