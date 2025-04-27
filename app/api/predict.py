# app/api/predict.py

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.ai_models.predict_model import predict_sentiment_from_db
from app.models import Message

api = Namespace('predict', description="Prédictions IA à partir des messages")

# Modèle Swagger pour la prédiction
prediction_model = api.model('Prediction', {
    'message_id': fields.Integer(description='ID du message'),
    'content': fields.String(description='Contenu du message'),
    'prediction': fields.Integer(description='Prédiction du sentiment (0 = négatif, 1 = positif)')
})

@api.route('/from-db')
class PredictFromDB(Resource):
    @api.doc('predire_dernier_messages')
    @api.marshal_list_with(prediction_model)
    @jwt_required()
    def get(self):
        """
        Prédit le sentiment des 10 derniers messages stockés en base.
        """
        # Récupération des messages
        messages = Message.query.order_by(Message.created_at.desc()).limit(10).all()

        if not messages:
            api.abort(404, "Aucun message trouvé dans la base de données.")

        # Extraire les contenus pour la prédiction
        contents = [msg.content for msg in messages]
        
        # Prédiction
        predictions = predict_sentiment_from_db(contents)

        # Réponse formatée
        return [
            {
                "message_id": msg.id,
                "content": msg.content,
                "prediction": pred
            }
            for msg, pred in zip(messages, predictions)
        ]

