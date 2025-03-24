from transformers import pipeline
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        """Initialize the sentiment analysis service with a pre-trained model"""
        try:
            # Load the sentiment analysis pipeline from Hugging Face
            self.sentiment_analyzer = pipeline("sentiment-analysis")
            
            # Load a more specific model for emotion detection
            self.emotion_detector = pipeline(
                "text-classification", 
                model="j-hartmann/emotion-english-distilroberta-base", 
                return_all_scores=True
            )
        except Exception as e:
            print(f"Error initializing sentiment analysis models: {e}")
            self.sentiment_analyzer = None
            self.emotion_detector = None
    
    def analyze(self, text):
        """Analyze the sentiment and emotions in the given text"""
        result = {
            "text": text,
            "sentiment": self._get_sentiment(text),
            "emotions": self._get_emotions(text),
            "productivity_insights": self._get_productivity_insights(text)
        }
        return result
    
    def _get_sentiment(self, text):
        """Get basic sentiment (positive/negative) with confidence score"""
        if not self.sentiment_analyzer:
            return {"label": "NEUTRAL", "score": 0.5}
        
        try:
            sentiment = self.sentiment_analyzer(text)[0]
            return sentiment
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {"label": "NEUTRAL", "score": 0.5}
    
    def _get_emotions(self, text):
        """Detect emotions in the text (joy, sadness, anger, etc.)"""
        if not self.emotion_detector:
            return [{"label": "unknown", "score": 1.0}]
        
        try:
            emotions = self.emotion_detector(text)[0]
            # Sort emotions by score
            emotions.sort(key=lambda x: x["score"], reverse=True)
            return emotions
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return [{"label": "unknown", "score": 1.0}]
    
    def _get_productivity_insights(self, text):
        """Extract productivity-related insights from sentiment analysis"""
        insights = []
        
        # Get primary sentiment and emotion
        sentiment = self._get_sentiment(text)
        emotions = self._get_emotions(text)
        primary_emotion = emotions[0]["label"] if emotions else "unknown"
        
        # Check for signs of stress or burnout
        stress_indicators = ["overwhelmed", "stressed", "exhausted", "burnt out", 
                            "too much", "can't handle", "drowning in", "anxiety"]
        stress_level = 0
        for indicator in stress_indicators:
            if indicator in text.lower():
                stress_level += 1
        
        if stress_level > 1 or primary_emotion in ["anger", "fear", "sadness"]:
            insights.append({
                "type": "stress_warning",
                "message": "User may be experiencing stress or burnout",
                "confidence": min(0.5 + (stress_level * 0.1), 0.9)
            })
        
        # Check for motivation levels
        if sentiment["label"] == "POSITIVE" and sentiment["score"] > 0.8:
            if primary_emotion in ["joy", "optimism"]:
                insights.append({
                    "type": "high_motivation",
                    "message": "User appears highly motivated",
                    "confidence": sentiment["score"]
                })
        elif sentiment["label"] == "NEGATIVE" and sentiment["score"] > 0.7:
            if primary_emotion in ["sadness", "disappointment"]:
                insights.append({
                    "type": "low_motivation",
                    "message": "User may be experiencing low motivation",
                    "confidence": sentiment["score"]
                })
        
        # Check for focus issues
        focus_indicators = ["distracted", "can't focus", "losing focus", 
                           "hard to concentrate", "concentration"]
        if any(indicator in text.lower() for indicator in focus_indicators):
            insights.append({
                "type": "focus_issue",
                "message": "User may be having trouble focusing",
                "confidence": 0.7
            })
        
        return insights 