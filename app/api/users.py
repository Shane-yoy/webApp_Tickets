# app/api/users.py

from flask_restx import Namespace, Resource, fields
from flask import request
from app.models import User, db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

api = Namespace('users', description='Gestion des utilisateurs')

# Modèle Swagger pour validation / documentation
user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    'role': fields.String(enum=['user', 'admin'], default='user'),
    'is_active': fields.Boolean(default=True)
})

@api.route('/')
class UserList(Resource):
    @api.doc('liste_des_utilisateurs')
    @api.marshal_list_with(user_model)
    @jwt_required()
    def get(self):
        """Liste tous les utilisateurs"""
        claims = get_jwt()
        if claims['role'] != 'admin':
            api.abort(403, "Accès réservé aux administrateurs.")
        return User.query.all()

    @api.doc('créer_un_utilisateur')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    @jwt_required()
    def post(self):
        """Créer un nouvel utilisateur"""
        data = request.json
        claims = get_jwt()
        if claims['role'] != 'admin':
            api.abort(403, "Accès réservé aux administrateurs.")
        
        hashed_password = generate_password_hash(data.get("password", "1234"))  # valeur par défaut si manquante
        user = User(
            name=data['name'],
            email=data['email'],
            role=data.get('role', 'user'),
            is_active=data.get('is_active', True),
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        return user, 201

@api.route('/<int:id>')
@api.param('id', 'ID de l\'utilisateur')
class UserDetail(Resource):
    @api.marshal_with(user_model)
    @jwt_required()
    def get(self, id):
        """Récupère un utilisateur par ID"""
        return User.query.get_or_404(id)

    @api.expect(user_model)
    @api.marshal_with(user_model)
    @jwt_required()
    def put(self, id):
        """Met à jour un utilisateur"""
        user = User.query.get_or_404(id)
        data = request.json
        user.name = data['name']
        user.email = data['email']
        user.role = data.get('role', user.role)
        user.is_active = data.get('is_active', user.is_active)
        db.session.commit()
        return user

    @jwt_required()
    def delete(self, id):
        """Supprime un utilisateur"""
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'Utilisateur supprimé'}
