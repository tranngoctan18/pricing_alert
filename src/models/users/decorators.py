from functools import wraps
from src.app import app
from flask import session, url_for, request
from werkzeug.utils import redirect


def requires_login(endpoint):
    @wraps(endpoint)
    def decorated_endpoint(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return endpoint(*args, **kwargs)

    return decorated_endpoint


def require_admin_permisson(endpoint):
    @wraps(endpoint)
    def decorated_endpoint(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app.config['ADMIN']:
            return redirect(url_for('users.login_user'))
        return endpoint(*args, **kwargs)

    return decorated_endpoint
