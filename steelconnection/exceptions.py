# -*- coding: utf-8 -*-

"""Provide custom exceptions."""


class BadRequest(RuntimeError):
    """400 - Bad Request."""


class AuthenticationError(RuntimeError):
    """401 - Authentication Failed."""


class InvalidResource(RuntimeError):
    """404 - Path or resource not found."""


class ResourceGone(RuntimeError):
    """410 - Gone. Resource no longer available."""


class APINotEnabled(RuntimeError):
    """502 - REST API not enabled."""
