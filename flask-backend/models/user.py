import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from sqlalchemy.dialects.mysql import JSON
from .db import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    googleCalendarToken = db.Column(db.String(500), nullable=True)
    outlookToken = db.Column(db.String(500), nullable=True)
    emailSettings = db.Column(JSON, default={
        "service": None,
        "connected": False,
        "token": None
    })
    focusSettings = db.Column(JSON, default={
        "workDuration": 25,
        "breakDuration": 5,
        "longBreakDuration": 15,
        "longBreakInterval": 4
    })
    habitSettings = db.Column(JSON, default={
        "reminderTime": None,
        "trackingEnabled": True
    })
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='user', lazy=True, cascade="all, delete-orphan")
    habits = db.relationship('Habit', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, name, email, password, **kwargs):
        self.name = name
        self.email = email
        self.password = self._hash_password(password)
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def _hash_password(self, password):
        """Hash the password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if the password matches the hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def get_token(self):
        """Generate a JWT token for the user"""
        expiration = datetime.utcnow() + timedelta(days=30)
        payload = {
            'exp': expiration,
            'iat': datetime.utcnow(),
            'sub': self.id
        }
        token = jwt.encode(
            payload,
            os.getenv('JWT_SECRET'),
            algorithm='HS256'
        )
        return token
    
    @staticmethod
    def verify_token(token):
        """Verify a JWT token and return the user ID"""
        try:
            payload = jwt.decode(
                token,
                os.getenv('JWT_SECRET'),
                algorithms=['HS256']
            )
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token
    
    def to_dict(self, exclude_password=True):
        """Convert the user object to a dictionary"""
        user_dict = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'googleCalendarToken': self.googleCalendarToken,
            'outlookToken': self.outlookToken,
            'emailSettings': self.emailSettings,
            'focusSettings': self.focusSettings,
            'habitSettings': self.habitSettings,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None,
        }
        if not exclude_password:
            user_dict['password'] = self.password
        return user_dict 