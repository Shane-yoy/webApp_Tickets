# app/api/retrain.py

from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt
from app.ai_models.train_pipeline import retrain_model_from_database

api = Namespace('retrain', description='Réentraînement du modèle IA')

@api.route('/')
class RetrainModel(Resource):
    @api.doc('reentrainer_modele_ia')
    @jwt_required()
    def post(self):
        """
        (Admin uniquement) ➔ Réentraîne le modèle sur les derniers messages en base.
        """
        claims = get_jwt()
        if claims['role'] != 'admin':
            api.abort(403, "Accès réservé aux administrateurs.")

        try:
            result = retrain_model_from_database()
            return {"message": result}, 200
        except Exception as e:
            return {"error": str(e)}, 500
