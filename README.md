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

#### Lookup convienience methods:
SteelConnection provides a collection of `lookup` methods to look up the id for various API objects.  
Currently these are the available lookup methods:
    `lookup.orgid(org_shor_name)`
    `lookup.nodeid(serial)` 
    `lookup.siteid(site_name, org_id=org_id)` 
    
For example, most REST API calls require that you know the org id of the Organization to which you are making changes.  You can provide the 'short name' of your org to the function and it will return the org id.
```python
>>> org_id = sconnect.lookup.orgid('Spacely')
>>> org_id
'org-Spacely-0a501e7f27b2c03e'
>>> 
```
Similarly, the `lookup.nodeid` method exists to privide the node id when you supply the appliance serial number.
```python
>>> node_id = sconnect.lookup.nodeid('XN00012345ABCDEF')
>>> node_id
'node-56f1968e229ca738'
>>> 
```
The site id can be found in a similar name, but since the same site name, like HQ, could exist in multiple organizations, the org_id must also be supplied.
```python
>>> site_id = sconnect.lookup.siteid('NYC', org_id=org_id)
>>> site_id
'site-NYC-884b9071141e4bc0'
>>> 
```