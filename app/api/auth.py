# app/api/auth.py

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app.models import User
from app import db

auth_api = Namespace('auth', description='Authentification & rôles')

login_model = auth_api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

user_model = auth_api.model('User', {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'role': fields.String
})

@auth_api.route('/login')
class Login(Resource):
    @auth_api.expect(login_model)
    def post(self):
        """Authentifie un utilisateur et retourne un JWT Token"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
            return {"access_token": access_token}, 200

        return {"message": "Identifiants invalides"}, 401

@auth_api.route('/me')
class Me(Resource):
    @jwt_required()
    @auth_api.marshal_with(user_model)
    def get(self):
        """Retourne les infos de l'utilisateur courant"""
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return user
