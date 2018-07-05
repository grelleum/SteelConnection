# coding: utf-8


import getpass
import sys
import pytest
import subprocess
import steelconnection


from PRIVATE import REALM_ADMIN, ORG_ADMIN, PASSWORD
from PRIVATE import REALM_2_8, REALM_2_9, REALM_2_10, REALM_2_11


def test_create_object_2_8():
    sc = steelconnection.SConAPI(REALM_2_8, REALM_ADMIN, PASSWORD)
    assert isinstance(sc, steelconnection.SConAPI)


def test_create_object_2_9():
    sc = steelconnection.SConAPI(REALM_2_9, REALM_ADMIN, PASSWORD)
    assert isinstance(sc, steelconnection.SConAPI)


def test_create_object_2_10():
    sc = steelconnection.SConAPI(REALM_2_10, REALM_ADMIN, PASSWORD)
    assert isinstance(sc, steelconnection.SConAPI)


def test_create_object_2_11():
    sc = steelconnection.SConAPI(REALM_2_11, REALM_ADMIN, PASSWORD)
    assert isinstance(sc, steelconnection.SConAPI)
