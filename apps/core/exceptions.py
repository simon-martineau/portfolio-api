
class AlreadyExistsException(Exception):
    """Exception for when a unique field value already exists"""


class IllegalCallException(Exception):
    """Exception for a function call that should not have been made"""
