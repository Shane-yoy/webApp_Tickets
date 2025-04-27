# app/tasks.py

from app.celery_worker import celery
from app.models import Message
from app.ai_models.train_model import retrain_model_from_database
from app import db
import os

# Stockage simple du nombre de messages depuis le dernier entraînement
LAST_TRAINING_COUNT_FILE = "last_training_count.txt"

def load_last_training_count():
    """Charge le dernier nombre de messages enregistrés."""
    if os.path.exists(LAST_TRAINING_COUNT_FILE):
        with open(LAST_TRAINING_COUNT_FILE, "r") as f:
            return int(f.read())
    return 0

def save_last_training_count(count):
    """Sauvegarde le nombre actuel de messages."""
    with open(LAST_TRAINING_COUNT_FILE, "w") as f:
        f.write(str(count))

@celery.task
def check_and_retrain_model():
    """
    Vérifie si >=500 nouveaux messages et réentraîne automatiquement.
    """
    total_messages = Message.query.count()
    last_training_count = load_last_training_count()

    print(f"ℹ️ Nombre actuel de messages : {total_messages}")
    print(f"ℹ️ Dernier réentraînement après : {last_training_count} messages")

    if (total_messages - last_training_count) >= 500:
        retrain_model_from_database()
        save_last_training_count(total_messages)
        print("✅ Modèle réentraîné automatiquement après 500 nouveaux messages !")
    else:
        print(f"⏳ Pas encore assez de nouveaux messages ({total_messages - last_training_count}/500)")
