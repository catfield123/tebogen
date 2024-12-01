"""
Exceptions raised by the application.

This module contains the exceptions that are raised by the application when
invalid input is provided.

"""


class NotValidPythonVariableNameException(Exception):
    def __init__(self, message=None, details=None):
        """
        Initializes a NotValidPythonVariableNameException.

        Args:
            message (str): The exception message.
            details (dict): Additional details about the exception.
        """
        super().__init__(message)
        self.details = details


class PythonKeywordException(Exception):
    def __init__(self, message=None, details=None):
        """
        Initializes a PythonKeywordException.

        Args:
            message (str): The message for the exception.
            details (dict): Additional details for the exception.
        """
        super().__init__(message)
        self.details = details
