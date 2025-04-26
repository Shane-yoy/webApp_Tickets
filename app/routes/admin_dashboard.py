from flask import Blueprint, render_template,redirect, url_for
from app import db
from app.models import User, Ticket, Prediction
from sqlalchemy.sql import func
from app.decorators import role_required 

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)


@admin_dashboard_bp.route('/admin')
@role_required('admin') 
def admin_dashboard():
    # Données statistiques
    user_count = User.query.filter_by(is_active=True).count()
    ticket_count = Ticket.query.filter_by(status='open').count()
    avg_prediction = db.session.query(func.avg(Prediction.confidence)).scalar() or 0.0

    return render_template(
        "admin_dashboard.html",
        user_count=user_count,
        ticket_count=ticket_count,
        avg_prediction=round(avg_prediction, 2)
    )
