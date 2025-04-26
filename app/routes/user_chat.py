from flask import Blueprint, request, jsonify, render_template, abort
from flask_login import login_required, current_user
from app import db
from app.models import Ticket, Message, Prediction, ModelVersion, User
from datetime import datetime
import joblib
import os

user_chat_bp = Blueprint('user_chat', __name__)

# 🧠 Charger le modèle IA une seule fois
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../ai_models/TF_IDF_models")
model = joblib.load(os.path.join(MODEL_DIR, "model_analyse_tweet.joblib"))
vectorizer = joblib.load(os.path.join(MODEL_DIR, "vectorizer.joblib"))

# Fonction pour prédire le sentiment
def predict_sentiment(text):
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    confidence = model.predict_proba(X)[0].max()  # Confidence maximale
    return prediction, float(confidence)


# Route GET pour récupérer les messages d'un ticket
@user_chat_bp.route('/api/messages/<int:ticket_id>', methods=['GET'])
@login_required
def get_messages(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    # Vérifier que le ticket appartient à l'utilisateur actuel
    if ticket.created_by != current_user.id:
        abort(403)

    # Récupérer tous les messages du ticket
    messages = Message.query.filter_by(ticket_id=ticket.id).order_by(Message.created_at).all()

    # Sérialiser les messages en JSON
    serialized_messages = [{
        'id': msg.id,
        'user': msg.user.name,  # Nom de l'utilisateur qui a envoyé le message
        'content': msg.content,
        'created_at': msg.created_at.isoformat(),
        'prediction': msg.prediction.sentiment if msg.prediction else 'Non prédite',  # Sentiment prédit
        'role': 'user' if msg.user_id == current_user.id else 'admin'  # Rôle de l'utilisateur
    } for msg in messages]

    return jsonify(serialized_messages)


# Route POST pour envoyer un message et générer une prédiction
@user_chat_bp.route('/send_message/<int:ticket_id>', methods=['POST'])
@login_required
def send_message(ticket_id):
    content = request.json.get('content')
    
    if not content:
        return jsonify({"error": "Message vide"}), 400

    # Enregistrer le message dans la base de données
    message = Message(ticket_id=ticket_id, user_id=current_user.id, content=content)
    db.session.add(message)
    db.session.flush()  # Pour avoir l'ID du message créé

    # Prédiction du sentiment
    sentiment_label, confidence = predict_sentiment(content)
    sentiment = 'positive' if sentiment_label == 1 else 'negative'

    # Récupérer la version active du modèle
    version = ModelVersion.query.filter_by(is_active=True).first()

    # Enregistrer la prédiction associée au message
    prediction = Prediction(
        message_id=message.id,
        sentiment=sentiment,
        confidence=confidence,
        model_version=version
    )
    db.session.add(prediction)
    db.session.commit()

    # Retourner la réponse avec le message et la prédiction
    return jsonify({
        "success": True,
        "message": {
            "id": message.id,
            "content": message.content,
            "created_at": message.created_at.strftime("%d/%m/%Y %H:%M"),
            "user_name": current_user.name,
            "role": current_user.role,
            "prediction": sentiment
        }
    }), 200

@user_chat_bp.route('/user/chat/<int:ticket_id>', methods=['GET'])
@login_required
def view_user_chat(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    # ⚠️ Vérifie que le ticket appartient bien à l'utilisateur connecté
    if ticket.created_by != current_user.id:
        abort(403)

    return render_template('user_chat.html', ticket=ticket)
