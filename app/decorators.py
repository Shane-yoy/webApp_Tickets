from functools import wraps
from flask import abort
from flask_login import login_required, current_user

def role_required(role):
    """
    Décorateur pour restreindre l'accès à certains rôles.
    Utilisation : @role_required('admin')
    """
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role != role:
                return abort(403)  # Interdit
            return f(*args, **kwargs)
        return decorated_function
    return decorator
