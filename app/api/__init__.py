from flask_restx import Api
from flask import Blueprint

from .users import api as users_ns



api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, title='Admin Chatbot API', version='1.0', doc='/docs')

# On enregistre les endpoints avec le bon nom
api.add_namespace(users_ns, path='/users')

