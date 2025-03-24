import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import datetime
import os

class MLPredictor:
    def __init__(self):
        """Initialize the ML service for task prediction and suggestion"""
        # This would normally load pre-trained models
        # For now, we'll implement a simpler recommendation approach
        self.task_categories = [
            "Email", "Meeting", "Report", "Research", "Planning",
            "Development", "Design", "Review", "Testing", "Documentation",
            "Marketing", "Sales", "Customer Support", "Administrative", "Personal"
        ]
        
        # Sample tasks for each category (would be learned from user data)
        self.sample_tasks = {
            "Email": [
                "Respond to client emails",
                "Clear inbox",
                "Send project update email",
                "Follow up with team members"
            ],
            "Meeting": [
                "Prepare for team meeting",
                "Schedule client call",
                "Create meeting agenda",
                "Review meeting notes"
            ],
            "Report": [
                "Write weekly status report",
                "Prepare financial summary",
                "Create analytics report",
                "Compile project metrics"
            ],
            "Planning": [
                "Update project timeline",
                "Create sprint plan",
                "Set quarterly goals",
                "Review resource allocation"
            ],
            "Personal": [
                "Schedule doctor appointment",
                "Pay bills",
                "Buy groceries",
                "Exercise",
                "Read for 30 minutes"
            ]
        }
        
        # Initialize user profiles (would be loaded from database)
        self.user_profiles = {}
    
    def suggest_tasks(self, user_id, context=None):
        """Suggest tasks based on user history, current context, and time patterns"""
        suggestions = []
        
        # Get or create user profile
        user_profile = self._get_user_profile(user_id)
        
        # Get current date and time information
        now = datetime.datetime.now()
        day_of_week = now.weekday()  # 0=Monday, 6=Sunday
        hour_of_day = now.hour
        
        # 1. Suggest regular tasks based on day of week and time
        day_tasks = self._get_day_specific_tasks(day_of_week, user_profile)
        suggestions.extend(day_tasks)
        
        # 2. Suggest tasks based on time of day
        time_tasks = self._get_time_specific_tasks(hour_of_day, user_profile)
        suggestions.extend(time_tasks)
        
        # 3. If we have context, suggest tasks based on that
        if context:
            context_tasks = self._get_context_specific_tasks(context, user_profile)
            suggestions.extend(context_tasks)
        
        # 4. Add some general task suggestions
        general_tasks = self._get_general_task_suggestions(user_profile)
        suggestions.extend(general_tasks)
        
        # Remove duplicates and limit suggestions
        unique_suggestions = []
        suggestion_texts = set()
        
        for suggestion in suggestions:
            if suggestion["text"] not in suggestion_texts:
                suggestion_texts.add(suggestion["text"])
                unique_suggestions.append(suggestion)
                
                # Limit to 10 suggestions
                if len(unique_suggestions) >= 10:
                    break
        
        return unique_suggestions
    
    def _get_user_profile(self, user_id):
        """Get or create a user profile with preferences and patterns"""
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]
        
        # Create a new user profile with defaults
        profile = {
            "user_id": user_id,
            "preferred_categories": ["Email", "Meeting", "Personal"],
            "day_patterns": {
                0: ["Meeting", "Planning"],  # Monday
                1: ["Development", "Email"],  # Tuesday
                2: ["Meeting", "Development"],  # Wednesday
                3: ["Development", "Testing"],  # Thursday
                4: ["Report", "Email"],  # Friday
                5: ["Personal"],  # Saturday
                6: ["Personal"]   # Sunday
            },
            "time_patterns": {
                "morning": ["Email", "Planning"],
                "midday": ["Meeting", "Development"],
                "afternoon": ["Development", "Review"],
                "evening": ["Personal", "Email"]
            },
            "task_history": []
        }
        
        self.user_profiles[user_id] = profile
        return profile
    
    def _get_day_specific_tasks(self, day_of_week, user_profile):
        """Get tasks specific to the current day of the week"""
        suggestions = []
        
        # Get preferred categories for this day
        day_categories = user_profile["day_patterns"].get(day_of_week, [])
        
        for category in day_categories:
            if category in self.sample_tasks:
                tasks = self.sample_tasks[category]
                for task in tasks[:2]:  # Limit to 2 tasks per category
                    suggestions.append({
                        "text": task,
                        "category": category,
                        "reason": f"This is a common {category.lower()} task for you on {self._day_name(day_of_week)}",
                        "confidence": 0.8
                    })
        
        return suggestions
    
    def _get_time_specific_tasks(self, hour_of_day, user_profile):
        """Get tasks specific to the current time of day"""
        suggestions = []
        
        # Determine time of day
        time_of_day = "morning"
        if 12 <= hour_of_day < 15:
            time_of_day = "midday"
        elif 15 <= hour_of_day < 18:
            time_of_day = "afternoon"
        elif hour_of_day >= 18:
            time_of_day = "evening"
        
        # Get preferred categories for this time
        time_categories = user_profile["time_patterns"].get(time_of_day, [])
        
        for category in time_categories:
            if category in self.sample_tasks:
                tasks = self.sample_tasks[category]
                for task in tasks[:1]:  # Limit to 1 task per category
                    suggestions.append({
                        "text": task,
                        "category": category,
                        "reason": f"You often do {category.lower()} tasks during the {time_of_day}",
                        "confidence": 0.75
                    })
        
        return suggestions
    
    def _get_context_specific_tasks(self, context, user_profile):
        """Get tasks specific to the current context (e.g., project, mood)"""
        suggestions = []
        
        # Handle different types of context
        if "project" in context:
            project = context["project"]
            suggestions.append({
                "text": f"Work on {project} tasks",
                "category": "Development",
                "reason": f"Based on your current project: {project}",
                "confidence": 0.9
            })
        
        if "mood" in context:
            mood = context["mood"]
            if mood.lower() in ["tired", "stressed", "exhausted"]:
                suggestions.append({
                    "text": "Take a short break",
                    "category": "Personal",
                    "reason": f"Based on your current mood: {mood}",
                    "confidence": 0.85
                })
            elif mood.lower() in ["focused", "energetic", "productive"]:
                suggestions.append({
                    "text": "Work on high-priority tasks",
                    "category": "Development",
                    "reason": f"You seem {mood}, a good time for important work",
                    "confidence": 0.85
                })
        
        return suggestions
    
    def _get_general_task_suggestions(self, user_profile):
        """Get general task suggestions based on user preferences"""
        suggestions = []
        
        for category in user_profile["preferred_categories"]:
            if category in self.sample_tasks:
                tasks = self.sample_tasks[category]
                for task in tasks[:2]:  # Limit to 2 tasks per category
                    suggestions.append({
                        "text": task,
                        "category": category,
                        "reason": f"Based on your preference for {category.lower()} tasks",
                        "confidence": 0.6
                    })
        
        return suggestions
    
    def _day_name(self, day_of_week):
        """Convert day number to name"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[day_of_week] 