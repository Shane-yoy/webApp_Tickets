# tests/test_user_chat.py

from app import db
from app.models import User, Ticket, Message

def test_homepage(client):
    response = client.get('/')
    assert response.status_code in [200, 302]  # 302 = redirection si non connecté

def test_send_message(client, app):
    with app.app_context():
        user = User(name="TestUser", email="test@example.com", password="hashed")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

        ticket = Ticket(subject="Test Ticket", created_by=user_id)
        db.session.add(ticket)
        db.session.commit()
        ticket_id = ticket.id

    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_id)

    res = client.post(f"/send_message/{ticket_id}", json={"content": "Hello world!"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "message" in data

def test_get_messages(client, app):
    with app.app_context():
        user = User(name="TestUser2", email="test2@example.com", password="hashed")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

        ticket = Ticket(subject="Another Ticket", created_by=user_id)
        db.session.add(ticket)
        db.session.commit()
        ticket_id = ticket.id

        message = Message(ticket_id=ticket_id, user_id=user_id, content="First message!")
        db.session.add(message)
        db.session.commit()

    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_id)

    res = client.get(f"/api/messages/{ticket_id}")
    assert res.status_code == 200
    messages = res.get_json()
    assert isinstance(messages, list)
    assert messages[0]['content'] == "First message!"
