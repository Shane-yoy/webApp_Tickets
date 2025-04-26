import flask_monitoringdashboard as dashboard
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask
import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Configuration du login manager
login_manager.login_view = 'auth.login'  # Redirige ici si non connecté
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."

def create_app():
    app = Flask(__name__, static_folder='../static')

    # Vérification des variables d'environnement essentielles
    required_env_vars = ['DATABASE_URL', 'SECRET_KEY']
    for var in required_env_vars:
        if var not in os.environ or not os.environ[var]:
            raise RuntimeError(f"La variable d'environnement {var} est manquante dans le fichier .env")

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

    print("Utilisation de la base de données MySQL pour Docker")

    # Initialiser les extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Enregistrement des routes Flask classiques
    from .routes import register_routes
    register_routes(app)

    # Enregistrement des routes API REST
    from app.api import api_bp
    app.register_blueprint(api_bp)

    # Activer le dashboard de monitoring
    dashboard.bind(app)

    # Fonction de rappel pour recharger un utilisateur
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    print("Application Flask créée avec succès.")
    return app
