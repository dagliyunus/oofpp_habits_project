from datetime import datetime


def validate_datetime(date_string):
    """
    Validates a datetime string in the format 'YYYY-MM-DD HH:MM'.
    Parameters:
        date_string (str): The input string representing date and time.
    Returns:
        datetime: A datetime object parsed from the input string.
    Raises:
        ValueError: If the input string does not match the expected format.
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d %H:%M")
    except ValueError as e:
        raise ValueError("❌ Invalid date format. Use 'YYYY-MM-DD HH:MM'") from e


def validate_frequency(value):
    """
    Validates that the frequency value is either 'daily' or 'weekly'.
    Parameters:
        value (str): The input frequency value.
    Returns:
        str: The validated frequency string.
    Raises:
        ValueError: If the input value is not 'daily' or 'weekly'.
    """
    if value not in ["daily", "weekly"]:
        raise ValueError("❌ Frequency must be 'daily' or 'weekly'")
    return value


def is_valid_user_id(user_id):
    """
    Validates that the user ID is a positive integer.
    Parameters:
        user_id (int): The user ID to validate.
    Returns:
        bool: True if the user ID is valid.
    Raises:
        ValueError: If the user ID is not a positive integer.
    """
    if not isinstance(user_id, int) or user_id < 1:
        raise ValueError("❌ Invalid User ID. Must be a positive integer.")
    return True