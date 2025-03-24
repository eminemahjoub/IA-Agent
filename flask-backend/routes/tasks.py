from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from sqlalchemy import desc
from models import Task, db
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    """Get all tasks for the authenticated user"""
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        completed = request.args.get('completed')
        priority = request.args.get('priority')
        category = request.args.get('category')
        
        # Build query
        query = Task.query.filter_by(userId=user_id)
        
        # Apply filters if provided
        if completed is not None:
            query = query.filter_by(completed=(completed.lower() == 'true'))
        if priority:
            query = query.filter_by(priority=priority)
        if category:
            query = query.filter_by(category=category)
        
        # Order by due date, with null values at the end
        tasks = query.order_by(Task.dueDate.asc().nullslast()).all()
        
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        return jsonify({'error': str(e) or 'Server error'}), 500

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    """Create a new task"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        if not data or not data.get('title'):
            raise BadRequest('Title is required')
        
        # Create task
        task = Task(
            title=data['title'],
            userId=user_id,
            description=data.get('description'),
            priority=data.get('priority', 'medium'),
            category=data.get('category')
        )
        
        # Parse date fields
        if data.get('dueDate'):
            task.dueDate = datetime.fromisoformat(data['dueDate'].replace('Z', '+00:00'))
        if data.get('reminder'):
            task.reminder = datetime.fromisoformat(data['reminder'].replace('Z', '+00:00'))
        
        # Save to database
        db.session.add(task)
        db.session.commit()
        
        return jsonify(task.to_dict()), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e) or 'Server error'}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Get a specific task"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.get(task_id)
        
        if not task:
            raise NotFound('Task not found')
        
        # Check ownership
        if task.userId != user_id:
            raise Forbidden('Not authorized to access this task')
        
        return jsonify(task.to_dict())
    except (NotFound, Forbidden) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e) or 'Server error'}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Update a task"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.get(task_id)
        
        if not task:
            raise NotFound('Task not found')
        
        # Check ownership
        if task.userId != user_id:
            raise Forbidden('Not authorized to update this task')
        
        data = request.json
        if not data:
            raise BadRequest('Request body is required')
        
        # Update fields
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']
        if 'priority' in data:
            task.priority = data['priority']
        if 'category' in data:
            task.category = data['category']
        if 'dueDate' in data:
            task.dueDate = datetime.fromisoformat(data['dueDate'].replace('Z', '+00:00')) if data['dueDate'] else None
        if 'reminder' in data:
            task.reminder = datetime.fromisoformat(data['reminder'].replace('Z', '+00:00')) if data['reminder'] else None
        
        db.session.commit()
        return jsonify(task.to_dict())
    except (BadRequest, NotFound, Forbidden) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e) or 'Server error'}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a task"""
    try:
        user_id = get_jwt_identity()
        task = Task.query.get(task_id)
        
        if not task:
            raise NotFound('Task not found')
        
        # Check ownership
        if task.userId != user_id:
            raise Forbidden('Not authorized to delete this task')
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'})
    except (NotFound, Forbidden) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e) or 'Server error'}), 500 