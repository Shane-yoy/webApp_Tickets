from app import create_app, db
from app.models import Entreprise, Ticket, Conversation, Message, SentimentAnalysis, User

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully!")