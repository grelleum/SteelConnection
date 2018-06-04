# SteelConnection
REST API access to Riverbed SteelConnect Manager.

SteelConnection provides wrapper objects to simplify access to the Riverbed SteelConnect REST API.
The SteelConnection objects store the SCM base URL and authentication so that you only need to pass in the resource and any required data.
The object creates a Request session object, which is sent to the SteelConnect Manager and passes back a response object with an additional 'data' attribute containing any data from the SteelConnect Manager.

Supports Python 2.7, 3.4, 3.5, 3.6


## Requires:
Requests


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

#### Realms and Organizations:
There is a one to one relationship between a Realm and a SteelConnect Manager.  The SteelConnect Manager acts as the controller for a specific realm, which includes the domain `riverbed.cc`.  A Realm should have one or more organizations, which act an autonomous network system.  Only a newly created realm would not have any organizations.

You normally access the SteelConnect Manager (SCM) using a web browser.  The URL you use will specify the realm and organization that you are managing.  You will want to know these in order touse the Rest API.

A URL takes the form of `https://realm.riverbed.cc/admin/organization`.
The organization in the path of the URL is case-sensistive and is also known as the organization short-name, as opposed to the long-nme, which is more descriptive and can include spaces, and other characters.

#### Authentication:
##### Special Note on password security:
The password entered gets stored in the wrapper object in plain text.  So if you were to query the object attributes you could easily see the password.  This is done for the convienience of not requiring the password to be input or passed everytime an API call is made.

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
The site id can be found in a similar way, but since the same site name, like HQ, could exist in multiple organizations, the org_id must also be supplied.
```python
>>> site_id = sconnect.lookup.siteid('Skypad', orgid='org-Spacely-0a501e7f27b2c03e')
>>> site_id
'site-Skypad-884b9071141e4bc0'
>>> 
```