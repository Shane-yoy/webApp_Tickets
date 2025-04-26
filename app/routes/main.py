from flask import Blueprint, redirect, url_for
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home_redirect():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard.admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard.user_dashboard'))
    return redirect(url_for('auth.login'))
