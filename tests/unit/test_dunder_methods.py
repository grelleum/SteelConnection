# coding: utf-8

import responses
import steelconnection


class NameSpace():
    def __init__(self, ok):
        self.ok = ok


# Dunder Methods:

def test_scon_returns_true():
    """Test object returns True when reponse is OK."""
    sc = steelconnection.SConAPI('some.realm')
    sc.response = NameSpace(ok=True)
    assert bool(sc)


def test_scon_returns_false():
    """Test object returns False when reponse is not OK."""
    sc = steelconnection.SConAPI('some.realm')
    sc.response = NameSpace(ok=False)
    assert not bool(sc)


def test_scon_bool_returns_true():
    """Test __bool__ returns True when reponse is OK."""
    sc = steelconnection.SConAPI('some.realm')
    sc.response = NameSpace(ok=True)
    assert sc.__bool__()


def test_scon_bool_returns_false():
    """Test __bool__ returns False when reponse is not OK."""
    sc = steelconnection.SConAPI('some.realm')
    sc.response = NameSpace(ok=False)
    assert not sc.__bool__()


def test_scon_nonzero_returns_true():
    """Test __bool__ returns True when reponse is OK."""
    sc = steelconnection.SConAPI('some.realm')
    sc.response = NameSpace(ok=True)
    assert sc.__nonzero__()


def test_scon_nonzero_returns_false():
    """Test __bool__ returns False when reponse is not OK."""
    sc = steelconnection.SConAPI('some.realm')
    sc.response = NameSpace(ok=False)
    assert not sc.__nonzero__()


@responses.activate
def test_scon_repr():
    """Test __repr__ returns a proper string."""
    responses.add(
        responses.GET,
        'https://some.realm/api/scm.config/1.0/status',
        json={'scm_version': '1.23.4', 'scm_build': '56'},
        status=200,
    )
    realm = 'some.realm'
    scm_version = '1.23.4.56'
    api_version = '1.0'
    pkg_version = steelconnection.__version__
    expected = (
        "SConAPI(controller: '{0}', scm version: '{1}', "
        "api version: '{2}', package version: '{3}')"
    ).format(realm, scm_version, api_version, pkg_version)
    sc = steelconnection.SConAPI(realm, api_version=api_version)
    assert repr(sc) == expected


@responses.activate
def test_scon_str():
    """Test __str__ returns expected string."""
    responses.add(
        responses.GET,
        'https://some.realm/api/scm.config/1.0/status',
        json={'scm_version': '1.23.4', 'scm_build': '56'},
        status=200,
    )
    realm = 'some.realm'
    scm_version = '1.23.4.56'
    api_version = '1.0'
    pkg_version = steelconnection.__version__
    expected = '\n'.join((
        'SteelConnection:',
        ">> controller: '{}'",
        ">> scm version: '{}'",
        ">> api version: '{}'",
        ">> package version: '{}'",
        '>> GET: https://some.realm/api/scm.config/1.0/status',
        '>> Data Sent: None',
        '>> Status: 200 - OK',
        '>> Error: None'
    ))
    expected = expected.format(realm, scm_version, api_version, pkg_version)
    sc = steelconnection.SConAPI(realm, api_version=api_version)
    assert str(sc) == expected
