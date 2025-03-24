from datetime import datetime
from .db import db

class HabitProgress(db.Model):
    __tablename__ = 'habit_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    habitId = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    value = db.Column(db.Float, default=0)
    notes = db.Column(db.Text, nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, habitId, date=None, **kwargs):
        self.habitId = habitId
        self.date = date if date else datetime.utcnow().date()
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        """Convert the habit progress object to a dictionary"""
        return {
            'id': self.id,
            'habitId': self.habitId,
            'date': self.date.isoformat() if self.date else None,
            'value': self.value,
            'notes': self.notes,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None
        }
    
    # Add a unique constraint to prevent duplicate entries for the same habit and date
    __table_args__ = (
        db.UniqueConstraint('habitId', 'date', name='uq_habit_progress_habitId_date'),
    ) 