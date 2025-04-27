import joblib
from app.models import Message

def load_model_and_vectorizer():
    model = joblib.load("app/ai_models/TF_IDF_models/model_analyse_tweet.joblib")
    vectorizer = joblib.load("app/ai_models/TF_IDF_models/vectorizer.joblib")
    return model, vectorizer

def predict_sentiment(texts):
    model, vectorizer = load_model_and_vectorizer()
    X = vectorizer.transform(texts)
    predictions = model.predict(X)
    return predictions.tolist()

def predict_sentiment_from_db(contents):
    """
    Reçoit une liste de textes et retourne les prédictions.
    """
    return predict_sentiment(contents)
