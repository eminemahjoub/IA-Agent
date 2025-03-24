from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from sqlalchemy import desc
from models import Habit, db
from datetime import datetime, time

habits_bp = Blueprint('habits', __name__)

@habits_bp.route('/', methods=['GET'])
@jwt_required()
def get_habits():
    """Get all habits for the authenticated user"""
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        active = request.args.get('active')
        type = request.args.get('type')
        
        # Build query
        query = Habit.query.filter_by(userId=user_id)
        
        # Apply filters if provided
        if active is not None:
            query = query.filter_by(active=(active.lower() == 'true'))
        if type:
            query = query.filter_by(type=type)
        
        # Order by creation date, newest first
        habits = query.order_by(Habit.createdAt.desc()).all()
        
        return jsonify([habit.to_dict() for habit in habits])
    except Exception as e:
        return jsonify({'error': str(e) or 'Server error'}), 500

@habits_bp.route('/', methods=['POST'])
@jwt_required()
def create_habit():
    """Create a new habit"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        if not data or not data.get('name'):
            raise BadRequest('Habit name is required')
        
        # Create habit
        habit = Habit(
            name=data['name'],
            userId=user_id,
            description=data.get('description'),
            type=data.get('type', 'daily'),
            target=data.get('target', 1.0),
            unit=data.get('unit'),
            color=data.get('color', '#3f51b5'),
            icon=data.get('icon', 'star')
        )
        
        # Parse date fields
        if data.get('startDate'):
            habit.startDate = datetime.fromisoformat(data['startDate'].replace('Z', '+00:00')).date()
        if data.get('endDate'):
            habit.endDate = datetime.fromisoformat(data['endDate'].replace('Z', '+00:00')).date()
        
        # Parse time fields
        if data.get('reminderTime'):
            habit.reminderTime = time.fromisoformat(data['reminderTime'])
        
        # Save to database
        db.session.add(habit)
        db.session.commit()
        
        return jsonify(habit.to_dict()), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e) or 'Server error'}), 500

@habits_bp.route('/<int:habit_id>', methods=['GET'])
@jwt_required()
def get_habit(habit_id):
    """Get a specific habit"""
    try:
        user_id = get_jwt_identity()
        habit = Habit.query.get(habit_id)
        
        if not habit:
            raise NotFound('Habit not found')
        
        # Check ownership
        if habit.userId != user_id:
            raise Forbidden('Not authorized to access this habit')
        
        return jsonify(habit.to_dict())
    except (NotFound, Forbidden) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e) or 'Server error'}), 500

@habits_bp.route('/<int:habit_id>', methods=['PUT'])
@jwt_required()
def update_habit(habit_id):
    """Update a habit"""
    try:
        user_id = get_jwt_identity()
        habit = Habit.query.get(habit_id)
        
        if not habit:
            raise NotFound('Habit not found')
        
        # Check ownership
        if habit.userId != user_id:
            raise Forbidden('Not authorized to update this habit')
        
        data = request.json
        if not data:
            raise BadRequest('Request body is required')
        
        # Update fields
        if 'name' in data:
            habit.name = data['name']
        if 'description' in data:
            habit.description = data['description']
        if 'type' in data:
            habit.type = data['type']
        if 'target' in data:
            habit.target = data['target']
        if 'unit' in data:
            habit.unit = data['unit']
        if 'color' in data:
            habit.color = data['color']
        if 'icon' in data:
            habit.icon = data['icon']
        if 'active' in data:
            habit.active = data['active']
        
        # Parse date fields
        if 'startDate' in data:
            habit.startDate = datetime.fromisoformat(data['startDate'].replace('Z', '+00:00')).date() if data['startDate'] else None
        if 'endDate' in data:
            habit.endDate = datetime.fromisoformat(data['endDate'].replace('Z', '+00:00')).date() if data['endDate'] else None
        
        # Parse time fields
        if 'reminderTime' in data:
            habit.reminderTime = time.fromisoformat(data['reminderTime']) if data['reminderTime'] else None
        
        db.session.commit()
        return jsonify(habit.to_dict())
    except (BadRequest, NotFound, Forbidden) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e) or 'Server error'}), 500

@habits_bp.route('/<int:habit_id>', methods=['DELETE'])
@jwt_required()
def delete_habit(habit_id):
    """Delete a habit"""
    try:
        user_id = get_jwt_identity()
        habit = Habit.query.get(habit_id)
        
        if not habit:
            raise NotFound('Habit not found')
        
        # Check ownership
        if habit.userId != user_id:
            raise Forbidden('Not authorized to delete this habit')
        
        db.session.delete(habit)
        db.session.commit()
        
        return jsonify({'message': 'Habit deleted successfully'})
    except (NotFound, Forbidden) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e) or 'Server error'}), 500 