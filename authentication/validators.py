import re


def is_password_valid(password):
    """Password validation

    Args:
        password (str): user potential password

    Returns:
        bool: returns True if password is valid else False
    """
    # pattern meaning: password should contains
    #   at least 1 char
    #   at least 1 number
    #   at least length >= 6
    pattern = r'(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'
    if not re.match(pattern, password):
        return False
    return True
