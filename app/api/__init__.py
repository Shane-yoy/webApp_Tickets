from flask_restx import Api
from flask import Blueprint

from .auth import auth_api as auth_ns
from .users import api as users_ns
from .predict import api as predict_ns
from .retrain import api as retrain_ns



api_bp = Blueprint('api', __name__, url_prefix='/api')

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Ajoutez votre token JWT ici : **Bearer &lt;token&gt;**"
    }
}

api = Api(
    api_bp,
    title='Admin Chatbot API',
    version='1.0',
    doc='/docs',
    authorizations=authorizations,
    security='Bearer Auth'
)

# Ici c'était une erreur ➔ pas de @ ici
api.authorizations['Bearer Auth'].update({
    'description': 'Tapez seulement votre token JWT. Le préfixe Bearer sera ajouté automatiquement.'
})

# On enregistre les endpoints avec le bon nom
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(users_ns, path='/users')
api.add_namespace(predict_ns, path='/predict')
api.add_namespace(retrain_ns, path='/retrain')

