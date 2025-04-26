from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import Ticket, Message, TicketUser
from datetime import datetime

user_tickets_bp = Blueprint('user_tickets', __name__)

@user_tickets_bp.route('/user/tickets', methods=['GET', 'POST'])
@login_required
def user_tickets():
    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        content = request.form.get('content', '').strip()

        # 🛡️ Sécurité : vérifier que les champs ne sont pas vides
        if not subject or not content:
            flash("Le sujet et le message sont requis.", "danger")
            return redirect(url_for('user_tickets.user_tickets'))

        try:
            # Crée le ticket
            new_ticket = Ticket(subject=subject, created_by=current_user.id, created_at=datetime.utcnow())
            db.session.add(new_ticket)
            db.session.flush()

            # Lie l'utilisateur à ce ticket
            link = TicketUser(ticket_id=new_ticket.id, user_id=current_user.id, role='creator')
            db.session.add(link)

            # Premier message
            message = Message(ticket_id=new_ticket.id, user_id=current_user.id, content=content, created_at=datetime.utcnow())
            db.session.add(message)

            db.session.commit()

            flash("Ticket créé avec succès 🎉", "success")
            return redirect(url_for('user_tickets.user_tickets'))

        except Exception as e:
            db.session.rollback()
            flash(f"Une erreur est survenue lors de la création du ticket : {str(e)}", "danger")
            return redirect(url_for('user_tickets.user_tickets'))

    # Liste des tickets de l'utilisateur
    user_tickets = Ticket.query.filter_by(created_by=current_user.id).order_by(Ticket.created_at.desc()).all()

    # Afficher un message si aucun ticket n'est trouvé
    if not user_tickets:
        flash("Vous n'avez pas encore créé de tickets.", "info")

    return render_template('user_tickets.html', tickets=user_tickets)
