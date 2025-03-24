from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from sqlalchemy import and_, between
from models import Habit, HabitProgress, db
from datetime import datetime, timedelta

habit_progress_bp = Blueprint('habit_progress', __name__)

@habit_progress_bp.route('/<int:habit_id>', methods=['GET'])
@jwt_required()
def get_habit_progress(habit_id):
    """Get progress for a specific habit"""
    try:
        user_id = get_jwt_identity()
        
        # Check if habit exists and belongs to user
        habit = Habit.query.get(habit_id)
        if not habit:
            raise NotFound('Habit not found')
        if habit.userId != user_id:
            raise Forbidden('Not authorized to access this habit')
        
        # Get date range from query parameters
        start_date_str = request.args.get('startDate')
        end_date_str = request.args.get('endDate')
        
        # Default to last 30 days if no dates provided
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=30)
        
        if start_date_str:
            start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00')).date()
        if end_date_str:
            end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00')).date()
        
        # Query progress records within date range
        progress = HabitProgress.query.filter(
            and_(
                HabitProgress.habitId == habit_id,
                HabitProgress.date.between(start_date, end_date)
            )
        ).order_by(HabitProgress.date).all()
        
        return jsonify([p.to_dict() for p in progress])
    except (NotFound, Forbidden) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e) or 'Server error'}), 500

@habit_progress_bp.route('/<int:habit_id>', methods=['POST'])
@jwt_required()
def add_habit_progress(habit_id):
    """Add or update progress for a habit"""
    try:
        user_id = get_jwt_identity()
        
        # Check if habit exists and belongs to user
        habit = Habit.query.get(habit_id)
        if not habit:
            raise NotFound('Habit not found')
        if habit.userId != user_id:
            raise Forbidden('Not authorized to update this habit')
        
        data = request.json
        if not data:
            raise BadRequest('Request body is required')
        
        # Get date from request or default to today
        date_str = data.get('date')
        progress_date = datetime.utcnow().date()
        if date_str:
            progress_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
        
        # Check if progress already exists for this date
        existing_progress = HabitProgress.query.filter(
            and_(
                HabitProgress.habitId == habit_id,
                HabitProgress.date == progress_date
            )
        ).first()
        
        if existing_progress:
            # Update existing progress
            existing_progress.value = data.get('value', existing_progress.value)
            existing_progress.notes = data.get('notes', existing_progress.notes)
            db.session.commit()
            return jsonify(existing_progress.to_dict())
        else:
            # Create new progress entry
            progress = HabitProgress(
                habitId=habit_id,
                date=progress_date,
                value=data.get('value', 0),
                notes=data.get('notes')
            )
            
            db.session.add(progress)
            db.session.commit()
            return jsonify(progress.to_dict()), 201
    except (BadRequest, NotFound, Forbidden) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e) or 'Server error'}), 500

@habit_progress_bp.route('/<int:progress_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_habit_progress(progress_id):
    """Delete a habit progress entry"""
    try:
        user_id = get_jwt_identity()
        
        # Get the progress record
        progress = HabitProgress.query.get(progress_id)
        if not progress:
            raise NotFound('Progress record not found')
        
        # Check if the associated habit belongs to the user
        habit = Habit.query.get(progress.habitId)
        if not habit or habit.userId != user_id:
            raise Forbidden('Not authorized to delete this progress record')
        
        db.session.delete(progress)
        db.session.commit()
        
        return jsonify({'message': 'Progress record deleted successfully'})
    except (NotFound, Forbidden) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e) or 'Server error'}), 500 