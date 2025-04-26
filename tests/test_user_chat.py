import pytest
from flask import url_for
from app import create_app, db
from app.models import User, Ticket, Message

@pytest.fixture
def app_instance():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key",
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

def test_homepage(client):
    response = client.get('/')
    assert response.status_code in [200, 302]  # 302 if redirect to login

def test_send_message(client, app_instance):
    with app_instance.app_context():
        user = User(name="TestUser", email="test@example.com", password="hashed")
        db.session.add(user)
        db.session.commit()
        user_id = user.id  # ⚡ Capture l'ID maintenant

        ticket = Ticket(subject="Test Ticket", created_by=user_id)
        db.session.add(ticket)
        db.session.commit()
        ticket_id = ticket.id  # ⚡ Capture aussi l'ID du ticket

    with client.session_transaction() as sess:
        sess['_user_id'] = str(user_id)  # ⚡ Utilise user_id capturé

    res = client.post(f"/send_message/{ticket_id}", json={"content": "Hello world!"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "message" in data


def test_get_messages(client, app_instance):
    with app_instance.app_context():
        user = User(name="TestUser2", email="test2@example.com", password="hashed")
        db.session.add(user)
        db.session.commit()
        user_id = user.id  # ⚡ Capture ID

        ticket = Ticket(subject="Another Ticket", created_by=user_id)
        db.session.add(ticket)
        db.session.commit()
        ticket_id = ticket.id  # ⚡ Capture ID

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

