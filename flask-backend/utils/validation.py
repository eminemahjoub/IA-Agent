import re
from datetime import datetime

def validate_email(email):
    """
    Validate email format
    
    Args:
        email (str): Email to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
    
    # Simple regex for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present in the data
    
    Args:
        data (dict): Data to validate
        required_fields (list): List of required field names
        
    Returns:
        tuple: (is_valid, missing_fields)
    """
    if not data or not required_fields:
        return False, required_fields
    
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    return len(missing_fields) == 0, missing_fields

def validate_string_length(value, min_length=1, max_length=None):
    """
    Validate string length
    
    Args:
        value (str): String to validate
        min_length (int): Minimum length
        max_length (int, optional): Maximum length
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    if len(value) < min_length:
        return False
    
    if max_length is not None and len(value) > max_length:
        return False
    
    return True

def validate_date_format(date_str, formats=['%Y-%m-%d']):
    """
    Validate date string format
    
    Args:
        date_str (str): Date string to validate
        formats (list): List of valid date formats
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not date_str:
        return False
    
    for format_str in formats:
        try:
            datetime.strptime(date_str, format_str)
            return True
        except ValueError:
            continue
    
    return False

def validate_integer_range(value, min_value=None, max_value=None):
    """
    Validate integer range
    
    Args:
        value: Value to validate
        min_value (int, optional): Minimum value
        max_value (int, optional): Maximum value
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        num = int(value)
        
        if min_value is not None and num < min_value:
            return False
        
        if max_value is not None and num > max_value:
            return False
        
        return True
    except (ValueError, TypeError):
        return False

def validate_password_strength(password):
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Check for uppercase, lowercase, digit, and special character
    if not re.search(r'[A-Z]', password):
        return False, "Password must include at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must include at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must include at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must include at least one special character"
    
    return True, "Password is strong"

def sanitize_string(value):
    """
    Sanitize string by removing HTML tags and script elements
    
    Args:
        value (str): String to sanitize
        
    Returns:
        str: Sanitized string
    """
    if not value:
        return value
    
    # Remove HTML tags
    value = re.sub(r'<[^>]*>', '', value)
    
    # Remove script tags and their contents
    value = re.sub(r'<script.*?</script>', '', value, flags=re.DOTALL)
    
    return value 