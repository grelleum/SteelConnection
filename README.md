# SteelConnection
REST API access to Riverbed SteelConnect Manager.

SteelConnection provides wrapper objects to simplify access to the Riverbed SteelConnect REST API.
The SteelConnection objects store the SCM base URL and authentication so that you only need to pass in the resource and any required data.
The object creates a Request object, which is sent to the SteelConnect Manager and passes back a response object with an additional 'data' attribute containing any data from the SteelConnect Manager.

Supports Python 2.7, 3.4, 3.5, 3.6

## Requires:
Requests

## Note:
The password entered gets stored in the wrapper object in plain text.  So if you were to query the object attributes you could easily see the password.  This is done for convienience not requiring the password to be input or passed everytime an API call is made.
