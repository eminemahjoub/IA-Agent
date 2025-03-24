import spacy
import os
import numpy as np
from collections import defaultdict

class SentimentAnalyzer:
    """Service for sentiment and emotion analysis"""
    
    def __init__(self):
        """Initialize the sentiment analyzer"""
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_md")
            
            # Emotion lexicon (simplified)
            self.emotion_lexicon = {
                'positive': ['happy', 'good', 'great', 'excellent', 'wonderful', 'fantastic', 'amazing', 'pleased',
                           'love', 'enjoy', 'like', 'glad', 'excited', 'thrilled', 'delighted', 'satisfied',
                           'proud', 'confident', 'calm', 'peaceful', 'relaxed', 'grateful', 'thankful'],
                           
                'negative': ['sad', 'bad', 'terrible', 'awful', 'horrible', 'disappointing', 'upset', 'angry',
                           'hate', 'dislike', 'annoyed', 'frustrated', 'furious', 'worried', 'anxious', 'stressed',
                           'afraid', 'scared', 'tired', 'exhausted', 'bored', 'confused', 'overwhelmed'],
                           
                'joy': ['happy', 'joy', 'delighted', 'excited', 'thrilled', 'pleased', 'content', 'cheerful'],
                'sadness': ['sad', 'unhappy', 'depressed', 'grief', 'heartbroken', 'miserable', 'disappointed', 'blue'],
                'anger': ['angry', 'mad', 'furious', 'irritated', 'annoyed', 'frustrated', 'rage', 'outraged'],
                'fear': ['afraid', 'scared', 'frightened', 'terrified', 'anxious', 'worried', 'panic', 'nervous'],
                'surprise': ['surprised', 'amazed', 'astonished', 'shocked', 'stunned', 'startled', 'unexpected'],
                'trust': ['trust', 'believe', 'confidence', 'faithful', 'reliable', 'dependable', 'loyal'],
                'anticipation': ['anticipate', 'expect', 'look forward', 'hope', 'waiting'],
                'disgust': ['disgusted', 'hate', 'dislike', 'aversion', 'repulsed', 'revolted', 'sick'],
                
                # Productivity-specific emotions
                'motivated': ['motivated', 'inspired', 'determined', 'focused', 'energized', 'driven', 'goal'],
                'unmotivated': ['unmotivated', 'uninspired', 'lazy', 'procrastinate', 'distracted', 'apathetic'],
                'productive': ['productive', 'efficient', 'effective', 'accomplish', 'completed', 'achieved', 'finished'],
                'unproductive': ['unproductive', 'inefficient', 'ineffective', 'wasted', 'distracted', 'unfinished'],
                'stressed': ['stressed', 'overwhelmed', 'pressured', 'swamped', 'overworked', 'burnout', 'burden'],
                'relieved': ['relieved', 'unburdened', 'destressed', 'unwound', 'relaxed', 'released']
            }
            
            # Build lexicon vectors
            self.emotion_vectors = {}
            for emotion, words in self.emotion_lexicon.items():
                vectors = [self.nlp(word).vector for word in words]
                self.emotion_vectors[emotion] = np.mean(vectors, axis=0) if vectors else None
            
            print("Sentiment Analyzer initialized successfully")
        except Exception as e:
            print(f"Error initializing Sentiment Analyzer: {str(e)}")
            # Fallback to empty model
            self.nlp = None
            self.emotion_vectors = {}
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment and emotions in text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Sentiment and emotion analysis results
        """
        if not self.nlp or not text:
            return {
                "sentiment": "neutral",
                "score": 0,
                "emotions": {},
                "productivity_mood": {
                    "motivation": "neutral",
                    "productivity": "neutral",
                    "stress": "neutral"
                }
            }
        
        try:
            # Process text with spaCy
            doc = self.nlp(text)
            
            # Extract tokens and filter stop words and punctuation
            tokens = [token for token in doc if not token.is_stop and not token.is_punct]
            
            # If no significant tokens, return neutral
            if not tokens:
                return {
                    "sentiment": "neutral",
                    "score": 0,
                    "emotions": {},
                    "productivity_mood": {
                        "motivation": "neutral",
                        "productivity": "neutral",
                        "stress": "neutral"
                    }
                }
            
            # Calculate sentiment using positive/negative lexicon
            sentiment_score = 0
            positive_count = 0
            negative_count = 0
            
            for token in tokens:
                if any(token.similarity(self.nlp(word)) > 0.7 for word in self.emotion_lexicon['positive']):
                    sentiment_score += 1
                    positive_count += 1
                elif any(token.similarity(self.nlp(word)) > 0.7 for word in self.emotion_lexicon['negative']):
                    sentiment_score -= 1
                    negative_count += 1
            
            # Normalize score between -1 and 1
            if positive_count + negative_count > 0:
                sentiment_score = sentiment_score / (positive_count + negative_count)
            
            # Determine sentiment label
            sentiment = "neutral"
            if sentiment_score > 0.2:
                sentiment = "positive"
            elif sentiment_score < -0.2:
                sentiment = "negative"
            
            # Calculate emotion scores
            emotions = defaultdict(float)
            for token in tokens:
                token_vector = token.vector
                
                for emotion, emotion_vector in self.emotion_vectors.items():
                    if emotion_vector is not None:
                        # Calculate cosine similarity
                        similarity = np.dot(token_vector, emotion_vector) / (np.linalg.norm(token_vector) * np.linalg.norm(emotion_vector))
                        
                        if similarity > 0.5:  # Threshold for emotion detection
                            emotions[emotion] += similarity
            
            # Normalize emotion scores and filter out low scores
            all_scores = list(emotions.values())
            if all_scores:
                max_score = max(all_scores)
                if max_score > 0:
                    for emotion in list(emotions.keys()):
                        emotions[emotion] = emotions[emotion] / max_score
                        
                        # Filter out emotions with low scores
                        if emotions[emotion] < 0.3:
                            del emotions[emotion]
            
            # Calculate productivity-specific metrics
            productivity_mood = {
                "motivation": "neutral",
                "productivity": "neutral",
                "stress": "neutral"
            }
            
            # Determine motivation level
            motivation_score = emotions.get('motivated', 0) - emotions.get('unmotivated', 0)
            if motivation_score > 0.3:
                productivity_mood["motivation"] = "high"
            elif motivation_score < -0.3:
                productivity_mood["motivation"] = "low"
                
            # Determine productivity level
            productivity_score = emotions.get('productive', 0) - emotions.get('unproductive', 0)
            if productivity_score > 0.3:
                productivity_mood["productivity"] = "high"
            elif productivity_score < -0.3:
                productivity_mood["productivity"] = "low"
                
            # Determine stress level
            stress_score = emotions.get('stressed', 0) - emotions.get('relieved', 0)
            if stress_score > 0.3:
                productivity_mood["stress"] = "high"
            elif stress_score < -0.3:
                productivity_mood["stress"] = "low"
            
            return {
                "sentiment": sentiment,
                "score": sentiment_score,
                "emotions": dict(emotions),
                "productivity_mood": productivity_mood
            }
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return {
                "sentiment": "neutral",
                "score": 0,
                "emotions": {},
                "productivity_mood": {
                    "motivation": "neutral",
                    "productivity": "neutral",
                    "stress": "neutral"
                },
                "error": str(e)
            }
    
    def get_productive_insights(self, text):
        """
        Get productivity insights from text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Productivity insights
        """
        if not self.nlp or not text:
            return {
                "insights": [],
                "suggestions": []
            }
        
        try:
            # Get sentiment analysis
            sentiment_analysis = self.analyze_sentiment(text)
            
            # Generate insights based on productivity mood
            insights = []
            suggestions = []
            
            # Check motivation level
            motivation = sentiment_analysis['productivity_mood']['motivation']
            if motivation == 'low':
                insights.append("You seem to be feeling unmotivated right now.")
                suggestions.append("Consider breaking your tasks into smaller, manageable chunks.")
                suggestions.append("Take a short break and do something you enjoy to reset your mindset.")
            elif motivation == 'high':
                insights.append("You're feeling motivated and ready to tackle challenges.")
                suggestions.append("Channel this energy into your most important or difficult tasks.")
            
            # Check productivity level
            productivity = sentiment_analysis['productivity_mood']['productivity']
            if productivity == 'low':
                insights.append("You may be feeling unproductive or inefficient.")
                suggestions.append("Try the Pomodoro technique: 25 minutes of focused work followed by a 5 minute break.")
                suggestions.append("Minimize distractions in your environment.")
            elif productivity == 'high':
                insights.append("You're in a productive state of mind.")
                suggestions.append("Keep up the momentum by continuing to check off tasks on your list.")
            
            # Check stress level
            stress = sentiment_analysis['productivity_mood']['stress']
            if stress == 'high':
                insights.append("You appear to be experiencing stress or feeling overwhelmed.")
                suggestions.append("Practice deep breathing or a quick meditation to reduce stress.")
                suggestions.append("Prioritize your tasks and focus on one thing at a time.")
            elif stress == 'low':
                insights.append("You seem relaxed and at ease.")
                suggestions.append("This is a good state for creative thinking and planning.")
            
            # Add emotion-based insights
            emotions = sentiment_analysis['emotions']
            if 'joy' in emotions and emotions['joy'] > 0.6:
                insights.append("Your positive mood can enhance creativity and problem-solving.")
            elif 'sadness' in emotions and emotions['sadness'] > 0.6:
                insights.append("You might be feeling down, which can impact focus and motivation.")
                suggestions.append("Set small, achievable goals to build momentum and boost your mood.")
            
            return {
                "insights": insights,
                "suggestions": suggestions,
                "mood": sentiment_analysis['productivity_mood']
            }
        except Exception as e:
            print(f"Error getting productive insights: {str(e)}")
            return {
                "insights": [],
                "suggestions": [],
                "error": str(e)
            } 