# coding: utf-8

import requests
import steelconnection
import PATCH


def test_scon_get(monkeypatch):
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.get('orgs') == PATCH.responses['orgs']
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


def test_scon_getstatus(monkeypatch):
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.getstatus('orgs') == PATCH.responses['orgs']
    assert sc.response.ok
    assert '/api/scm.reporting/' in sc.response.url


def test_scon_delete(monkeypatch):
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    sc = steelconnection.SConAPI('some.realm')
    assert sc.delete('orgs') == PATCH.responses['orgs']
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


def test_scon_put(monkeypatch):
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    data = PATCH.responses['orgs']
    sc = steelconnection.SConAPI('some.realm')
    assert sc.put('orgs', data=data) == data
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url


def test_scon_post(monkeypatch):
    monkeypatch.setattr(requests, 'Session', PATCH.Fake_Session)
    data = PATCH.responses['orgs']
    sc = steelconnection.SConAPI('some.realm')
    assert sc.post('orgs', data=data) == data
    assert sc.response.ok
    assert '/api/scm.config/' in sc.response.url



#     def delete(self, resource, data=None, params=None):
#         r"""Send a DELETE request to the SteelConnect.Config API.

#         :param str resource: api resource to get.
#         :param dict data: (optional) Dictionary of 'body' data to be sent.
#         :param dict params: (optional) Dictionary of query parameters.
#         :returns: Dictionary or List of Dictionaries based on request.
#         :rtype: dict, or list
#         """
#         self.response = self.session.delete(
#             url=self.url('config', resource),
#             auth=(self.username, self.password) if self.username else None,
#             headers=self.headers,
#             params=params,
#             data=json.dumps(data) if data and isinstance(data, dict) else data
#         )
#         self.result = self._get_result(self.response)
#         if self.result is None:
#             self._raise_exception(self.response)
#         return self.result

#     def post(self, resource, data=None):
#         r"""Send a POST request to the SteelConnect.Config API.

#         :param str resource: api resource to get.
#         :param dict data: (optional) Dictionary of 'body' data to be sent.
#         :returns: Dictionary or List of Dictionaries based on request.
#         :rtype: dict, or list
#         """
#         self.response = self.session.post(
#             url=self.url('config', resource),
#             auth=(self.username, self.password) if self.username else None,
#             headers=self.headers,
#             data=json.dumps(data) if data and isinstance(data, dict) else data
#         )
#         self.result = self._get_result(self.response)
#         if self.result is None:
#             self._raise_exception(self.response)
#         return self.result

#     def put(self, resource, data=None, params=None):
#         r"""Send a PUT request to the SteelConnect.Config API.

#         :param str resource: api resource to get.
#         :param dict data: (optional) Dictionary of 'body' data to be sent.
#         :param dict params: (optional) Dictionary of query parameters.
#         :returns: Dictionary or List of Dictionaries based on request.
#         :rtype: dict, or list
#         """
#         self.response = self.session.put(
#             url=self.url('config', resource),
#             auth=(self.username, self.password) if self.username else None,
#             headers=self.headers,
#             params=params,
#             data=json.dumps(data) if data and isinstance(data, dict) else data
#         )
#         self.result = self._get_result(self.response)
#         if self.result is None:
#             self._raise_exception(self.response)
#         return self.result

#     def url(self, api, resource):
#         r"""Combine attributes and resource as a url string.

#         :param str api: api route, usually 'config' or 'reporting'.
#         :param str resource: resource path.
#         :returns: Complete URL path to access resource.
#         :rtype: str
#         """        
#         resource = resource[1:] if resource.startswith('/') else resource
#         return 'https://{0}/api/scm.{1}/{2}/{3}'.format(
#             self.controller, api, self.api_version, resource,
#         )

#     def savefile(self, filename):
#         r"""Save binary return data to a file.

#         :param str filename: Where to save the response.content.
#         """       
#         with open(filename, 'wb') as f:
#             f.write(self.response.content)

#     def _get_result(self, response):
#         r"""Return response data as native Python datatype.

#         :param requests.response response: Response from HTTP request.
#         :returns: Dictionary or List of Dictionaries based on response.
#         :rtype: dict, list, or None
#         """
#         if not response.ok:
#             if response.text and 'Queued' in response.text:
#                 # work-around for get:'/node/{node_id}/image_status'
#                 return response.json()
#             return None
#         if response.headers['Content-Type'] == 'application/octet-stream':
#             message = ' '.join(
#                 "Binary data returned."
#                 "Use '.savefile(filename)' method"
#                 "or access using '.response.content'."
#             )
#             return {'status': message}
#         if not response.json():
#             return {}
#         elif 'items' in response.json():
#             return response.json()['items']
#         else:
#             return response.json()

#     def _raise_exception(self, response):
#         r"""Return an appropriate exception if required.

#         :param requests.response response: Response from HTTP request.
#         :returns: Exception if non-200 response code else None.
#         :rtype: BaseException, or None
#         """
#         if not response.ok:
#             error = _error_string(response)
#             if response.status_code == 400:
#                 raise BadRequest(error)
#             elif response.status_code == 401:
#                 raise AuthenticationError(error)
#             elif response.status_code == 404:
#                 raise InvalidResource(error)
#             elif response.status_code == 502:
#                 raise APINotEnabled(error)
#             else:
#                 raise RuntimeError(error)

#     def _authenticate(self, username=None, password=None):
#         r"""Attempt authentication.

#         Makes GET request against 'orgs' (because 'status' was introduced 
#         in 2.9).  If neither username or password are provided,
#         will make the request without auth, to see if requests package
#         can authenticate using .netrc.

#         :param str username: (optional) Admin account name.
#         :param str password: (optional) Admin account password.
#         :returns: None.
#         :rtype: None
#         """
#         attempt_netrc_auth = username is None and password is None
#         if attempt_netrc_auth:
#             try:
#                 self.get('orgs')
#             except AuthenticationError:
#                 pass
#             else:
#                 return
#         self.username, self.password = self._get_auth(username, password)
#         self.get('orgs')

#     def _get_auth(self, username=None, password=None):
#         """Prompt for username and password if not provided.

#         :param str username: (optional) Admin account name.
#         :param str password: (optional) Admin account password.
#         :returns: Tuple of strings as (username, password).
#         :rtype: (str, str)
#         """
#         username = get_username() if username is None else username
#         password = get_password_once() if password is None else password 
#         return username, password

#     def _get_scm_version(self):
#         """Get version and build number of SteelConnect Manager.

#         :returns: SteelConnect Manager version and build number.
#         :rtype: str
#         """
#         try:
#             status = self.get('status')
#         except InvalidResource:
#             return 'unavailable'
#         else:
#             scm_version = status.get('scm_version'), status.get('scm_build')
#             return '.'.join(s for s in scm_version if s)

#     def __bool__(self):
#         """Return the success of the last request.

#         :returns: True of False if last request succeeded.
#         :rtype: bool
#         """
#         return False if self.response is None else self.response.ok 

#     def __repr__(self):
#         """Return a string consisting of class name, controller, and api.

#         :returns: Information about this object.
#         :rtype: str
#         """
#         details = ', '.join([
#             "controller: '{0}'".format(self.controller),
#             "scm version: '{0}'".format(self.scm_version),
#             "api version: '{0}'".format(self.api_version),
#             "package version: '{0}'".format(self.__version__),
#         ])
#         return '{0}({1})'.format(self.__class__.__name__, details)


# def test_error_string():
#     sc = steelconnection.SConAPI(REALM_2_10, REALM_ADMIN, PASSWORD)
#     items = sc.get('orgs')
#     items = (item for item in items if 'name' in item)
#     item = next(items)
#     key = item['name']
#     key_id = item['id']
#     result = sc.lookup._lookup(domain='orgs', value=key, key='name')
#     assert result == (key_id, item)
# def _error_string(response):
#     r"""Summarize error conditions and return as a string.

#     :param requests.response response: Response from HTTP request.
#     :returns: A multiline string summarizing the error.
#     :rtype: str
#     """
#     details = ''
#     if response.text:
#         try:
#             details = response.json()
#             details = details.get('error', {}).get('message', '')
#         except ValueError:
#             pass
#     error = '{0} - {1}{2}\nURL: {3}\nData Sent: {4}'.format(
#         response.status_code,
#         response.reason,
#         '\nDetails: ' + details if details else '',
#         response.url,
#         repr(response.request.body),
#     )
#     return error


# class SConAPIwithoutExceptions(SConAPI):
#     r"""Make REST API calls to Riverbed SteelConnect Manager.

#     This version of the class does not raise exceptions
#     when an HTTP response has a non-200 series status code.
    
#     :param str controller: hostname or IP address of SteelConnect Manager.
#     :param str username: (optional) Admin account name.
#     :param str password: (optional) Admin account password.
#     :param str api_version: (optional) REST API version.
#     :returns: Dictionary or List of Dictionaries based on request.
#     :rtype: dict, or list
#     """    

#     def _raise_exception(self, response):
#         r"""Return None to short-circuit the exception process.

#         :param requests.response response: Response from HTTP request.
#         :returns: None.
#         :rtype: None
#         """
#         return None
