# coding: utf-8

import pytest
import steelconnection
import fake_requests


# Helper Functions:

def test_error_string():
    """Test _error_string generates a properly formatted string."""
    url = 'MYREALM'
    status_code = 600
    response = fake_requests.Fake_Response(url, status_code, {'no': 'data'})
    expected = "{0} - Failed\nURL: {1}\nData Sent: {2}".format(
        status_code, url, repr(response.text)
    )
    error = steelconnection.steelconnection._error_string(response)
    assert error == expected
