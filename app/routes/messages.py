from flask import Blueprint

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages')
def list_messages():
    return "Liste des messages"