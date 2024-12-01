class NotValidPythonVariableNameException(Exception):
    def __init__(self, message=None, details=None):
        super().__init__(message)
        self.details = details


class PythonKeywordException(Exception):
    def __init__(self, message=None, details=None):
        super().__init__(message)
        self.details = details
