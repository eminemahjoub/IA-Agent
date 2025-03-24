from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from werkzeug.exceptions import Unauthorized, Forbidden

def admin_required(fn):
    """
    Decorator to check if the authenticated user is an admin
    To be used in conjunction with jwt_required
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        # Here you would check if the user has admin role
        # For now, we just check a specific user ID
        # Replace this with your admin check logic
        if user_id != 1:  # Example: user with ID 1 is admin
            raise Forbidden("Admin privileges required")
        return fn(*args, **kwargs)
    return wrapper

def extract_token_from_header():
    """
    Extract JWT token from the Authorization header
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    parts = auth_header.split()
    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return None
    
    return parts[1] 