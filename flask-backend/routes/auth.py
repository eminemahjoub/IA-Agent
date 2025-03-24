from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from models import User, db
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return a token"""
    try:
        data = request.json
        if not data or not data.get('email') or not data.get('password'):
            raise BadRequest('Email and password are required')
        
        # Find the user by email
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            raise Unauthorized('Invalid credentials')
        
        # Check if the password is correct
        if not user.check_password(data['password']):
            raise Unauthorized('Invalid credentials')
        
        # Create token with 30 days expiry
        expires = datetime.timedelta(days=30)
        token = create_access_token(identity=user.id, expires_delta=expires)
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        })
    except (BadRequest, Unauthorized) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e) or 'Server error'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    """Get the current logged in user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            raise NotFound('User not found')
        
        return jsonify(user.to_dict())
    except NotFound as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        return jsonify({'error': str(e) or 'Server error'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        if not data:
            raise BadRequest('Request body is required')
        
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                raise BadRequest(f'{field} is required')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            raise BadRequest('User already exists with that email')
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        # Create token
        expires = datetime.timedelta(days=30)
        token = create_access_token(identity=user.id, expires_delta=expires)
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e) or 'Server error'}), 500

@auth_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            raise NotFound('User not found')
        
        data = request.json
        if not data:
            raise BadRequest('Request body is required')
        
        # Update user fields
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            # Check if email already exists
            if data['email'] != user.email:
                existing_user = User.query.filter_by(email=data['email']).first()
                if existing_user:
                    raise BadRequest('Email already in use')
            user.email = data['email']
        if 'password' in data and data['password']:
            user.password = user._hash_password(data['password'])
        
        # Update settings if provided
        if 'focusSettings' in data:
            user.focusSettings = data['focusSettings']
        if 'habitSettings' in data:
            user.habitSettings = data['habitSettings']
        if 'emailSettings' in data:
            user.emailSettings = data['emailSettings']
        
        db.session.commit()
        return jsonify(user.to_dict())
    except (BadRequest, NotFound) as e:
        return jsonify({'error': str(e)}), e.code
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e) or 'Server error'}), 500 