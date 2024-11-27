import re
import keyword


def is_valid_python_variable_name(name: str) -> bool:
    """
    Checks if the given name is a valid Python variable name.

    Args:
        name (str): The name to check.

    Returns:
        bool: True if the name is a valid Python variable name, False otherwise.
    """
    if not re.match(r"^[^\W\d]\w*$", name):
        raise ValueError(
            "variable_name must be a valid Python variable name. "
            "It should start with a letter or an underscore and contain only alphanumeric characters or underscores."
        )
    
    if keyword.iskeyword(name):
        raise ValueError(
            f"variable_name '{name}' is a reserved Python keyword and cannot be used as a variable name."
        )
    
    return True