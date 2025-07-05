from flask import session, redirect, url_for, request
from functools import wraps

def is_authenticated(required_role=None):
    if 'user_id' not in session:
        return False
    if required_role and session.get('permissions') != required_role:
        return False
    return True

def login_required(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not is_authenticated(role):
                return redirect(url_for('auth.login', next=request.url))
            return func(*args, **kwargs)
        return wrapper
    return decorator