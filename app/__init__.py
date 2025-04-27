# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import flask_monitoringdashboard as dashboard
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Extensions globales
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()

# Configuration du login manager
login_manager.login_view = 'auth.login'
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."

def create_app(test_config=None):
    app = Flask(__name__, static_folder='../static')

    # Mode TEST ou PROD
    if test_config:
        app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret-key",
            "WTF_CSRF_ENABLED": False,
            "JWT_SECRET_KEY": "test-jwt-secret",
            "JWT_ACCESS_TOKEN_EXPIRES": 3600,
            "JWT_TOKEN_LOCATION": ["headers"]
        })
        app.config.update(test_config)  # Permet de surcharger si besoin
        print("🧪 Démarrage en mode TEST avec SQLite en mémoire")
    else:
        required_env_vars = ['DATABASE_URL', 'SECRET_KEY', 'JWT_SECRET_KEY']
        for var in required_env_vars:
            if var not in os.environ or not os.environ[var]:
                raise RuntimeError(f"La variable d'environnement {var} est manquante dans le fichier .env")

        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
        app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
        app.config['JWT_TOKEN_LOCATION'] = ['headers']

        print("🚀 Démarrage en mode PRODUCTION avec MySQL Docker")

    # Initialiser les extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Enregistrement des routes Flask
    from .routes import register_routes
    register_routes(app)

    # Enregistrement des API REST
    from app.api import api_bp
    app.register_blueprint(api_bp)

    # Monitoring Dashboard
    dashboard.bind(app)

    # User loader pour Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    print("✅ Application Flask créée avec succès")
    return app
