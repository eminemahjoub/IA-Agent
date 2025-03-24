from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.nlp_service import NLPService
from services.sentiment_service import SentimentAnalyzer
from services.ml_service import MLPredictor

nlp_bp = Blueprint('nlp', __name__)

# Initialize services
nlp_service = NLPService()
sentiment_analyzer = SentimentAnalyzer()
ml_predictor = MLPredictor()

@nlp_bp.route('/analyze-text', methods=['POST'])
@jwt_required()
def analyze_text():
    """Analyze text using NLP service"""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Text is required'}), 400
    
    text = data['text']
    result = nlp_service.analyze_text(text)
    return jsonify(result)

@nlp_bp.route('/extract-entities', methods=['POST'])
@jwt_required()
def extract_entities():
    """Extract entities from text"""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Text is required'}), 400
    
    text = data['text']
    entities = nlp_service.extract_entities(text)
    return jsonify({'entities': entities})

@nlp_bp.route('/sentiment-analysis', methods=['POST'])
@jwt_required()
def analyze_sentiment():
    """Analyze sentiment of text"""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Text is required'}), 400
    
    text = data['text']
    sentiment = sentiment_analyzer.analyze_sentiment(text)
    return jsonify(sentiment)

@nlp_bp.route('/suggest-tasks', methods=['POST'])
@jwt_required()
def suggest_tasks():
    """Suggest tasks based on user context"""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    context = data.get('context', {})
    count = data.get('count', 5)
    
    try:
        suggestions = ml_predictor.suggest_tasks(user_id, context, count)
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nlp_bp.route('/parse-command', methods=['POST'])
@jwt_required()
def parse_command():
    """Parse natural language command"""
    data = request.get_json()
    if not data or 'command' not in data:
        return jsonify({'error': 'Command is required'}), 400
    
    command = data['command']
    result = nlp_service.process(command)
    return jsonify(result) 