# app/ai_models/train_pipeline.py

import joblib
from app import db
from app.models import Message
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def retrain_model_from_database():
    """Réentraîne le modèle sur tous les messages existants en base."""
    # 1. Charger les messages
    messages = Message.query.all()
    if not messages:
        raise ValueError("Aucun message trouvé pour entraîner le modèle.")

    # 2. Préparer les textes
    texts = [m.content for m in messages]
    labels = [m.label for m in messages]  # ⚡ Attention : il faut que ta table Message ait une colonne `label`

    if not labels or any(l is None for l in labels):
        raise ValueError("Certains messages n'ont pas de label. Impossible d'entraîner.")

    # 3. Vectorisation
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2), stop_words='english')
    X = vectorizer.fit_transform(texts)

    # 4. Modèle
    model = LogisticRegression(max_iter=100, random_state=32)
    model.fit(X, labels)

    # 5. Sauvegarde
    joblib.dump(model, "app/ai_models/TF_IDF_models/model_analyse_tweet.joblib")
    joblib.dump(vectorizer, "app/ai_models/TF_IDF_models/vectorizer.joblib")

    return f"Modèle réentraîné avec {len(messages)} messages."
