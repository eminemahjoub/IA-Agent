import os
import spacy
from transformers import pipeline

class NLPService:
    def __init__(self):
        """Initialize the NLP service with spaCy and transformers models"""
        # Load spaCy model for general NLP tasks
        try:
            self.nlp = spacy.load("en_core_web_md")
        except:
            # If model not found, download it
            import subprocess
            subprocess.call(["python", "-m", "spacy", "download", "en_core_web_md"])
            self.nlp = spacy.load("en_core_web_md")
        
        # Initialize text completion model (for command suggestions)
        try:
            self.text_generator = pipeline("text-generation", model="gpt2")
        except:
            # Fallback to a smaller model if GPU memory is limited
            self.text_generator = None
            print("Warning: Text generation model could not be loaded.")
    
    def analyze(self, text):
        """Perform comprehensive NLP analysis on the input text"""
        doc = self.nlp(text)
        
        # Extract various linguistic features
        analysis = {
            "tokens": [{"text": token.text, "lemma": token.lemma_, "pos": token.pos_, "is_stop": token.is_stop} 
                      for token in doc],
            "entities": [{"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char} 
                        for ent in doc.ents],
            "noun_chunks": [chunk.text for chunk in doc.noun_chunks],
            "sentences": [sent.text for sent in doc.sents],
        }
        
        # Perform dependency parsing to understand sentence structure
        analysis["dependencies"] = []
        for token in doc:
            if token.dep_ != "":
                analysis["dependencies"].append({
                    "text": token.text,
                    "dependency": token.dep_,
                    "head": token.head.text
                })
        
        # Extract key phrases (combinations of subjects, verbs, and objects)
        analysis["key_phrases"] = self._extract_key_phrases(doc)
        
        return analysis
    
    def extract_entities(self, text):
        """Extract named entities with detailed information"""
        doc = self.nlp(text)
        
        entities = []
        for ent in doc.ents:
            entity = {
                "text": ent.text,
                "label": ent.label_,
                "description": spacy.explain(ent.label_),
                "start_char": ent.start_char,
                "end_char": ent.end_char
            }
            
            # Add additional processing for dates and times
            if ent.label_ in ["DATE", "TIME"]:
                # Try to normalize the date/time (basic implementation)
                entity["normalized"] = self._normalize_date_time(ent.text)
            
            entities.append(entity)
            
        # Extract custom entities specific to productivity context
        custom_entities = self._extract_custom_entities(doc)
        entities.extend(custom_entities)
        
        return entities
    
    def predict_completion(self, text, max_length=50):
        """Predict text completion for user commands"""
        if not self.text_generator:
            return "Text completion not available"
        
        try:
            completions = self.text_generator(text, max_length=max_length, num_return_sequences=1)
            return completions[0]['generated_text']
        except Exception as e:
            print(f"Error in text completion: {e}")
            return text
    
    def _extract_key_phrases(self, doc):
        """Extract key action phrases from the document"""
        phrases = []
        
        for sent in doc.sents:
            # Find the main verb and its arguments
            main_verb = None
            subject = None
            obj = None
            
            for token in sent:
                if token.pos_ == "VERB":
                    main_verb = token
                    
                    # Find the subject
                    for child in token.children:
                        if child.dep_ in ["nsubj", "nsubjpass"]:
                            subject = child
                            break
                    
                    # Find the object
                    for child in token.children:
                        if child.dep_ in ["dobj", "pobj"]:
                            obj = child
                            break
            
            if main_verb:
                phrase = {}
                if subject:
                    phrase["subject"] = subject.text
                phrase["verb"] = main_verb.text
                if obj:
                    phrase["object"] = obj.text
                
                if len(phrase) > 1:  # Only add if we have more than just a verb
                    phrases.append(phrase)
        
        return phrases
    
    def _normalize_date_time(self, date_text):
        """Simple date/time normalization (placeholder for more advanced implementation)"""
        # This would typically use a date parsing library like dateutil or datetime
        # For now, just return the original text
        return date_text
    
    def _extract_custom_entities(self, doc):
        """Extract custom entities specific to productivity tasks"""
        custom_entities = []
        
        # Patterns for task-related entities
        priority_terms = {
            "high": ["urgent", "important", "critical", "high priority", "ASAP"],
            "medium": ["moderate", "normal", "medium priority"],
            "low": ["low priority", "when possible", "someday", "eventually"]
        }
        
        # Check for priority mentions
        for priority, terms in priority_terms.items():
            for term in terms:
                if term in doc.text.lower():
                    custom_entities.append({
                        "text": term,
                        "label": "PRIORITY",
                        "value": priority,
                        "start_char": doc.text.lower().find(term),
                        "end_char": doc.text.lower().find(term) + len(term)
                    })
        
        return custom_entities 