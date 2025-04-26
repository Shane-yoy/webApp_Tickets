from flask import Blueprint, render_template
from flask_login import login_required, current_user

user_dashboard_bp = Blueprint('user_dashboard', __name__)

@user_dashboard_bp.route('/user/dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html', user=current_user)
