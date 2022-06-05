
class PasswordException(Exception):
    def __init__(self, message):
        return super(PasswordException, self).__init__(message)

class ActionForbiddenException(Exception):
    def __init__(self, message):
        return super(ActionForbiddenException, self).__init__(message)