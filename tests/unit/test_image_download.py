# coding: utf-8

# import json
import os
# import sys
# import pytest
# import responses
import steelconnection


# class NameSpace():
#     def __init__(self):
#         pass


# db = {
#     'status': {
#         'fw_versions': {'yogi': '2.10.2.16-yogi'},
#         'scm_version': '1.23.4',
#         'scm_build': '56',
#     },
#     'orgs': {
#         'items': [
#             {
#                 'id': 'org-12345',
#                 'name': 'WineAndCheese',
#             }
#         ]
#     },
#     'sites': {
#         'items': [
#             {
#                 'id': 'site-12345',
#                 'org': 'org-12345',
#                 'city': 'Uptown, US',
#                 'name': 'UP',
#             },
#             {
#                 'id': 'site-56789',
#                 'org': 'org-56789',
#                 'city': 'Downtown, US',
#                 'name': 'DOWN',
#             },
#         ],
#     },
#     'nodes': {
#         'items': [
#              {
#                 'id': 'node-12345',
#                 'org': 'org-12345',
#                 'site': 'site-12345',
#                 'serial': 'XNABCD0123456789',
#                 'model': 'yogi'
#              }
#         ],
#     },
#     'image_status': {
#         'status': 'Success',
#         'image_file': 'node-12345-random.zip',
#         'image_type': 'kvm'
#     },
#     'image_download': b'abcdefghijklmnopqrstuvwxyz',
#     'invalid_status': {},
# }


# get_image = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/image',
#     headers={'Content-Type': 'application/octet-stream'},
#     body=b'B',
#     status=200,
# )

# get_node = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/node/node-12345',
#     json=db['nodes']['items'][0],
#     status=200,
# )

# get_nodes = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/nodes',
#     json=db['nodes'],
#     status=200,
# )

# get_nonesuch = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/nonesuch',
#     body=db['image_download'],
#     status=404,
# )

# get_orgs = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/orgs',
#     json=db['orgs'],
#     status=200,
# )

# get_queued = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/Queued',
#     body='{"error":{"message":"Queued","code":404}}',
#     status=404,
# )

# get_status = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/status',
#     json=db['status'],
#     status=200,
# )

# get_invalid_status = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/status',
#     json=db['invalid_status'],
#     status=200,
# )

# get_status_404 = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/status',
#     status=404,
# )

# get_stream = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/stream',
#     body=db['image_download'],
#     status=200,
# )

# get_image_status = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/node/node-12345/image_status',
#     json=db['image_status'],
#     status=200,
# )

# get_image_download = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/node/node-12345/get_image',
#     body=db['image_download'],
#     status=200,
# )

# getstatus_node = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.reporting/1.0/node/node-12345',
#     json=db['nodes']['items'][0],
#     status=200,
# )

# getstatus_nonesuch = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.reporting/1.0/nonesuch',
#     status=404,
# )

# delete_nonesuch = responses.Response(
#     method='DELETE',
#     url='https://some.realm/api/scm.config/1.0/nonesuch',
#     status=404,
# )

# delete_org = responses.Response(
#     method='DELETE',
#     url='https://some.realm/api/scm.config/1.0/org/org-12345',
#     json={},
#     status=200,
# )

# post_nodes = responses.Response(
#     method='POST',
#     url='https://some.realm/api/scm.config/1.0/nodes',
#     json=db['nodes']['items'][0],
#     status=200,
# )

# post_nonesuch = responses.Response(
#     method='POST',
#     url='https://some.realm/api/scm.config/1.0/nonesuch',
#     status=404,
# )

# post_prepare_image = responses.Response(
#     method='POST',
#     url='https://some.realm/api/scm.config/1.0/node/node-12345/prepare_image',
#     json={},
#     status=200,
# )

# put_node = responses.Response(
#     method='PUT',
#     url='https://some.realm/api/scm.config/1.0/node/node-12345',
#     json=db['nodes']['items'][0],
#     status=200,
# )

# put_nonesuch = responses.Response(
#     method='PUT',
#     url='https://some.realm/api/scm.config/1.0/nonesuch',
#     status=404,
# )


def test_get_file_path():
    """Test SConnect.image_download._get_file_path method."""
    filename = steelconnection.image_download._get_file_path('A', 'Z')
    assert filename == 'Z'


def test_get_file_path_source_only():
    """Test SConnect.image_download._get_file_path method."""
    filename = steelconnection.image_download._get_file_path('A', None)
    assert filename == 'A'


def test_get_file_path_with_dir():
    """Test SConnect.image_download._get_file_path method."""
    cwd = os.getcwd()
    src = 'xYz'
    filename = steelconnection.image_download._get_file_path(src, cwd)
    assert filename == os.path.join(cwd, src)
