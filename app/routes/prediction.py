from flask import Blueprint

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/prediction')
def list_prediction():
    return "Liste des predictions"