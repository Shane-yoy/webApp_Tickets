# Import des bibliothèques nécessaires
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
from sklearn.svm import SVC

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


import matplotlib.pyplot as plt
import joblib 
import re
import mlflow
import mlflow.sklearn

# On configure MLflow
mlflow.set_tracking_uri("http://mlflow:5000")  # URL du serveur MLflow (ton conteneur Docker)
mlflow.set_experiment("Analyse_Sentiment")     # Nom du projet

def load_data(file_path):
    """Charge le fichier CSV contenant les tweets."""
    data = pd.read_csv(file_path)
    print(f"Données chargées : {data.shape[0]} lignes, {data.shape[1]} colonnes.")
    return data


def preprocess_data(data):
    """
    Prépare les données pour l'analyse en nettoyant les textes et en s'assurant de leur qualité.
    
    Args:
        data (pd.DataFrame): Jeu de données contenant les colonnes 'text' et 'label'.
    
    Returns:
        pd.DataFrame: Jeu de données nettoyé.
    """
    # Vérifier que les colonnes nécessaires existent
    if 'text' not in data.columns or 'label' not in data.columns:
        raise ValueError("Les colonnes 'text' et 'label' doivent exister dans le dataset.")
    
    # Supprimer les lignes avec des valeurs manquantes
    data.dropna(subset=['text', 'label'], inplace=True)
    
    # Convertir les labels en entiers
    data['label'] = data['label'].astype(int)
    
    # Nettoyage de base des textes
    def clean_text(text):
        text = text.lower()  # Convertir en minuscules
        text = re.sub(r"http\S+", "", text)  # Supprimer les URLs
        text = re.sub(r"@\w+", "", text)  # Supprimer les mentions Twitter
        text = re.sub(r"#\w+", "", text)  # Supprimer les hashtags
        text = re.sub(r"[^a-zA-Z\s]", "", text)  # Supprimer les caractères non alphabétiques
        text = re.sub(r"\s+", " ", text)  # Supprimer les espaces multiples
        return text.strip()
    
    # Appliquer le nettoyage à la colonne 'text'
    data['text'] = data['text'].apply(clean_text)
    
    # Optionnel : Supprimer les doublons
    data.drop_duplicates(subset=['text'], inplace=True)
    
    # Afficher le statut des données
    print(f"Données préparées : {data.shape[0]} lignes après nettoyage.")
    
    return data

def split_data(data):
    """Divise les données en ensembles d'entraînement et de test."""
    X_train, X_test, y_train, y_test = train_test_split(
        data['text'], data['label'], test_size=0.2, random_state=10
    )
    print(f"Train set : {len(X_train)} exemples, Test set : {len(X_test)} exemples.")
    return X_train, X_test, y_train, y_test


def vectorize_data(X_train, X_test):
    """Convertit les textes en vecteurs TF-IDF."""
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2), stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    print("Données vectorisées avec TF-IDF.")
    return X_train_tfidf, X_test_tfidf, vectorizer

def train_model(X_train_tfidf, y_train):
    """Entraîne un modèle de régression logistique et log dans MLflow."""
    with mlflow.start_run():
        model = LogisticRegression(max_iter=100, random_state=32)
        model.fit(X_train_tfidf, y_train)
        print("Modèle entraîné.")

        # Log des paramètres
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("max_iter", 100)
        mlflow.log_param("random_state", 32)

        # Log du score sur l'entraînement
        train_accuracy = model.score(X_train_tfidf, y_train)
        mlflow.log_metric("train_accuracy", train_accuracy)

        # Sauvegarde du modèle dans MLflow
        mlflow.sklearn.log_model(model, artifact_path="model")

    return model



def evaluate_model(model, X_test_tfidf, y_test):
    """Évalue le modèle sur l'ensemble de test et log dans MLflow."""
    y_pred = model.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy : {acc:.4f}")
    print("Rapport de classification :\n")
    print(classification_report(y_test, y_pred))

    # Log de la métrique test dans MLflow
    mlflow.log_metric("test_accuracy", acc)

    return acc


def main(file_path):
    """Pipeline principal pour l'analyse de sentiment."""
    data = load_data(file_path)
    data = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_data(data)
    X_train_tfidf, X_test_tfidf, vectorizer = vectorize_data(X_train, X_test)
    model = train_model(X_train_tfidf, y_train)
    evaluate_model(model, X_test_tfidf, y_test)
    return model, vectorizer

def save_model(model, vectorizer, model_filename=f'models_ML/model_analyse_tweet_{acc}.joblib', vectorizer_filename=f'models_ML/vectorizer_{acc}.joblib'):
    """Sauvegarde le modèle et le vectoriseur avec joblib."""
    joblib.dump(model, model_filename)
    joblib.dump(vectorizer, vectorizer_filename)
    print(f"Modèle sauvegardé sous {model_filename} et vectoriseur sous {vectorizer_filename}.")



if __name__ == "__main__":
    file_path = "/home/shaney/Bureau/Analyse_de_Sentiment/webApp_Tickets/app/ai_models/data_set/french_tweets.csv"  # Remplacez par le chemin vers votre fichier
    model, vectorizer = main(file_path)
    save_model(model=model, vectorizer=vectorizer)
    
    

def load_saved_model(model_filename='/home/shaney/Bureau/Analyse_de_Sentiment/webApp_Tickets/app/ai_models/TF_IDF_models/model_analyse_tweet.joblib', vectorizer_filename='/home/shaney/Bureau/Analyse_de_Sentiment/webApp_Tickets/app/ai_models/TF_IDF_models/vectorizer.joblib'):
    """Charge le modèle et le vectoriseur sauvegardés avec joblib."""
    model = joblib.load(model_filename)
    vectorizer = joblib.load(vectorizer_filename)
    print(f"Modèle chargé depuis {model_filename} et vectoriseur chargé depuis {vectorizer_filename}.")
    return model, vectorizer

def predict_new_data(model, vectorizer, new_data):
    """Effectue des prédictions sur de nouvelles données textuelles.
    
    Args:
        model: Modèle chargé pour l'inférence.
        vectorizer: Vectoriseur chargé pour transformer les données.
        new_data: Liste de chaînes de texte à analyser.
    
    Returns:
        Liste de prédictions effectuées par le modèle.
    """
    # Transformer les nouvelles données avec le vectoriseur
    new_data_tfidf = vectorizer.transform(new_data)
    
    # Effectuer les prédictions avec le modèle
    predictions = model.predict(new_data_tfidf)
    
    return predictions

model, vectorizer = load_saved_model()
new_tweets = ["je te déteste espece de monstre !",
"t'es vraiment nul",
"vraiment pas engageant",
"une perte de temps",
"décevant",

"encourageant"
"moi j'aime bien",
"je trouve le service tres efficaces"
"je t'aime",
"j'aime bien passer du temps avec toi <3"]
predictions = predict_new_data(model, vectorizer, new_tweets)
print("Prédictions pour les nouveaux tweets :", predictions)
