import json
import logging
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


# Standard error messages for authentication
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Decorator method for the API to initiate authentication process
def requires_auth(permission=''):
    pass
