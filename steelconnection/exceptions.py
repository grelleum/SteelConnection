# -*- coding: utf-8 -*-

"""steelconnection.exceptions

Contains exceptions raised by steelconnection.
"""

class AuthenticationError(RuntimeError):
    """Authentication Failed."""

class APIUnavailableError(RuntimeError):
    """REST API not enabled."""

class NotFoundError(RuntimeError):
    """Path or resource not found."""


