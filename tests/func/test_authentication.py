# coding: utf-8


import getpass
import sys
import pytest
import subprocess
import steelconnection


def test_auth_attempt_netrc_fails(monkeypatch):
    """By not providing auth, netrc should be attempted and fail."""
    if sys.version_info.major < 3:
        monkeypatch.setattr('__builtin__.raw_input', lambda x: REALM_ADMIN)
    else:
        monkeypatch.setattr('builtins.input', lambda x: REALM_ADMIN)
    monkeypatch.setattr('getpass.getpass', lambda x: PASSWORD)
    sc = steelconnection.SConAPI(REALM_2_8)
    _ = sc.get('orgs')
    assert sc
