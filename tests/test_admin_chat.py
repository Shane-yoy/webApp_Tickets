# tests/test_admin_chat.py

from app import db
from app.models import User, Ticket, Message

def test_admin_get_messages(client, app, admin_user):
    """Test de récupération des messages par un admin"""
    with app.app_context():
        admin = User.query.get(admin_user)
        ticket = Ticket(subject="Admin Ticket", created_by=admin.id)
        db.session.add(ticket)
        db.session.commit()
        ticket_id = ticket.id

        message = Message(ticket_id=ticket_id, user_id=admin.id, content="Admin's first message")
        db.session.add(message)
        db.session.commit()

    with client.session_transaction() as sess:
        sess['_user_id'] = str(admin_user)

    response = client.get(f"/api/admin/messages/{ticket_id}")
    assert response.status_code == 200
    messages = response.get_json()
    assert isinstance(messages, list)
    assert messages[0]["content"] == "Admin's first message"

def test_admin_send_message(client, app, admin_user):
    """Test de l'envoi d'un message par l'admin"""
    with app.app_context():
        admin = User.query.get(admin_user)
        ticket = Ticket(subject="New Admin Ticket", created_by=admin.id)
        db.session.add(ticket)
        db.session.commit()
        ticket_id = ticket.id

    with client.session_transaction() as sess:
        sess['_user_id'] = str(admin_user)

    response = client.post(f"/send_message_admin/{ticket_id}", json={"content": "Hello depuis l'admin"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"]["content"] == "Hello depuis l'admin"
