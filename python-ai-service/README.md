# Python AI Service for ProdigyAI

This is the Python-based AI microservice that powers ProdigyAI's advanced natural language processing and machine learning capabilities, providing intelligent productivity recommendations and insights.

## Features

- **Advanced NLP Analysis**: Detailed linguistic analysis of text using spaCy
- **Named Entity Recognition**: Extract entities like dates, times, people, and organizations
- **Sentiment Analysis**: Detect user mood and emotional state
- **Task Prediction**: Suggest tasks based on user patterns and context
- **Text Completion**: Predict and complete user commands

## Technologies Used

- **Flask**: Lightweight web framework
- **spaCy**: Industrial-strength NLP library
- **Transformers**: State-of-the-art NLP models from Hugging Face
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation and analysis

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Download the spaCy language model:
   ```
   python -m spacy download en_core_web_md
   ```
4. Copy `.env.example` to `.env` and configure as needed
5. Start the service:
   ```
   python app.py
   ```

## API Endpoints

- **GET /** - Service health check and information
- **POST /api/analyze-text** - Perform detailed NLP analysis
- **POST /api/sentiment-analysis** - Analyze sentiment and emotions
- **POST /api/predict-completion** - Predict text completion
- **POST /api/suggest-tasks** - Get personalized task suggestions
- **POST /api/extract-entities** - Extract named entities

## Integration with Node.js Backend

This service is designed to work with the main Node.js backend. The Node.js server makes API calls to this Python service when advanced AI capabilities are needed.

### Example Integration Flow:

1. User sends a command to Node.js backend
2. Node.js performs basic intent recognition
3. For complex analysis, Node.js calls the Python service
4. Python service processes the request and returns enhanced results
5. Node.js combines results and responds to the user

## Development

To extend this service:

1. Add new models in the `services` directory
2. Register new endpoints in `app.py`
3. Update integration with Node.js in the main application 