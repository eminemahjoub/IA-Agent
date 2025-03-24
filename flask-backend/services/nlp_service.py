import spacy
import os
import json
from datetime import datetime, timedelta

class NLPService:
    """Service for natural language processing tasks"""
    
    def __init__(self):
        """Initialize the NLP service with spaCy model"""
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_md")
            
            # Load intents data
            self.intents = self._load_intents()
            
            # Entity extraction configuration
            self.productivity_entities = {
                'DATE': 'date',
                'TIME': 'time',
                'PERSON': 'person',
                'ORG': 'organization',
                'GPE': 'location',
                'PRIORITY': 'priority',
                'CATEGORY': 'category',
                'DURATION': 'duration'
            }
            
            # Add custom entity recognition for priorities
            priorities = ["high", "medium", "low", "urgent", "critical", "normal"]
            self.priority_patterns = [{"label": "PRIORITY", "pattern": priority} for priority in priorities]
            
            # Add custom entity recognition for categories
            categories = ["work", "personal", "health", "finance", "education", "family", "project", "meeting", "call"]
            self.category_patterns = [{"label": "CATEGORY", "pattern": category} for category in categories]
            
            # Add custom entity matcher
            self.matcher = spacy.matcher.PhraseMatcher(self.nlp.vocab)
            self._add_custom_patterns()
            
            print("NLP Service initialized successfully")
        except Exception as e:
            print(f"Error initializing NLP service: {str(e)}")
            # Fallback to empty model
            self.nlp = None
            self.intents = {}
    
    def _load_intents(self):
        """Load intents from JSON file"""
        try:
            intents_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'intents.json')
            if os.path.exists(intents_path):
                with open(intents_path, 'r') as file:
                    return json.load(file)
            else:
                # Return default intents if file not found
                return {
                    "intents": [
                        {
                            "tag": "greeting",
                            "patterns": ["hi", "hello", "hey", "good morning", "good evening", "hi there"],
                            "responses": ["Hello! How can I help you with your productivity today?", "Hi there! What would you like to do?"]
                        },
                        {
                            "tag": "goodbye",
                            "patterns": ["bye", "see you", "goodbye", "exit", "quit"],
                            "responses": ["Goodbye!", "Have a great day!", "See you soon!"]
                        },
                        {
                            "tag": "add_task",
                            "patterns": ["add task", "create task", "new task", "add a task", "create a new task", "remind me to"],
                            "responses": ["Task added successfully", "I've added that task for you", "Your new task has been created"]
                        },
                        {
                            "tag": "create_habit",
                            "patterns": ["track habit", "new habit", "create habit", "add habit", "start tracking"],
                            "responses": ["Habit created successfully", "I'll help you track that habit", "Your new habit has been added"]
                        }
                    ]
                }
        except Exception as e:
            print(f"Error loading intents: {str(e)}")
            return {"intents": []}
    
    def _add_custom_patterns(self):
        """Add custom patterns to the matcher"""
        if not self.nlp:
            return
            
        # Add priority patterns
        priority_patterns = [self.nlp(text) for text in ["high", "medium", "low", "urgent", "critical", "normal"]]
        self.matcher.add("PRIORITY", None, *priority_patterns)
        
        # Add category patterns
        category_patterns = [self.nlp(text) for text in ["work", "personal", "health", "finance", "education", "family", "project", "meeting", "call"]]
        self.matcher.add("CATEGORY", None, *category_patterns)
        
        # Add duration patterns
        duration_patterns = [self.nlp(text) for text in ["minute", "hour", "day", "week", "month", "year"]]
        self.matcher.add("DURATION", None, *duration_patterns)
    
    def analyze_text(self, text):
        """
        Analyze text using spaCy
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Analyzed text with tokens, entities, and other information
        """
        if not self.nlp or not text:
            return {"tokens": [], "entities": [], "sentiment": "neutral"}
        
        try:
            # Process text with spaCy
            doc = self.nlp(text)
            
            # Extract tokens
            tokens = [{"text": token.text, "lemma": token.lemma_, "pos": token.pos_, "is_stop": token.is_stop} for token in doc]
            
            # Extract entities
            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "type": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
            
            # Add custom entities from matcher
            matches = self.matcher(doc)
            for match_id, start, end in matches:
                match_type = self.nlp.vocab.strings[match_id]
                span = doc[start:end]
                entities.append({
                    "text": span.text,
                    "type": match_type,
                    "start": span.start_char,
                    "end": span.end_char
                })
            
            # Basic sentiment analysis
            sentiment = "neutral"
            if doc._.has_sentiment:
                sentiment_score = doc._.sentiment
                if sentiment_score > 0.3:
                    sentiment = "positive"
                elif sentiment_score < -0.3:
                    sentiment = "negative"
            
            return {
                "tokens": tokens,
                "entities": entities,
                "sentiment": sentiment
            }
        except Exception as e:
            print(f"Error analyzing text: {str(e)}")
            return {"tokens": [], "entities": [], "sentiment": "neutral", "error": str(e)}
    
    def extract_entities(self, text):
        """
        Extract entities from text
        
        Args:
            text (str): Text to extract entities from
            
        Returns:
            dict: Dictionary of entity types and values
        """
        if not self.nlp or not text:
            return {}
        
        try:
            # Process text with spaCy
            doc = self.nlp(text)
            
            # Extract entities
            entities = {}
            for ent in doc.ents:
                entity_type = self.productivity_entities.get(ent.label_, ent.label_.lower())
                if entity_type not in entities:
                    entities[entity_type] = []
                entities[entity_type].append(ent.text)
            
            # Add custom entities from matcher
            matches = self.matcher(doc)
            for match_id, start, end in matches:
                match_type = self.nlp.vocab.strings[match_id]
                entity_type = self.productivity_entities.get(match_type, match_type.lower())
                if entity_type not in entities:
                    entities[entity_type] = []
                entities[entity_type].append(doc[start:end].text)
            
            # Process dates and times
            if 'date' in entities:
                try:
                    # Attempt to parse relative dates like "tomorrow", "next week", etc.
                    for i, date_text in enumerate(entities['date']):
                        if date_text.lower() == 'tomorrow':
                            tomorrow = datetime.now() + timedelta(days=1)
                            entities['date'][i] = tomorrow.strftime('%Y-%m-%d')
                        elif date_text.lower() == 'today':
                            entities['date'][i] = datetime.now().strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"Error processing dates: {str(e)}")
            
            return entities
        except Exception as e:
            print(f"Error extracting entities: {str(e)}")
            return {}
    
    def detect_intent(self, text):
        """
        Detect intent from text
        
        Args:
            text (str): Text to detect intent from
            
        Returns:
            dict: Intent information with tag, confidence, and response
        """
        if not self.nlp or not text or 'intents' not in self.intents:
            return {"tag": "unknown", "confidence": 0, "response": "I'm not sure what you want to do."}
        
        try:
            # Process text with spaCy
            doc = self.nlp(text.lower())
            
            # Calculate similarity scores for each intent
            max_score = 0
            best_intent = None
            
            for intent in self.intents['intents']:
                score = 0
                count = 0
                
                for pattern in intent['patterns']:
                    pattern_doc = self.nlp(pattern.lower())
                    pattern_score = doc.similarity(pattern_doc)
                    score += pattern_score
                    count += 1
                
                if count > 0:
                    avg_score = score / count
                    if avg_score > max_score:
                        max_score = avg_score
                        best_intent = intent
            
            # Return the best intent if the confidence is above threshold
            if best_intent and max_score > 0.60:
                import random
                return {
                    "tag": best_intent['tag'],
                    "confidence": max_score,
                    "response": random.choice(best_intent['responses'])
                }
            else:
                return {
                    "tag": "unknown",
                    "confidence": max_score,
                    "response": "I'm not sure what you want to do."
                }
        except Exception as e:
            print(f"Error detecting intent: {str(e)}")
            return {"tag": "unknown", "confidence": 0, "response": "I'm not sure what you want to do."}
    
    def extract_task(self, text):
        """
        Extract task information from text
        
        Args:
            text (str): Text to extract task from
            
        Returns:
            dict: Task information with title, priority, date, etc.
        """
        if not self.nlp or not text:
            return {"title": text}
        
        try:
            # Process text with spaCy
            entities = self.extract_entities(text)
            
            # Extract task details
            task = {"title": text}
            
            # Remove entities from title
            for entity_type, entity_values in entities.items():
                for entity in entity_values:
                    task["title"] = task["title"].replace(entity, "").strip()
            
            # Add entities to task
            if 'priority' in entities and entities['priority']:
                task['priority'] = entities['priority'][0].lower()
            
            if 'category' in entities and entities['category']:
                task['category'] = entities['category'][0].lower()
            
            if 'date' in entities and entities['date']:
                task['dueDate'] = entities['date'][0]
            
            if 'time' in entities and entities['time']:
                # If we have a date and time, combine them
                if 'dueDate' in task:
                    task['dueDate'] += f"T{entities['time'][0]}"
                else:
                    task['dueDate'] = f"{datetime.now().strftime('%Y-%m-%d')}T{entities['time'][0]}"
            
            # Clean up title if needed (remove "add task", "create task", etc.)
            for phrase in ["add task", "create task", "new task", "add a task", "create a new task", "remind me to"]:
                task["title"] = task["title"].replace(phrase, "").strip()
            
            # If title is empty, use the original text
            if not task["title"]:
                task["title"] = text
            
            return task
        except Exception as e:
            print(f"Error extracting task: {str(e)}")
            return {"title": text}
    
    def process(self, text):
        """
        Process natural language command and determine action
        
        Args:
            text (str): User command or query text
            
        Returns:
            dict: Response with intent, action, and data
        """
        if not self.nlp or not text:
            return {
                "intent": "unknown",
                "action": "none",
                "response": "I couldn't process that command.",
                "data": {}
            }
        
        try:
            # Detect intent
            intent = self.detect_intent(text)
            
            # Extract entities
            entities = self.extract_entities(text)
            
            # Determine action based on intent
            action = "none"
            data = {}
            response = intent.get("response", "I'm not sure what you want to do.")
            
            if intent["tag"] == "add_task":
                action = "create_task"
                data = self.extract_task(text)
                response = f"Adding task: {data['title']}"
            
            elif intent["tag"] == "list_tasks":
                action = "list_tasks"
                if 'date' in entities:
                    data['date'] = entities['date'][0]
                if 'category' in entities:
                    data['category'] = entities['category'][0]
                response = "Here are your tasks"
            
            elif intent["tag"] == "create_habit":
                action = "create_habit"
                # Extract habit details
                habit = {"name": text}
                
                # Remove entities from name
                for entity_type, entity_values in entities.items():
                    for entity in entity_values:
                        habit["name"] = habit["name"].replace(entity, "").strip()
                
                # Add entities to habit
                if 'category' in entities and entities['category']:
                    habit['category'] = entities['category'][0].lower()
                
                # Clean up name
                for phrase in ["track habit", "new habit", "create habit", "add habit", "start tracking"]:
                    habit["name"] = habit["name"].replace(phrase, "").strip()
                
                data = habit
                response = f"Creating habit: {data['name']}"
            
            # Return the response
            return {
                "intent": intent["tag"],
                "confidence": intent["confidence"],
                "action": action,
                "response": response,
                "entities": entities,
                "data": data
            }
        
        except Exception as e:
            print(f"Error processing command: {str(e)}")
            return {
                "intent": "unknown",
                "action": "none",
                "response": "I encountered an error processing your request.",
                "error": str(e),
                "data": {}
            } 