from flask import Blueprint, request, jsonify, render_template, abort
from flask_login import current_user
from app import db
from app.models import Ticket, Message, Prediction, ModelVersion
from datetime import datetime
import joblib
import os
from app.decorators import role_required

admin_chat_bp = Blueprint('admin_chat', __name__)

# 🧠 Charger le modèle IA
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../ai_models/TF_IDF_models")
model = joblib.load(os.path.join(MODEL_DIR, "model_analyse_tweet.joblib"))
vectorizer = joblib.load(os.path.join(MODEL_DIR, "vectorizer.joblib"))

def predict_sentiment(text):
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    confidence = model.predict_proba(X)[0].max()
    return prediction, float(confidence)

# Route pour afficher la page de chat admin
@admin_chat_bp.route('/admin/chat/<int:ticket_id>', methods=['GET'])
@role_required('admin')
def view_chat(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template('admin_chat.html', ticket=ticket)

# Route GET pour récupérer les messages d'un ticket
@admin_chat_bp.route('/api/admin/messages/<int:ticket_id>', methods=['GET'])
@role_required('admin')
def get_admin_messages(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    messages = Message.query.filter_by(ticket_id=ticket.id).order_by(Message.created_at).all()

    serialized_messages = [{
        'id': msg.id,
        'user': msg.user.name,
        'content': msg.content,
        'created_at': msg.created_at.isoformat(),
        'prediction': msg.prediction.sentiment if msg.prediction else 'Non prédite',
        'confidence': round(msg.prediction.confidence * 100, 1) if msg.prediction else None,
        'role': 'sent' if msg.user_id == current_user.id else 'received'
    } for msg in messages]

    return jsonify(serialized_messages)

# Route POST pour envoyer un message et prédire côté admin
@admin_chat_bp.route('/send_message_admin/<int:ticket_id>', methods=['POST'])
@role_required('admin')
def send_admin_message(ticket_id):
    content = request.json.get('content')
    if not content:
        return jsonify({"error": "Message vide"}), 400

    message = Message(ticket_id=ticket_id, user_id=current_user.id, content=content)
    db.session.add(message)
    db.session.flush()

    sentiment_label, confidence = predict_sentiment(content)
    sentiment = 'positive' if sentiment_label == 1 else 'negative'

    version = ModelVersion.query.filter_by(is_active=True).first()

    prediction = Prediction(
        message_id=message.id,
        sentiment=sentiment,
        confidence=confidence,
        model_version=version
    )
    db.session.add(prediction)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": {
            "id": message.id,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "user_name": current_user.name,
            "role": "sent",
            "prediction": sentiment
        }
    }), 200
