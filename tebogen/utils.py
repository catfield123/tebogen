"""
Utilities.

This module contains utility functions.

"""

import keyword
import re

from tebogen.exceptions.common import (
    NotValidPythonVariableNameException,
    PythonKeywordException,
)


def is_valid_python_variable_name(name: str) -> bool:
    """
    Checks if the given name is a valid Python variable name.

    Args:
        name (str): The name to check.

    Returns:
        bool: True if the name is a valid Python variable name, False otherwise.
    """
    if not re.match(r"^[^\W\d]\w*$", name):
        raise NotValidPythonVariableNameException

    if keyword.iskeyword(name):
        raise PythonKeywordException

    return True
