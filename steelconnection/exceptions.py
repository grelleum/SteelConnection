# -*- coding: utf-8 -*-

"""steelconnection.exceptions

Contains exceptions raised by steelconnection.
"""

class AuthenticationError(RuntimeError):
    """401 - Authentication Failed."""

class NotFoundError(RuntimeError):
    """404 - Path or resource not found."""

class APIUnavailableError(RuntimeError):
    """502 - REST API not enabled."""
