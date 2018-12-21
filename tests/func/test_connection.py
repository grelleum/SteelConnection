# coding: utf-8

import os
import sys
import steelconnection


REALM_ADMIN = os.environ.get("SCONUSER")
PASSWORD = os.environ.get("SCONPASSWD")
ORG_NAME = os.environ.get("SCONORG")
ORG_ADMIN = os.environ.get("SCONORGADMIN")
APPLIANCE = os.environ.get("SCONAPPLIANCE")
REALM = os.environ.get("SCONREALM")
ALT_REALM = os.environ.get("SCONALTREALM")


def test_create_object():
    sc = steelconnection.SConnect(REALM, REALM_ADMIN, PASSWORD)
    orgs = sc.get("orgs")
    assert orgs
    assert isinstance(orgs, list)
    assert isinstance(sc, steelconnection.SConnect)
    assert orgs[0]["id"]


def test_auth_attempt_netrc_fails(monkeypatch):
    """By not providing auth, netrc should be attempted and fail."""
    if sys.version_info.major < 3:
        monkeypatch.setattr("__builtin__.raw_input", lambda x: REALM_ADMIN)
    else:
        monkeypatch.setattr("builtins.input", lambda x: REALM_ADMIN)
    monkeypatch.setattr("getpass.getpass", lambda x: PASSWORD)
    sc = steelconnection.SConnect(ALT_REALM)
    sc.get("orgs")
    assert sc
