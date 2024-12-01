"""
This module defines custom exceptions related to question group list operations.

The exceptions are used to handle specific error conditions that may arise
when manipulating questions and groups within a QuestionGroupList. These 
exceptions provide meaningful error messages to help identify the nature 
of the error and facilitate debugging.

Classes:
    BoundaryReachedException: Raised when an attempt is made to move a 
                              question or group beyond the boundaries 
                              of a list or group.
"""


class BoundaryReachedException(Exception):
    def __init__(self):
        """
        Initializes the BoundaryReachedException with a default message.

        This exception is raised when an attempt is made to move a question or group
        beyond the boundaries of a list or group where no further movement is possible.
        """
        super().__init__("Boundary reached.")
