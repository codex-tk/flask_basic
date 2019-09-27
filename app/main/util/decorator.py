from functools import wraps
from flask import request

from app.main.service.auth_service import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')
        if not token:
            return data, status
        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')
        if not token:
            return data, status

        if not token.get('admin'):
            resp = {
                'status': 'fail',
                'message': 'Admin token required'
            }
            return resp, 401

        return f(*args, **kwargs)
    return decorated
