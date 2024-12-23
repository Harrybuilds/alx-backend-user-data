#!/usr/bin/env python3
""" Module of authentication class
"""
from flask import request
from api.v1.views import app_views
from typing import TypeVar


class Auth():
    """
    Authentication class definition
    """
    def __init__(self):
        pass

    def require_auth(self, path: str, excluded_paths: list[str]) -> bool:
        """
        that returns False - path and excluded_paths will be used later, now, you don’t need to take care of them
        """
        if path is None:
            return True

        if path.endswith('/'):
            pass
        else:
            path = path + '/'

        if path not in excluded_paths:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """
        that returns None - request will be the Flask request object
        """
        if request is None:
            return None

        if "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization")


    def current_user(self, request=None) -> TypeVar('User'):
        """
        that returns None - request will be the Flask request object
        """
        return None
