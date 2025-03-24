import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from collections import defaultdict

class MLPredictor:
    """Service for machine learning-based predictions and suggestions"""
    
    def __init__(self):
        """Initialize the ML predictor"""
        try:
            # Task categories
            self.task_categories = {
                'work': [
                    "Review {document} report",
                    "Schedule meeting with {person}",
                    "Prepare presentation for {project}",
                    "Follow up on {project} project",
                    "Update {document} documentation",
                    "Complete {project} tasks",
                    "Respond to emails about {project}",
                    "Call {person} regarding {project}",
                    "Review budget for {project}",
                    "Submit expense report"
                ],
                'personal': [
                    "Call {person}",
                    "Buy {item} from grocery store",
                    "Pay {bill} bill",
                    "Schedule appointment with {person}",
                    "Plan weekend activities",
                    "Buy gift for {person}'s birthday",
                    "Organize {room} closet",
                    "Research {topic} online",
                    "Renew {document} subscription",
                    "Check in with {person}"
                ],
                'health': [
                    "Go for a {duration} run",
                    "Schedule {type} doctor appointment",
                    "Take medication",
                    "Drink water",
                    "Prepare healthy meals",
                    "Go to gym",
                    "Do {duration} yoga session",
                    "Meditate for {duration}",
                    "Get {duration} of sleep",
                    "Track daily water intake"
                ],
                'learning': [
                    "Study {topic} for {duration}",
                    "Take online course on {topic}",
                    "Read {book} book",
                    "Watch tutorial on {topic}",
                    "Practice {skill} for {duration}",
                    "Review notes on {topic}",
                    "Research {topic} online",
                    "Attend webinar on {topic}",
                    "Complete {topic} assignment",
                    "Learn about {topic}"
                ],
                'home': [
                    "Clean {room}",
                    "Do laundry",
                    "Wash dishes",
                    "Water plants",
                    "Take out trash",
                    "Vacuum {room}",
                    "Fix {item} in {room}",
                    "Organize {room}",
                    "Mow lawn",
                    "Pick up groceries"
                ]
            }
            
            # Day-specific tasks
            self.day_specific_tasks = {
                'Monday': [
                    "Plan weekly goals",
                    "Review weekly schedule",
                    "Check emails from weekend",
                    "Follow up on pending items",
                    "Team meeting preparation"
                ],
                'Tuesday': [
                    "Follow up on Monday's meetings",
                    "Continue work on weekly goals",
                    "Mid-week planning check-in",
                    "Send progress updates"
                ],
                'Wednesday': [
                    "Mid-week review",
                    "Check in on weekly goals progress",
                    "Organize workspace",
                    "Follow up on ongoing projects"
                ],
                'Thursday': [
                    "Prepare for Friday's meetings",
                    "Follow up on pending responses",
                    "Begin preparing weekly summary",
                    "Finalize remaining weekly deliverables"
                ],
                'Friday': [
                    "Submit weekly report",
                    "Plan for next week",
                    "Clear inbox before weekend",
                    "Review weekly accomplishments",
                    "Set Monday priorities"
                ],
                'Saturday': [
                    "Weekly grocery shopping",
                    "Home cleaning",
                    "Personal errands",
                    "Relax and recharge",
                    "Social activities"
                ],
                'Sunday': [
                    "Prepare meals for the week",
                    "Review calendar for upcoming week",
                    "Set goals for the week",
                    "Rest and recharge",
                    "Light organization for the week ahead"
                ]
            }
            
            # Time-specific tasks
            self.time_specific_tasks = {
                'morning': [
                    "Check emails",
                    "Review daily schedule",
                    "Set daily priorities",
                    "Morning exercise",
                    "Team stand-up meeting",
                    "Respond to urgent messages"
                ],
                'afternoon': [
                    "Follow up on morning tasks",
                    "Work on primary projects",
                    "Check-in with team members",
                    "Schedule for tomorrow",
                    "Return phone calls",
                    "Afternoon break and stretching"
                ],
                'evening': [
                    "Wrap up daily tasks",
                    "Prepare for tomorrow",
                    "Review accomplishments",
                    "Evening exercise",
                    "Personal reading time",
                    "Relaxation activities"
                ]
            }
            
            # User profiles (would typically be stored in a database)
            self.user_profiles = defaultdict(lambda: {
                'preferred_categories': ['work', 'personal', 'health'],
                'common_tasks': [
                    "Check emails",
                    "Team meeting",
                    "Exercise",
                    "Read"
                ]
            })
            
            print("ML Predictor initialized successfully")
        except Exception as e:
            print(f"Error initializing ML Predictor: {str(e)}")
    
    def _get_time_of_day(self):
        """Get the current time of day category"""
        current_hour = datetime.datetime.now().hour
        if 5 <= current_hour < 12:
            return 'morning'
        elif 12 <= current_hour < 18:
            return 'afternoon'
        else:
            return 'evening'
    
    def _get_user_profile(self, user_id):
        """
        Get user profile based on user_id
        In a real implementation, this would fetch from database
        """
        return self.user_profiles[user_id]
    
    def suggest_tasks(self, user_id, context=None, count=5):
        """
        Suggest tasks based on user history, current context, and time patterns
        
        Args:
            user_id (str): User identifier
            context (dict): Additional context (location, current activity, etc.)
            count (int): Number of suggestions to return
            
        Returns:
            list: Suggested tasks
        """
        try:
            # Get user profile
            user_profile = self._get_user_profile(user_id)
            
            # Get current day and time
            current_day = datetime.datetime.now().strftime('%A')
            time_of_day = self._get_time_of_day()
            
            # Generate suggestions
            suggestions = []
            
            # Add day-specific tasks
            day_tasks = self._get_day_specific_tasks(current_day)
            suggestions.extend(day_tasks[:2])  # Add up to 2 day-specific tasks
            
            # Add time-specific tasks
            time_tasks = self._get_time_specific_tasks(time_of_day)
            suggestions.extend(time_tasks[:2])  # Add up to 2 time-specific tasks
            
            # Add category-specific tasks
            category_tasks = self._get_category_specific_tasks(user_profile)
            suggestions.extend(category_tasks[:3])  # Add up to 3 category-specific tasks
            
            # Add context-specific tasks if context is provided
            if context:
                context_tasks = self._get_context_specific_tasks(context)
                suggestions.extend(context_tasks[:2])  # Add up to 2 context-specific tasks
            
            # Ensure we have unique tasks
            unique_suggestions = list(dict.fromkeys(suggestions))
            
            # If we don't have enough unique suggestions, add some generic tasks
            if len(unique_suggestions) < count:
                generic_tasks = self._get_generic_tasks()
                unique_suggestions.extend([task for task in generic_tasks if task not in unique_suggestions])
            
            # Return the requested number of suggestions
            return unique_suggestions[:count]
        except Exception as e:
            print(f"Error suggesting tasks: {str(e)}")
            return ["Check email", "Review calendar", "Work on current project"]
    
    def _get_day_specific_tasks(self, day):
        """Get tasks specific to the given day"""
        if day in self.day_specific_tasks:
            return random.sample(self.day_specific_tasks[day], 
                                min(2, len(self.day_specific_tasks[day])))
        return []
    
    def _get_time_specific_tasks(self, time_of_day):
        """Get tasks specific to the time of day"""
        if time_of_day in self.time_specific_tasks:
            return random.sample(self.time_specific_tasks[time_of_day], 
                                min(2, len(self.time_specific_tasks[time_of_day])))
        return []
    
    def _get_category_specific_tasks(self, user_profile):
        """Get tasks from user's preferred categories"""
        preferred_categories = user_profile.get('preferred_categories', ['work', 'personal'])
        tasks = []
        
        for category in preferred_categories:
            if category in self.task_categories:
                # Select 1-2 random tasks from each preferred category
                category_tasks = random.sample(self.task_categories[category], 
                                             min(2, len(self.task_categories[category])))
                
                # Format task templates with placeholders
                formatted_tasks = []
                for task in category_tasks:
                    if '{' in task:
                        # Simple placeholder replacement
                        if '{document}' in task:
                            task = task.replace('{document}', random.choice(['quarterly', 'project', 'annual', 'budget']))
                        if '{person}' in task:
                            task = task.replace('{person}', random.choice(['team', 'manager', 'client', 'colleague']))
                        if '{project}' in task:
                            task = task.replace('{project}', random.choice(['marketing', 'development', 'research', 'design']))
                        if '{duration}' in task:
                            task = task.replace('{duration}', random.choice(['30 minute', '1 hour', '15 minute', '45 minute']))
                        if '{topic}' in task:
                            task = task.replace('{topic}', random.choice(['Python', 'marketing', 'project management', 'design']))
                        if '{type}' in task:
                            task = task.replace('{type}', random.choice(['dental', 'medical', 'therapy', 'wellness']))
                        if '{room}' in task:
                            task = task.replace('{room}', random.choice(['living room', 'bedroom', 'kitchen', 'office']))
                        if '{item}' in task:
                            task = task.replace('{item}', random.choice(['lamp', 'chair', 'table', 'appliance']))
                        if '{bill}' in task:
                            task = task.replace('{bill}', random.choice(['electric', 'water', 'internet', 'phone']))
                        if '{book}' in task:
                            task = task.replace('{book}', random.choice(['business', 'self-help', 'technical', 'novel']))
                        if '{skill}' in task:
                            task = task.replace('{skill}', random.choice(['coding', 'writing', 'drawing', 'language']))
                    
                    formatted_tasks.append(task)
                
                tasks.extend(formatted_tasks)
        
        return tasks
    
    def _get_context_specific_tasks(self, context):
        """Get tasks specific to user context"""
        context_tasks = []
        
        # Check location context
        if 'location' in context:
            location = context['location'].lower()
            
            if 'home' in location:
                context_tasks.extend([
                    "Organize your workspace", 
                    "Check home inventory", 
                    "Water plants"
                ])
            elif 'office' in location or 'work' in location:
                context_tasks.extend([
                    "Schedule team check-in", 
                    "Update project status", 
                    "Prepare for upcoming meetings"
                ])
            elif 'travel' in location or 'trip' in location:
                context_tasks.extend([
                    "Check travel itinerary", 
                    "Confirm reservations", 
                    "Pack essentials"
                ])
        
        # Check activity context
        if 'activity' in context:
            activity = context['activity'].lower()
            
            if 'working' in activity or 'focusing' in activity:
                context_tasks.extend([
                    "Take a short break",
                    "Drink water",
                    "Stretch for 5 minutes"
                ])
            elif 'meeting' in activity:
                context_tasks.extend([
                    "Follow up on action items",
                    "Send meeting notes",
                    "Schedule follow-up meeting if needed"
                ])
        
        return random.sample(context_tasks, min(len(context_tasks), 2)) if context_tasks else []
    
    def _get_generic_tasks(self):
        """Get generic productivity tasks"""
        generic_tasks = [
            "Check and respond to emails",
            "Review your calendar",
            "Update your to-do list",
            "Take a short break",
            "Drink water",
            "Stretch for 5 minutes",
            "Reflect on your progress",
            "Set goals for tomorrow",
            "Organize your workspace",
            "Review your goals",
            "Follow up on pending items",
            "Check in with team members",
            "Schedule important meetings",
            "Review project deadlines",
            "Back up important files"
        ]
        
        return random.sample(generic_tasks, 5) 