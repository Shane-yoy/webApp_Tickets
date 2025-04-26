# app/api/messages.py

from flask_restx import Namespace, Resource
from app.models import Message
from flask_login import current_user
from flask import jsonify
from app import db

messages_api = Namespace('messages', description='Messages API')

@messages_api.route('/<int:ticket_id>')
class MessagesByTicket(Resource):
    def get(self, ticket_id):
        # Récupère tous les messages associés à un ticket
        messages = Message.query.filter_by(ticket_id=ticket_id).order_by(Message.created_at).all()

        results = []
        for msg in messages:
            results.append({
                'id': msg.id,
                'user': msg.user.name,
                'role': msg.user.role,
                'content': msg.content,
                'created_at': msg.created_at.strftime('%d/%m/%Y %H:%M'),
            })

        return jsonify(results)
