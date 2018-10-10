# coding: utf-8

import os
import pytest
import responses
import steelconnection


db = {
    'status': {
        'fw_versions': {'yogi': '2.10.2.16-yogi'},
        'scm_version': '1.23.4',
        'scm_build': '56',
    },
    'orgs': {'items': [{'id': 'org-12345', 'name': 'WineAndCheese'}]},
    'sites': {
        'items': [
            {
                'id': 'site-12345',
                'org': 'org-12345',
                'city': 'Uptown, US',
                'name': 'UP',
            },
            {
                'id': 'site-56789',
                'org': 'org-56789',
                'city': 'Downtown, US',
                'name': 'DOWN',
            },
        ]
    },
    'nodes': {
        'items': [
            {
                'id': 'node-12345',
                'org': 'org-12345',
                'site': 'site-12345',
                'serial': 'XNABCD0123456789',
                'model': 'yogi',
            }
        ]
    },
    'image_status': {
        'status': 'Success',
        'image_file': 'node-12345-random.zip',
        'image_type': 'kvm',
    },
    'image_download': b'abcdefghijklmnopqrstuvwxyz',
    'invalid_status': {},
}

get_image_status = responses.Response(
    method='GET',
    url='https://some.realm/api/scm.config/1.0/node/node-12345/image_status',
    json=db['image_status'],
    status=200,
)

get_image_status_queued = responses.Response(
    method='GET',
    url='https://some.realm/api/scm.config/1.0/node/node-12345/image_status',
    # url='https://some.realm/api/scm.config/1.0/Queued',
    body='{"error":{"message":"Queued","code":404}}',
    status=404,
)

get_image_status_ResourceGone = responses.Response(
    method='GET',
    url='https://some.realm/api/scm.config/1.0/node/node-12345/image_status',
    json=db['invalid_status'],
    status=410,
)

get_image_download = responses.Response(
    method='GET',
    url='https://some.realm/api/scm.config/1.0/node/node-12345/get_image',
    body=db['image_download'],
    status=200,
)

post_prepare_image = responses.Response(
    method='POST',
    url='https://some.realm/api/scm.config/1.0/node/node-12345/prepare_image',
    json={},
    status=200,
)


# no_op


def test_no_op():
    """Verify no_op always returns None."""
    assert steelconnection.image_download._no_op() is None
    assert steelconnection.image_download._no_op(1, 2, 3) is None
    assert steelconnection.image_download._no_op(1, ['x', 'y'], 'A') is None
    assert steelconnection.image_download._no_op(hello='goodbye') is None


# _get_file_path


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


# _download_image


@responses.activate
def test_download_image_quiet(capsys):
    """Test SConnect.download_image method in quiet mode."""
    responses.add(get_image_status)
    responses.add(get_image_download)
    filename = 'delete.me'
    sc = steelconnection.SConnect('some.realm', connection_attempts=0)
    steelconnection.image_download._download_image(
        sc, 'node-12345', save_as=filename, quiet=True
    )
    with open(filename, 'rb') as f:
        contents = f.read()
    assert contents == db['image_download']
    captured = capsys.readouterr()
    assert captured.out == ''


@responses.activate
def test_build_and_download_image(capsys):
    """Test SConnect.download_image method."""
    responses.add(post_prepare_image)
    responses.add(get_image_status)
    responses.add(get_image_download)
    filename = 'delete.me'
    sc = steelconnection.SConnect('some.realm', connection_attempts=0)
    steelconnection.image_download._download_image(
        sc, 'node-12345', save_as=filename, build='kvm'
    )
    with open(filename, 'rb') as f:
        contents = f.read()
    assert contents == db['image_download']
    captured = capsys.readouterr()
    assert 'Requesting image of type kvm' in captured.out


@responses.activate
def test_download_image_not_available():
    """Test SConnect.download_image method."""
    responses.add(get_image_status_ResourceGone)
    sc = steelconnection.SConnect('some.realm', connection_attempts=0)
    with pytest.raises(ValueError):
        steelconnection.image_download._download_image(sc, 'node-12345')


# _wait_for_ready


@responses.activate
def test_wait_for_ready_timeout():
    """Test _wait_for_ready will timeout when image is never ready."""
    responses.add(get_image_status_queued)
    sc = steelconnection.SConnect('some.realm', connection_attempts=0)
    with pytest.raises(RuntimeError):
        steelconnection.image_download._wait_for_ready(
            sc,
            'node-12345',
            steelconnection.image_download._no_op,
            retries=1,
            sleep_time=0.1,
        )


@responses.activate
def test_wait_for_ready_resource_gone():
    """Test _wait_for_ready returns None when image not available."""
    responses.add(get_image_status_ResourceGone)
    sc = steelconnection.SConnect('some.realm', connection_attempts=0)
    result = steelconnection.image_download._wait_for_ready(
        sc, 'node-12345', steelconnection.image_download._no_op
    )
    assert result is None


# def print_flush(*args, **kwargs):

# def _prepare_image(sconnect, nodeid, build, verbose):

# def _stream_download(sconnect, nodeid, source_file, save_as, verbose):
