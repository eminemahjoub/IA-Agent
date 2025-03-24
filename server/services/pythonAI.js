const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config();

// Configuration for Python AI service
const PYTHON_AI_URL = process.env.PYTHON_AI_URL || 'http://localhost:5001';

/**
 * Client for the Python AI service
 */
class PythonAIClient {
  /**
   * Perform detailed NLP analysis on text
   * @param {string} text - The text to analyze
   * @returns {Promise<Object>} - The analysis results
   */
  async analyzeText(text) {
    try {
      const response = await axios.post(`${PYTHON_AI_URL}/api/analyze-text`, { text });
      return response.data;
    } catch (error) {
      console.error('Error analyzing text with Python AI service:', error.message);
      // Return a simplified fallback response when Python service is unavailable
      return {
        tokens: [],
        entities: [],
        error: 'Python AI service unavailable'
      };
    }
  }

  /**
   * Analyze sentiment and emotions in text
   * @param {string} text - The text to analyze
   * @returns {Promise<Object>} - The sentiment analysis results
   */
  async analyzeSentiment(text) {
    try {
      const response = await axios.post(`${PYTHON_AI_URL}/api/sentiment-analysis`, { text });
      return response.data;
    } catch (error) {
      console.error('Error analyzing sentiment with Python AI service:', error.message);
      return {
        sentiment: { label: 'NEUTRAL', score: 0.5 },
        emotions: [],
        error: 'Python AI service unavailable'
      };
    }
  }

  /**
   * Predict completion for text
   * @param {string} text - The text to complete
   * @returns {Promise<string>} - The predicted completion
   */
  async predictCompletion(text) {
    try {
      const response = await axios.post(`${PYTHON_AI_URL}/api/predict-completion`, { text });
      return response.data.completion;
    } catch (error) {
      console.error('Error predicting completion with Python AI service:', error.message);
      return text;
    }
  }

  /**
   * Get task suggestions for a user
   * @param {string} userId - The user ID
   * @param {Object} context - Optional context information
   * @returns {Promise<Array>} - The suggested tasks
   */
  async suggestTasks(userId, context = {}) {
    try {
      const response = await axios.post(`${PYTHON_AI_URL}/api/suggest-tasks`, { 
        user_id: userId,
        context
      });
      return response.data.suggestions;
    } catch (error) {
      console.error('Error getting task suggestions from Python AI service:', error.message);
      return [];
    }
  }

  /**
   * Extract entities from text
   * @param {string} text - The text to extract entities from
   * @returns {Promise<Array>} - The extracted entities
   */
  async extractEntities(text) {
    try {
      const response = await axios.post(`${PYTHON_AI_URL}/api/extract-entities`, { text });
      return response.data.entities;
    } catch (error) {
      console.error('Error extracting entities with Python AI service:', error.message);
      return [];
    }
  }

  /**
   * Check if the Python AI service is available
   * @returns {Promise<boolean>} - True if available, false otherwise
   */
  async isAvailable() {
    try {
      const response = await axios.get(PYTHON_AI_URL);
      return response.status === 200;
    } catch (error) {
      console.error('Python AI service is not available:', error.message);
      return false;
    }
  }
}

module.exports = new PythonAIClient(); 