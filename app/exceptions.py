"""Custom exception classes"""

class PasswordException(Exception):
    """Exception raised when a password related error occurs"""
    def __init__(self, message):
        return super(PasswordException, self).__init__(message)


class ActionForbiddenException(Exception):
    """Exception to be raised when a user can not perform an action"""
    def __init__(self, message):
        return super(ActionForbiddenException, self).__init__(message)
