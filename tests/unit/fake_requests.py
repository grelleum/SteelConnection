# coding: utf-8

import json
from steelconnection import InvalidResource, AuthenticationError

codes = {
    'netrc401': 401,
    'nonesuch': 404,
}

org = {'id': 'not_an_org_id', 'name': 'steelconnection'}
status = {'scm_version': '2.9.1', 'scm_build': '50'}
node = {
    'org': 'not_an_org_id',
    'site': 'site-mysite',
    'id': 'node-somenode',
    'serial': 'XNABCD0123456789',
    'model': 'yogi',
}
site = {
    'org': 'not_an_org_id',
    'city': 'Anytown, US',
    'id': 'site-mysite',
    'name': 'Anytown',
}

netrc = node
netrc401 = node

responses = {
    'org': org,
    'orgs': {'items': [org]},
    'status': status,
    'node': node,
    'nodes': {'items': [node]},
    'site': site,
    'sites': {'items': [site]},
    'netrc': node,
    'netrc401': node,
}


def get_text(data):
    if isinstance(data, dict) or isinstance(data, list):
        try:
            return json.dumps(data)
        except ValueError:
            pass
    return data


class Fake_Request(object):

    def __init__(self, url, data):
        self.method = 'FAKE'
        self.url = url
        self.body = get_text(data)


class Fake_Response(object):

    def __init__(self, url, status_code, data, auth=None, content='json'):
        self.url = url
        self.ok = True if status_code < 300 else False
        self.reason = 'successs' if status_code < 300 else 'Failed'
        self.status_code = status_code
        self.headers = {'Content-Type': 'application/' + content}
        self.text = get_text(data)
        self.request = Fake_Request(url, data)
        self.auth = auth

    def json(self):
        return json.loads(self.text)


class Fake_Session(object):

    def __init__(self):
        self.proxies = {}
        self.headers = {
            'User-Agent': 'python-requests/2.19.1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

    def get(
            self, url, auth=None, headers=None,
            params=None, data=None, timeout=None,
    ):
        if data is not None:
            raise ValueError('get data must be None.')
        if url == 'https://old.school/api/scm.config/1.0/status':
            return Fake_Response(url, 404, data, auth)
        if url.startswith('https://timeout'):
            raise IOError('timed out :(')
        if url.startswith('https://InvalidResource'):
            raise InvalidResource('InvalidResource :(')
        if url.startswith('https://AuthenticationError'):
            raise AuthenticationError('AuthenticationError :(')
        resource = url.split('/')[-1]
        data = responses.get(resource, {})
        if resource == 'netrc401' and auth:
                resource = 'netrc'
        status_code = codes.get(resource, 200)
        return Fake_Response(url, status_code, data, auth)

    def getstatus(
            self, url, auth=None, headers=None,
            params=None, data=None, timeout=None,
    ):
        if data is not None:
            raise ValueError('getstatus data must be None.')
        resource = url.split('/')[-1]
        data = responses.get(resource, {})
        status_code = codes.get(resource, 200)
        return Fake_Response(url, status_code, data, auth)

    def delete(
            self, url, auth=None, headers=None,
            params=None, data=None, timeout=None,
    ):
        resource = url.split('/')[-1]
        data = responses.get(resource, {}) if not data else data
        status_code = codes.get(resource, 200)
        return Fake_Response(url, status_code, data, auth)

    def post(
            self, url, auth=None, headers=None,
            params=None, data=None, timeout=None,
    ):
        if params is not None:
            raise ValueError('post params must be None.')
        if data is None:
            raise ValueError('post have must data')
        resource = url.split('/')[-1]
        status_code = codes.get(resource, 200)
        return Fake_Response(url, status_code, data, auth)

    def put(
            self, url, auth=None, headers=None,
            params=None, data=None, timeout=None,
    ):
        if data is None:
            raise ValueError('put method must have data')
        resource = url.split('/')[-1]
        status_code = codes.get(resource, 200)
        return Fake_Response(url, status_code, data, auth)
