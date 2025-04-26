from flask import Blueprint, render_template, request
from app.decorators import role_required
from app.models import Ticket, Enterprise

admin_tickets_bp = Blueprint('admin_tickets', __name__)

@admin_tickets_bp.route('/admin/tickets')
@role_required('admin')
def list_tickets():
    status_filter = request.args.get('status', 'open')
    enterprise_id = request.args.get('enterprise_id', type=int)

    query = Ticket.query.filter_by(status=status_filter)

    if enterprise_id:
        query = query.join(Ticket.participants).filter_by(user_id=Ticket.created_by).filter(
            Ticket.creator.has(enterprise_id=enterprise_id)
        )

    tickets = query.all()
    enterprises = Enterprise.query.all()

    return render_template(
        'admin_tickets.html',
        tickets=tickets,
        enterprises=enterprises,
        selected_status=status_filter,
        selected_enterprise_id=enterprise_id
    )
