import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import our AI service modules
from services.nlp_service import NLPService
from services.sentiment_service import SentimentAnalyzer
from services.ml_service import MLPredictor

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize services
nlp_service = NLPService()
sentiment_analyzer = SentimentAnalyzer()
ml_predictor = MLPredictor()

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Personal Productivity Assistant - Python AI Service",
        "endpoints": [
            "/api/analyze-text",
            "/api/sentiment-analysis",
            "/api/predict-completion",
            "/api/suggest-tasks",
            "/api/extract-entities"
        ]
    })

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    analysis = nlp_service.analyze(data['text'])
    return jsonify(analysis)

@app.route('/api/sentiment-analysis', methods=['POST'])
def analyze_sentiment():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    sentiment = sentiment_analyzer.analyze(data['text'])
    return jsonify(sentiment)

@app.route('/api/predict-completion', methods=['POST'])
def predict_completion():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    completion = nlp_service.predict_completion(data['text'])
    return jsonify({"completion": completion})

@app.route('/api/suggest-tasks', methods=['POST'])
def suggest_tasks():
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error": "No user ID provided"}), 400
    
    # Optional context can be provided
    context = data.get('context', {})
    
    suggestions = ml_predictor.suggest_tasks(data['user_id'], context)
    return jsonify({"suggestions": suggestions})

@app.route('/api/extract-entities', methods=['POST'])
def extract_entities():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    entities = nlp_service.extract_entities(data['text'])
    return jsonify({"entities": entities})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False') == 'True') 