import pandas as pd
import numpy as np
import re
import joblib
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Import spécial pour retrain depuis base
from app import db
from app.models import Message

# Configuration MLflow
mlflow.set_tracking_uri("http://mlflow:5001")
mlflow.set_experiment("Analyse_Sentiment")

# Fonctions utiles
def load_data(file_path):
    data = pd.read_csv(file_path)
    print(f"Données chargées : {data.shape[0]} lignes.")
    return data

def preprocess_data(data):
    if 'text' not in data.columns or 'label' not in data.columns:
        raise ValueError("Les colonnes 'text' et 'label' doivent exister.")

    data.dropna(subset=['text', 'label'], inplace=True)
    data['label'] = data['label'].astype(int)

    def clean_text(text):
        text = text.lower()
        text = re.sub(r"http\S+|@\w+|#\w+|[^a-zA-Z\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    data['text'] = data['text'].apply(clean_text)
    data.drop_duplicates(subset=['text'], inplace=True)
    return data

def vectorize_data(X_train, X_test):
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2), stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    return X_train_tfidf, X_test_tfidf, vectorizer

def train_model(X_train_tfidf, y_train):
    model = LogisticRegression(max_iter=100, random_state=32)
    model.fit(X_train_tfidf, y_train)
    return model

def evaluate_model(model, X_test_tfidf, y_test):
    y_pred = model.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy : {acc:.4f}")
    print(classification_report(y_test, y_pred))
    return acc

def main():
    """
    Entraîne le modèle de base à partir du CSV 'french_tweets.csv'.
    """
    file_path = "app/ai_models/data_set/french_tweets.csv"  # ➔ Corrigé en chemin relatif
    data = load_data(file_path)
    data = preprocess_data(data)
    X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, random_state=10)
    X_train_tfidf, X_test_tfidf, vectorizer = vectorize_data(X_train, X_test)

    with mlflow.start_run(run_name="Initial_Training_from_CSV"):
        model = train_model(X_train_tfidf, y_train)
        acc = evaluate_model(model, X_test_tfidf, y_test)

        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("max_iter", 100)
        mlflow.log_param("random_state", 32)
        mlflow.log_metric("train_accuracy", model.score(X_train_tfidf, y_train))
        mlflow.log_metric("test_accuracy", acc)
        mlflow.sklearn.log_model(model, artifact_path="model")

        # Sauvegarde locale
        joblib.dump(model, "app/ai_models/TF_IDF_models/model_analyse_tweet.joblib")
        joblib.dump(vectorizer, "app/ai_models/TF_IDF_models/vectorizer.joblib")
        print("Modèle et vectorizer sauvegardés.")


# 🚀 NOUVEAU : pour la pipeline automatique
def retrain_model_from_database():
    """
    🚀 Réentraîne un modèle de prédiction depuis les données réelles stockées dans la table Message.
    """
    print("🚀 Démarrage du réentraînement du modèle à partir de la base de données...")

    # Charger tous les messages
    messages = Message.query.all()

    if not messages:
        print("❌ Pas de messages disponibles pour l'entraînement.")
        return

    # Extraire contenus et labels
    texts = []
    labels = []
    for msg in messages:
        if hasattr(msg, 'label') and msg.label is not None:
            texts.append(msg.content)
            labels.append(msg.label)

    if len(texts) == 0:
        print("❌ Aucun message avec label trouvé pour l'entraînement.")
        return

    # Split données
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

    # Vectorisation
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2), stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Entraînement du modèle
    model = LogisticRegression(max_iter=100, random_state=32)
    model.fit(X_train_tfidf, y_train)

    # Évaluation
    accuracy = accuracy_score(y_test, model.predict(X_test_tfidf))
    print(f"✅ Nouveau modèle accuracy : {accuracy:.4f}")

    # Logger dans MLflow
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("Analyse_Sentiment")

    with mlflow.start_run(run_name="Retrain_from_DB"):
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("max_iter", 100)
        mlflow.log_param("random_state", 32)
        mlflow.log_metric("test_accuracy", accuracy)
        mlflow.sklearn.log_model(model, artifact_path="model")

    # Sauvegarde locale
    joblib.dump(model, "app/ai_models/TF_IDF_models/model_analyse_tweet.joblib")
    joblib.dump(vectorizer, "app/ai_models/TF_IDF_models/vectorizer.joblib")

    print("💾 Nouveau modèle et vectorizer sauvegardés avec succès.")


if __name__ == "__main__":
    main()
