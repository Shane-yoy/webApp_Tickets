from flask import Blueprint

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/tickets')
def list_tickets():
    return "Liste des tickets"