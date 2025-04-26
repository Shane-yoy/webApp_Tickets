import pytest
import sys
import os

# 🔥 Ajouter la racine du projet au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User

@pytest.fixture
def app_instance():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Base en mémoire
        "SECRET_KEY": "test"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

@pytest.fixture
def admin_user(app_instance):
    """Créer un utilisateur admin pour les tests"""
    with app_instance.app_context():
        admin = User(name="AdminTest", email="admin@example.com", password="hashed", role="admin")
        db.session.add(admin)
        db.session.commit()
        admin_id = admin.id  # 🛠 copie l'id avant de sortir de la session
        return admin_id

