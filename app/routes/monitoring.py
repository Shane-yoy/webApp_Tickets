from flask import Blueprint

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/monitoring')
def list_monitoring():
    return "Monitoring"