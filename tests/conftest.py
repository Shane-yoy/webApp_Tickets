import pytest
import sys
import os

# 🔥 Ajouter la racine du projet au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_model_loading(monkeypatch):
    class DummyModel:
        def predict(self, X):
            return [1 for _ in range(X.shape[0])]

    class DummyVectorizer:
        def transform(self, texts):
            return DummyMatrix(len(texts))

    class DummyMatrix:
        def __init__(self, n_samples):
            self.shape = (n_samples, 10)

    def dummy_load_model_and_vectorizer():
        return DummyModel(), DummyVectorizer()

    monkeypatch.setattr('app.ai_models.predict_model.load_model_and_vectorizer', dummy_load_model_and_vectorizer)

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

