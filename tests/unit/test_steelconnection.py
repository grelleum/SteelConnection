# coding: utf-8

import json
import sys
import pytest
import responses
import steelconnection


class NameSpace:
    def __init__(self):
        pass


db = {
    "status": {
        "fw_versions": {"yogi": "2.10.2.16-yogi"},
        "scm_version": "1.23.4",
        "scm_build": "56",
    },
    "info": {"sw_version": "1.23.4", "sw_build": "56", "scm_id": "ABC"},
    "non_scm_info": {"sw_version": "1.23.4", "sw_build": "56"},
    "orgs": {"items": [{"id": "org-12345", "name": "WineAndCheese"}]},
    "sites": {
        "items": [
            {
                "id": "site-12345",
                "org": "org-12345",
                "city": "Uptown, US",
                "name": "UP",
            },
            {
                "id": "site-56789",
                "org": "org-56789",
                "city": "Downtown, US",
                "name": "DOWN",
            },
        ]
    },
    "nodes": {
        "items": [
            {
                "id": "node-12345",
                "org": "org-12345",
                "site": "site-12345",
                "serial": "XNABCD0123456789",
                "model": "yogi",
            }
        ]
    },
    "image_status": {
        "status": "Success",
        "image_file": "node-12345-random.zip",
        "image_type": "kvm",
    },
    "image_download": b"abcdefghijklmnopqrstuvwxyz",
    "invalid_status": {},
    "non_dict": b"[]",
}


get_image = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/image",
    headers={"Content-Type": "application/octet-stream"},
    body=b"B",
    status=200,
)

get_node = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/node/node-12345",
    json=db["nodes"]["items"][0],
    status=200,
)

get_nodes = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/nodes",
    json=db["nodes"],
    status=200,
)

get_nonesuch = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/nonesuch",
    body=db["image_download"],
    status=404,
)

get_nonesuch_non_dict = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/nonesuch",
    body=db["non_dict"],
    status=404,
)

get_orgs = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/orgs",
    json=db["orgs"],
    status=200,
)

get_queued = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/Queued",
    body='{"error":{"message":"Queued","code":404}}',
    status=404,
)

get_status = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/status",
    json=db["status"],
    status=200,
)

get_info = responses.Response(
    method="GET",
    url="https://some.realm/api/common/1.0/info",
    json=db["info"],
    status=200,
)

get_non_scm_info = responses.Response(
    method="GET",
    url="https://some.realm/api/common/1.0/info",
    json=db["non_scm_info"],
    status=200,
)

# get_invalid_status = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/status',
#     json=db['invalid_status'],
#     status=200,
# )

get_invalid_info = responses.Response(
    method="GET",
    url="https://some.realm/api/common/1.0/info",
    json=db["invalid_status"],
    status=200,
)

# get_status_404 = responses.Response(
#     method='GET',
#     url='https://some.realm/api/scm.config/1.0/status',
#     status=404,
# )

get_info_404 = responses.Response(
    method="GET", url="https://some.realm/api/common/1.0/info", status=404
)

get_stream = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/stream",
    body=db["image_download"],
    status=200,
)

get_image_status = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/node/node-12345/image_status",
    json=db["image_status"],
    status=200,
)

get_image_download = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.config/1.0/node/node-12345/get_image",
    body=db["image_download"],
    status=200,
)

getstatus_node = responses.Response(
    method="GET",
    url="https://some.realm/api/scm.reporting/1.0/node/node-12345",
    json=db["nodes"]["items"][0],
    status=200,
)

getstatus_nonesuch = responses.Response(
    method="GET", url="https://some.realm/api/scm.reporting/1.0/nonesuch", status=404
)

delete_nonesuch = responses.Response(
    method="DELETE", url="https://some.realm/api/scm.config/1.0/nonesuch", status=404
)

delete_org = responses.Response(
    method="DELETE",
    url="https://some.realm/api/scm.config/1.0/org/org-12345",
    json={},
    status=200,
)

post_nodes = responses.Response(
    method="POST",
    url="https://some.realm/api/scm.config/1.0/nodes",
    json=db["nodes"]["items"][0],
    status=200,
)

post_nonesuch = responses.Response(
    method="POST", url="https://some.realm/api/scm.config/1.0/nonesuch", status=404
)

post_prepare_image = responses.Response(
    method="POST",
    url="https://some.realm/api/scm.config/1.0/node/node-12345/prepare_image",
    json={},
    status=200,
)

put_node = responses.Response(
    method="PUT",
    url="https://some.realm/api/scm.config/1.0/node/node-12345",
    json=db["nodes"]["items"][0],
    status=200,
)

put_nonesuch = responses.Response(
    method="PUT", url="https://some.realm/api/scm.config/1.0/nonesuch", status=404
)


# Primary Methods:


@responses.activate
def test_scon_get():
    """Test SConnect.get method."""
    responses.add(get_orgs)
    responses.add(get_node)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.get("orgs") == db["orgs"]["items"]
    assert sc.response.ok
    assert "/api/scm.config/" in sc.response.url
    assert sc.get("/node/node-12345") == db["nodes"]["items"][0]
    assert sc.response.ok
    assert "/api/scm.config/" in sc.response.url


@responses.activate
def test_scon_getstatus():
    """Test SConnect.getstatus method."""
    responses.add(getstatus_node)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.getstatus("/node/node-12345") == db["nodes"]["items"][0]
    assert sc.response.ok
    assert "/api/scm.reporting/" in sc.response.url


@responses.activate
def test_scon_delete():
    """Test SConnect.delete method."""
    responses.add(delete_org)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.delete("org/org-12345") == {}
    assert sc.response.ok
    assert "/api/scm.config/" in sc.response.url


@responses.activate
def test_scon_post():
    """Test SConnect.post method."""
    responses.add(post_nodes)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    data = db["nodes"]["items"][0]
    assert sc.post("nodes", data=data) == data
    assert sc.response.ok
    assert "/api/scm.config/" in sc.response.url


@responses.activate
def test_scon_put():
    """Test SConnect.put method."""
    responses.add(put_node)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    data = db["nodes"]["items"][0]
    assert sc.put("node/node-12345", data=data) == data
    assert sc.response.ok
    assert "/api/scm.config/" in sc.response.url


# Primary Methods can generate exceptions:


@responses.activate
def test_scon_get_exception():
    """Test SConnect.get method."""
    responses.add(get_nonesuch)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    with pytest.raises(RuntimeError):
        sc.get("nonesuch")


@responses.activate
def test_scon_getstatus_exception():
    """Test SConnect.getstatus method."""
    responses.add(getstatus_nonesuch)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    with pytest.raises(RuntimeError):
        sc.getstatus("nonesuch")


@responses.activate
def test_scon_delete_exception():
    """Test SConnect.delete method."""
    responses.add(delete_nonesuch)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    with pytest.raises(RuntimeError):
        sc.delete("nonesuch")


@responses.activate
def test_scon_post_exception():
    """Test SConnect.post method."""
    responses.add(post_nonesuch)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    with pytest.raises(RuntimeError):
        sc.post("nonesuch", data={})


@responses.activate
def test_scon_put_exception():
    """Test SConnect.put method."""
    responses.add(put_nonesuch)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    with pytest.raises(RuntimeError):
        sc.put("nonesuch", data={})


# Properties:


def test_ascii_art():
    """Test SConnect.ascii_art returns a string."""
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.ascii_art


@responses.activate
def test_received_with_success():
    """Test SConnect.received when response.ok."""
    responses.add(get_status)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    sc.get("status")
    assert sc.received == "Status: 200 - OK\nError: None"


@responses.activate
def test_received_not_ok_and_no_json():
    """Test SConnect.received when response.text is not json formatted."""
    responses.add(get_nonesuch)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    with pytest.raises(RuntimeError):
        sc.get("nonesuch")
    assert sc.received == "Status: 404 - Not Found\nError: None"


@responses.activate
def test_received_not_ok_and_non_dict_json():
    """Test SConnect.received when response.text is not json dict."""
    responses.add(get_nonesuch_non_dict)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    with pytest.raises(RuntimeError):
        sc.get("nonesuch")
    assert sc.received == "Status: 404 - Not Found\nError: None"


def test_scon_realm_when_defined():
    """Test SConnect.realm property when pre-defined."""
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.realm == "some.realm"


# @responses.activate
# def test_scon_realm_when_not_defined(monkeypatch):
#     """Test SConnect.realm property when not provided."""
#     if sys.version_info.major < 3:
#         monkeypatch.setattr('__builtin__.raw_input', lambda x: 'some.realm')
#     else:
#         monkeypatch.setattr('builtins.input', lambda x: 'some.realm')
#     responses.add(get_orgs)
#     sc = steelconnection.SConnect(use_netrc=True)
#     # sc = steelconnection.SConnect(connection_attempts=0)
#     assert sc.realm == 'some.realm'


# @responses.activate
# def test_scon_realm_when_called_from_request_and_not_defined(monkeypatch):
#     """Test SConnect.realm property when not provided."""
#     responses.add(get_status)
#     if sys.version_info.major < 3:
#         monkeypatch.setattr('__builtin__.raw_input', lambda x: 'some.realm')
#     else:
#         monkeypatch.setattr('builtins.input', lambda x: 'some.realm')
#     sc = steelconnection.SConnect(connection_attempts=0)
#     sc.get('status')
#     assert sc.realm == 'some.realm'


# Helper methods:


def test_scon_make_url():
    """Test SConnect.url method."""
    sc = steelconnection.SConnect("NO.REALM", api_version="999", connection_attempts=0)
    url = sc.make_url("FAKE", "PATH")
    assert url == "https://NO.REALM/api/FAKE/999/PATH"


#


@responses.activate
def test_scm_version():
    """Test SConnect.scm_version method."""
    responses.add(get_info)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.scm_version == "1.23.4_56"


@responses.activate
def test_scm_version_invalid():
    """Test SConnect.scm_version method when an invalid status is returned."""
    responses.add(get_invalid_info)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.scm_version == "unavailable"


@responses.activate
def test_scm_version_other_riverbed_platform():
    """Test SConnect.scm_version method when run against another Riverbed product."""
    responses.add(get_non_scm_info)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.scm_version == 'Not a SteelConnect CX Manager'


@responses.activate
def test_scm_version_unavailable():
    """Test SConnect.scm_version method."""
    responses.add(get_info_404)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    assert sc.scm_version == "unavailable"


#


@responses.activate
def test_stream():
    """Test SConnect.stream method."""
    responses.add(get_stream)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    result = sc.stream("stream")
    assert list(result) == [db["image_download"]]


# Download image:


@responses.activate
def test_download_image():
    """Test SConnect.download_image method."""
    responses.add(get_image_status)
    responses.add(get_image_download)
    filename = "delete.me"
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    sc.download_image("node-12345", save_as=filename)
    with open(filename, "rb") as f:
        contents = f.read()
    assert contents == db["image_download"]


def test_savefile():
    """Test SConnect.savefile method."""
    filename = "delete.me"
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    sc.response = NameSpace()
    sc.response.content = b"ABCDEFG1234567890"
    sc.savefile(filename)
    with open(filename, "rb") as f:
        contents = f.read()
    assert contents == sc.response.content


# Get Results:


@responses.activate
def test_scon_get_result_not_ok():
    """Test SConnect.__get_result method."""
    responses.add(get_nonesuch)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    try:
        sc.get("nonesuch")
    except RuntimeError:
        pass
    assert sc._get_result(sc.response) is None


@responses.activate
def test_scon_get_result_not_ok_with_body():
    """Test SConnect.__get_result method."""
    responses.add(get_queued)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    sc.get("Queued")
    assert sc._get_result(sc.response) == json.loads(sc.response.text)


# @responses.activate
# def test_scon_get_result_octet_stream():
#     """Test SConnect._get_result method."""
#     responses.add(get_image)
#     sc = steelconnection.SConnect("some.realm", connection_attempts=0)
#     sc.get("image")
#     assert sc._get_result(sc.response) == {
#         "status": " ".join(
#             (
#                 "Binary data returned.",
#                 "Use '.savefile(filename)' method or access using '.response.content'.",
#             )
#         )
#     }


@responses.activate
def test_scon_get_result_no_json():
    """_get_results should return an empty dict when .json returns False."""
    responses.add(delete_org)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    sc.delete("org/org-12345")
    assert sc._get_result(sc.response) == {}


@responses.activate
def test_scon_get_result_no_items():
    """_get_results should return a dict when 'items' is not in response."""
    responses.add(get_node)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    sc.get("node/node-12345")
    assert isinstance(sc._get_result(sc.response), dict)
    assert sc._get_result(sc.response) == db["nodes"]["items"][0]


@responses.activate
def test_scon_get_result_with_items():
    """_get_results should return a list when 'items' is in response."""
    responses.add(get_nodes)
    sc = steelconnection.SConnect("some.realm", connection_attempts=0)
    sc.get("nodes")
    assert isinstance(sc._get_result(sc.response), list)
    assert sc._get_result(sc.response) == db["nodes"]["items"]
