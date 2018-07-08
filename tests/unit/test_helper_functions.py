# coding: utf-8

import json
import pytest
import steelconnection
import fake_requests


# Helper Functions:

def test_error_string():
    """Test _error_string generates a properly formatted string."""
    url = 'MYREALM'
    status_code = 600
    data = {'no': 'data'}
    response = fake_requests.Fake_Response(url, status_code, data)
    expected = "{0} - Failed\nURL: {1}\nData Sent: {2}".format(
        status_code, url, repr(json.dumps(data, indent=4))
    )
    error = steelconnection.steelconnection._error_string(response)
    assert error == expected


# def test_error_string_bad_input():
#     """Test _error_string generates a ValueError Exception."""
#     with pytest.raises(ValueError):
#         response = fake_requests.Fake_Response(
#             'old.sch.ool/status',
#             600,
#             '<!DOCTYPE html>\n\n\n<html>\n'
#         )
#     with pytest.raises(UnboundLocalError):
#         error = steelconnection.steelconnection._error_string(response)
