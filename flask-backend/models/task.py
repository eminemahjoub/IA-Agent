from datetime import datetime
from .db import db

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    dueDate = db.Column(db.DateTime, nullable=True)
    reminder = db.Column(db.DateTime, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, title, userId, **kwargs):
        self.title = title
        self.userId = userId
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        """Convert the task object to a dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'dueDate': self.dueDate.isoformat() if self.dueDate else None,
            'reminder': self.reminder.isoformat() if self.reminder else None,
            'category': self.category,
            'userId': self.userId,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None
        } 