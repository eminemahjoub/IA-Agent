from datetime import datetime, timedelta
import re

def parse_date_string(date_str):
    """
    Parse a date string in various formats to a datetime object
    
    Args:
        date_str (str): Date string in various formats
        
    Returns:
        datetime: Parsed datetime object or None if parsing fails
    """
    try:
        # Try ISO format (YYYY-MM-DD)
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return datetime.strptime(date_str, '%Y-%m-%d')
        
        # Try ISO format with time (YYYY-MM-DDThh:mm:ss)
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?$', date_str):
            if date_str.count(':') == 1:
                return datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
            
        # Try other common formats
        formats = [
            '%d/%m/%Y',  # DD/MM/YYYY
            '%m/%d/%Y',  # MM/DD/YYYY
            '%d-%m-%Y',  # DD-MM-YYYY
            '%m-%d-%Y',  # MM-DD-YYYY
            '%d %b %Y',  # DD Mon YYYY
            '%d %B %Y',  # DD Month YYYY
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # Handle relative date strings
        date_str = date_str.lower()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if date_str == 'today':
            return today
        elif date_str == 'tomorrow':
            return today + timedelta(days=1)
        elif date_str == 'yesterday':
            return today - timedelta(days=1)
        elif 'days ago' in date_str:
            days = int(re.search(r'(\d+) days ago', date_str).group(1))
            return today - timedelta(days=days)
        elif 'next week' in date_str:
            return today + timedelta(days=7)
        elif 'last week' in date_str:
            return today - timedelta(days=7)
        
        # If we get here, we couldn't parse the date
        return None
    except Exception as e:
        print(f"Error parsing date: {str(e)}")
        return None

def get_date_range(start_date, end_date=None):
    """
    Get a date range between two dates
    
    Args:
        start_date (datetime): Start date
        end_date (datetime, optional): End date. If None, uses today
        
    Returns:
        list: List of dates in the range
    """
    if not start_date:
        return []
    
    if end_date is None:
        end_date = datetime.now()
    
    if isinstance(start_date, str):
        start_date = parse_date_string(start_date)
    
    if isinstance(end_date, str):
        end_date = parse_date_string(end_date)
    
    if not start_date or not end_date:
        return []
    
    # Ensure start_date is earlier than end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    # Create date range
    date_range = []
    current_date = start_date
    
    while current_date <= end_date:
        date_range.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    
    return date_range

def format_date(date_obj, format_str='%Y-%m-%d'):
    """
    Format a datetime object to a string
    
    Args:
        date_obj (datetime): Date object to format
        format_str (str): Format string
        
    Returns:
        str: Formatted date string
    """
    if not date_obj:
        return None
    
    if isinstance(date_obj, str):
        date_obj = parse_date_string(date_obj)
        if not date_obj:
            return None
    
    try:
        return date_obj.strftime(format_str)
    except Exception as e:
        print(f"Error formatting date: {str(e)}")
        return None 