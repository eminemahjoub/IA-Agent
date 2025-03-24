from datetime import datetime
from .db import db

class Habit(db.Model):
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), default='daily')  # daily, weekly, monthly
    target = db.Column(db.Float, default=1.0)
    unit = db.Column(db.String(50), nullable=True)
    reminderTime = db.Column(db.Time, nullable=True)
    color = db.Column(db.String(20), default='#3f51b5')
    icon = db.Column(db.String(50), default='star')
    startDate = db.Column(db.Date, default=datetime.utcnow().date)
    endDate = db.Column(db.Date, nullable=True)
    active = db.Column(db.Boolean, default=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('HabitProgress', backref='habit', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, name, userId, **kwargs):
        self.name = name
        self.userId = userId
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        """Convert the habit object to a dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'target': self.target,
            'unit': self.unit,
            'reminderTime': self.reminderTime.isoformat() if self.reminderTime else None,
            'color': self.color,
            'icon': self.icon,
            'startDate': self.startDate.isoformat() if self.startDate else None,
            'endDate': self.endDate.isoformat() if self.endDate else None,
            'active': self.active,
            'userId': self.userId,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None
        } 