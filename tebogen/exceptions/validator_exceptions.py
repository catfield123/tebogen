"""
Exceptions related to validators.

This module contains exceptions related to validators, such as attempting to add
a validator with a name that already exists.

"""


class ValidatorAlreadyExists(Exception):
    def __init__(self, name):
        """
        Initialize a ValidatorAlreadyExists exception.

        Args:
            name (str): The name of the validator that already exists.
        """
        self.name = name
        super().__init__(f"Validator '{name}' already exists.")
