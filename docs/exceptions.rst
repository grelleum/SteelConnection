Errors and Exceptions
=====================

| The **Zen of Python** states:
|  *Errors should never pass silently.*
|  *Unless explicitly silenced.*

With this in mind, steelconnection assumes all REST API calls should
complete without error. Succeful requests will return with an HTTP
200-level response. Any other response if considered a failed request
and will cause steelconnection to raise either a ``RuntimeError``, or a
custom exceptions that inherits from ``RuntimeError``. Exception
handling can be used to catch the exception:

.. code:: python

   try:
       sc.put(f'node/{node_id}', data={'location': 'LAB'})
   except RuntimeError as e:
       your_code_to_handle_exception(e)

Specific Exceptions:
--------------------

+---------------------+------+-----------------------------------------------+
|                     | HTTP |                                               |
| Exception           | code | Reason                                        |
+=====================+======+===============================================+
| AuthenticationError | 401  | Incorrect username and password.              |
+---------------------+------+-----------------------------------------------+
| APINotEnabled       | 502  | Rest API is not enabled on Realm.             |
+---------------------+------+-----------------------------------------------+
| BadRequest          | 400  | Tried creating a resource that already exists.|
+---------------------+------+-----------------------------------------------+
| InvalidResource     | 404  | Path or resource not found.                   |
+---------------------+------+-----------------------------------------------+
| ResourceGone        | 402  | Resource no longer available.                 |
+---------------------+------+-----------------------------------------------+

Alternate Error Behavior
------------------------

If you prefer to have your script exit with a simple error message and
no traceback, which can be confusing to users who are not programmers,
you can set ``on_error='exit'`` when you create your SConnect object.

.. code:: python

   sc = SConnect('REALM.riverbed.cc', on_error='exit')

If you prefer to handle errors manually and do not want steelconnection
to generate exceptions based on HTTP response code, you can set
``on_error=None`` when you create your SConnect object. The
steelconnection object will evaluate as ``True`` after a successful
request and ``False`` otherwise. This reflects the status of the obect
attribute ``SConnect.response.ok``.

.. code:: python

   sc = SConnect('REALM.riverbed.cc', on_error=None)
