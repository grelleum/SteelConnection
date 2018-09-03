```
   ______          _______                       __  _
  / __/ /____ ___ / / ___/__  ___  ___  ___ ____/ /_(_)__  ___
 _\ \/ __/ -_) -_) / /__/ _ \/ _ \/ _ \/ -_) __/ __/ / _ \/ _ \
/___/\__/\__/\__/_/\___/\___/_//_/_//_/\__/\__/\__/_/\___/_//_/

```

# SteelConnection
##### version 0.91.1
SteelConnection provides a wrapper object to simplify access to the Riverbed SteelConnect REST API.

* Create an object once and it remembers the URL and authentication.
* All subsequent API requests are made via a single TCP connection.
* Call the appropriate method and supply the resource path and any upload data.
* Accepts and returns native Python data - no need to convert to or from JSON.

##### BETA software:
_actively working to simplify - some behavior may change before 1.0.0 release._

## Supports:
Python 2.7, 3.4, 3.5, 3.6, 3.7

## Requires:
Requests

## HOWTO:
#### To install or upgrade your copy to the latest version:
```bash
# Default Python
python -m pip install --upgrade steelconnection

# Python 3
python3 -m pip install --upgrade steelconnection

# Python 2
python2 -m pip install --upgrade steelconnection
```

#### Quickstart:
See the examples folder for sample scripts.\
https://github.com/grelleum/SteelConnection/tree/master/examples

#### Getting Started:
* Make sure the REST API is enabled on your SteelConnect realm before trying to access the REST API.
* Use pip to install steelconnection as shown above.
* Import steelconnection and create a new object.
```python
import steelconnection
sc = steelconnection.SConnect()
```

#### Realms and Organizations:
There is a one to one relationship between a Realm and a SteelConnect Manager.  The SteelConnect Manager acts as the controller for a the realm.  A newly created realm would not have any organizations, otherwise a realm will have one or more organizations.  Each oganization within a realm acts an autonomous network system. In practice, most REST API operations are performed within a specific organization.

You normally access the SteelConnect Manager (SCM) using a web browser.\
The URL you use includes the realm and organization that you are managing and takes the form:
`https://realm.riverbed.cc/admin/Organization`.\
The Organization is case-sensistive and is also known as the organization short name, as opposed to the longname, which is more descriptive and can include spaces, and other characters.

#### Authentication:
SteelConnect REST API uses Basic Auth, meaning a username and password are required for authentication for every request made.  The steelconnection object can store the username and pssword for you, or you can use a .netrc file as detailed below.  Choose one of the following methods:

##### Interactive login (Optional):
If you do not specify a realm, username, or password, and a .netrc file is not configured, steelconnection will interactively prompt you for your the missing information.  Steelconnection will validate the login by making a 'status' call against the REST API.
```python
>>> import steelconnection
>>> sc = steelconnection.SConnect()
Enter SteelConnect Manager fully qualified domain name: REALM.riverbed.cc
Enter username: admin
Enter password:
>>>
```
Three connection attempts are made by default and can be configured with the `connections_attempts=N` parameter, where N is replaced with an interger.

##### Using a .netrc file (Optional):
A .netrc file can be used to store credentials on Mac, Unix, and Linux machines.  .netrc is a standard way of storing login credentials for many network based servers.  It works like a hosts file, in that you specify servers and the credetials needed to access each server.  The .netrc file is stored in the root of your home directory.  When using a .netrc file, steelconnection will never have your password, rather the underlying requests library will be responsible for accessing the .netrc file.  When using .netrc file, you will still need to tell steelconnection the realm you want to access, and that hostname will be passed to requests without credentials.  Requests will then attempt to located your realm within the ,netrc file.\
Use the commands below to setup a .netrc file, replacing REALM, USERNAME, and PASSWORD with your actual values.
```bash
echo "machine REALM.riverbed.cc login USERNAME password PASSWORD" >> ~/.netrc
chmod 600 ~/.netrc
```

##### Specifying username and password (Optional):
If you prefer to use some other method to obtain the username and password, you can supply those as the time of object creation using the username and password keywaord argumets.\
For example, if you want to store your credentials in your system environment variables you could do something similar to the following:
```python
import os
import steelconnection

username = os.environ.get('SCONUSER')
password = os.environ.get('SCONPASSWD')

sc = steelconnection.SConnect('REALM.riverbed.cc', username=username, password=password)
```

#### Understanding the API:
The Riverbed SteelConnect REST API allows HTTPS access to the SteelConnect Manager (SCM) via the use of GET, POST, PUT, and DELETE commands.  SteelConneciton (this module) acts to simplify coding by providing an object that remembers your realm, version, and authentication and builds the HTTPS requests based on that information.  A `requests.session` object is used to allow a single TCP connection to be re-used for all subsequent API requests.

**With** SteelConnection, a request to get a list of all organizations in the realm would look like this:
```python
orgs = sc.get('orgs')
```
**Without** SteelConnection, the same request would look like this:
```python
response = requests.get(
    'https://REALM.riverbed.cc/api/scm.config/1.0/orgs',
    auth=(username, password)
)
orgs = response.json()['items']
```

##### Available Methods:
SteelConneciton provides the `.get`,  `.getstatus`, `.post`, `.put`, and `.delete` methods to simplify access to the API.\
These methods will build the request to include api version, auth, etc, so you onlu need to specify the resource you are interrested in.

* get: Used for retrieving information about a resource.  Expect data to be returned.
* getstatus: Used for retrieving current status about a resource.  Expect data to be returned.
* post: Create or deploy a new resource.  Requires additional data in the payload and returns the newly created object.
* put: Use to edit or update some existing resource.  Requires additional data in the payload.
* delete: Delete an existing resource.

##### A Tale of Two APIs:
Riverbed divides the REST API into two APIs:
* Config: used to make configurations changes and get information about SteelConnect resources.\
https://support.riverbed.com/apis/scm_beta/scm-2.10.0/scm.config/index.html
* Reporting: used to get current status information about a resource.\
https://support.riverbed.com/apis/scm_beta/scm-2.10.0/scm.reporting/index.html

By nature, the Reporting API only requires the HTTP GET method, where-as the more commonly used Confg API requires GET, POST, PUT and DELETE.  SteelConnections combines the two APIs by implementing `.get`,  `.post`, `.put`, and `.delete` methods to access to Config API and the `.getstatus` method to access the Reporting API.

For example: Calling `.get('/port/' + port)` would retireve configuration settings on a port, where-as `.getstatus('/port/' + port)` would retreive the actual link state, speed, duplex, etc. for that port.

##### Crafting your API calls:
The Riverbed documentation describes the various REST API calls that can be made.\
These take the form:  "_HTTP Method_" "_resource path_".

Take the network section for example:\
https://support.riverbed.com/apis/scm_beta/scm-2.10.0/scm.config/index.html#!/network:
* `GET` `/networks`  List networks.
* `GET` `/org/:orgid/networks`  Get network for an org.
* `POST` `/org/:orgid/networks`  Create network within an org.
* `DELETE` `/networks/:netid`  Delete network.
* `GET` `/networks/:netid`  Get network.
* `PUT` `/networks/:netid`  Update a network.

Within the resource path, you may see a name preceded by a colon `:`. These are considered variables and must be replaced with an actual value.  The `/networks/:netid` would require the `:netid` be replaced with the actual network ID for the network you are requesting.

SteelConnection methods mimic the HTTP Methods and accept the short form resource paths.\
To update a network, the documentation lists `PUT` `/networks/:netid`.  With the SteelConnection object, you would call the put method as `sc.put('/network/' +  net_id)`.  Note that the leading `/` in the resource is optional as the SteelConnection object will insert it if it is missing.

##### Model Schema (Data Payload):
Post (create) and Put (update) requests require additional data in the form of a payload.  This gets sent to the server in the form of JSON data, however the SteelConnection object will accept either JSON data or a native Python dictionary (`isinstance(data, dict)`).  The Riverbed documentation will specify the format of the data as a "Model Schema".  Not everything listed in the model schema is required.  Generally, you can determine the minimum required data by checking the equivalent function in SteelConnect Manager web GUI.

#### Retrieving Data:
The SteelConnection methods leverage the popular requests package.  Methods calls always return a native Python dictionary, or a list of dictionaries, depending on the API call.  The `requests.response` object will be stored as an attribute of the object (`sc.response`) so the latest response is always easily accessible.  By providing the full `requests.response` object you are free to check status and see all headers.

For example, the 'get orgs' request should always provide a list of orgs within the realm, so we can directly assign the result as a native Python list.\
`list_of_all_orgs = sc.get('orgs')`

Here are the rules to determine what gets returned by an API request:
* If response.json() is True and the 'items' key exists, then return a python list of response.json()['items'].
* If response.json() is True and the 'items' key _does not_ exist, then return a python dictionary.
* If response.json() is False, return an empty python dictionary.

##### Virtual Appliance Image Download:
There is a convenience method `.download_image` that can be used to download a virtual appliance image file.
This method will optionally request the 'build' of a virtual appliance image, when you set `build=` a vm type, such as `build=kvm` or `build=ova`.
Then it will check the availability of the image file every one second until the file is found.
Next it will download the file to the location specifed by the `save_as=` parameter.
`download_image` will print status messages while checking the status and downloading the file.  To disable status messages, include the `quiet=True` parameter.
Here are some examples:
```python
# Build kvm image and specify the downloads folder and filename.
`sc.download_image(node['id'], save_as='Downloads/scon_vgw.zip', build='kvm')

# Build a hyperv image and download to the current directory using the default file name.
`sc.download_image(node['id'], build='hyperv')

# Download an existing image to /images/ directory and suppress status updates.
`sc.download_image(node['id'], save_as='/images/scon_vgw.zip', quiet=True)
```

##### Other Binary Data:
In the event another API call returns binary data, You can access it directly through the object's '.response.content' attribute, or by calling the '.savefile(filename)' method, which will save the binary data to a file.

#### Errors and Exceptions:
The **_Zen of Python_** states:
> Errors should never pass silently.\
Unless explicitly silenced.

With this in mind, steelconnection assumes all REST API calls should complete without error.  Succeful requests will return with an HTTP 200-level response.  Any other response if considered a failed request and will cause steelconnection to raise either a `RuntimeError`, or a custom exceptions that inherits from `RuntimeError`.  Exception handling can be used to catch the exception:
```python
try:
    sc.put(f'node/{node_id}', data={'location': 'LAB'})
except RuntimeError as e:
    handle_exception(e)
```
More specific exceptions that might be generated (all inherit from `RuntimeError`):
* `steelconnection.exceptions.AuthenticationError`:  401 - Check your username and password.
* `steelconnection.exceptions.APINotEnabled`: 502 - Check if REST API is enabled on Realm settings.
* `steelconnection.exceptions.BadRequest`: 400 - Possibly tried creating a resource that already exists.
* `steelconnection.exceptions.InvalidResource`: 404 - Path or resource not found.

If you prefer to have your script exit with a simple error message and no traceback, which can be confusing to users who are not programmers, you can set `on_error='exit'` when you create your SConnect object.
```python
sc = SConnect('REALM.riverbed.cc', on_error='exit')
```

If you prefer to handle errors manually and do not want steelconnection to generate exceptions based on HTTP response code, you can set `on_error=None` when you create your SConnect object.  The steelconnection object will evaluate as `True` after a successful request and `False` otherwise.  This reflects the status of the obect attribute `SConnect.response.ok`.
```python
sc = SConnect('REALM.riverbed.cc', on_error=None)
```

#### Convenience functions:
##### Object-level Convenience functions:
In addition to the `download_image` method mentioned above in the "Virtual Appliance Image Download:" section, there are several other functions provided to simplify common tasks.

The SteelConnect Manager stores resources in a database with a uniquie identifier (id).  Many API calls require that you know the id number of the resource you are interested in, which you might not know off hand.  SteelConnection provides a collection of `lookup` functions to look up the resources based on known values.  These functions return the actual resouce.\
Currently these are the available lookup functions:
* `lookup.org(org_short_name)`
* `lookup.node(serial)`
* `lookup.site(site_name, org_id=org['id'])`
* `lookup.model(model)`

These functions are accessed directly from the object you created and are specific to the SteelConnect API.

###### Lookup Organization:
Many REST API calls require that you know the org id of your organization.  You can provide the organization short name to the function and it will return the org object, which includes the 'id' as a field.
```python
>>> org = sc.lookup.org('Spacely')
>>> org['id']
'org-Spacely-0a0b1cbadb33f34'
>>>
```
###### Lookup Node:
Similarly, the `lookup.node` method exists to provide the node object when you supply the commonly known appliance serial number.
```python
>>> node = sc.lookup.node('XN00012345ABCDEF')
>>> node['id']
'node-56f1968e222ab789'
>>>
```
###### Lookup Site:
The site id can be found in a similar way, but since the same site name could exist in multiple organizations, the org_id is a;so required.
```python
>>> site = sc.lookup.site('Skypad', orgid='org-Spacely-0a501e7f27b2c03e')
>>> site['id']
'site-Skypad-884b9071141e4bc0'
>>>
```
###### Lookup Model:
The `lookup.model()` method is simply a translation service to map model code names to standard model names.  It can also be used to make the opposite translations:
```python
>>> sc.lookup.model('panda')
'SDI-130'
>>> sc.lookup.model('SDI-1030')
'grizzly'
>>>
```

##### Module-level Convenience functions:
These functions are accessed directly from the imported module and can be used independently of the SteelConnect API.

###### Get Input:
`get_input(prompt)` function works with both Python 2 and Python 3 to get user input.

###### Get Username:
`get_username(prompt)` function works with both Python 2 and Python 3 to get username.

###### Get Password:
`get_password(prompt)` function works with both Python 2 and Python 3 to get user input.  Uses getpass to provide discretion.  Requires user to input password to be typed twice for verification.
