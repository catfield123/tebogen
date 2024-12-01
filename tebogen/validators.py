"""
Validators module.

This module contains various validators and related classes.

"""

from dataclasses import dataclass
from enum import Enum

from tebogen.exceptions.common import (
    NotValidPythonVariableNameException,
    PythonKeywordException,
)
from tebogen.exceptions.validator_exceptions import ValidatorAlreadyExists
from tebogen.utils import is_valid_python_variable_name


class DateFormatEnum(Enum):
    """
    An enumeration of the date formats that can be used for date validation.

    The enumeration contains the following date formats:

        - DD_MM_YYYY
        - MM_DD_YYYY
        - YYYY_MM_DD
        - DD_MM_YY
        - MM_DD_YY
        - YY_MM_DD

    The date formats are used to validate the input date string. The date formats
    are strings in the format "DD.MM.YYYY", "MM.DD.YYYY", "YYYY.MM.DD",
    "DD.MM.YY", "MM.DD.YY", "YY.MM.DD" respectively.
    """

    DD_MM_YYYY = "dd.mm.yyyy"
    MM_DD_YYYY = "mm.dd.yyyy"
    YYYY_MM_DD = "yyyy.mm.dd"
    DD_MM_YY = "dd.mm.yy"
    MM_DD_YY = "mm.dd.yy"
    YY_MM_DD = "yy.mm.dd"


@dataclass
class Validator:
    name: str

    def __eq__(self, value):
        if isinstance(value, Validator):
            return self.name == value.name
        if isinstance(value, str):
            return self.name == value
        return False

    def to_dict(self):
        """
        Converts the validator to a dictionary representation.

        The dictionary will contain the validator's name.

        Returns:
            dict: A dictionary representation of the validator.
        """
        return {"name": self.name}


@dataclass
class IntegerValidator(Validator):
    name = "integer_validator"
    min_value: int | None
    max_value: int | None

    def __init__(self, min_value: int | None = None, max_value: int | None = None):
        self.min_value = min_value
        self.max_value = max_value

    def to_dict(self):
        """
        Convert the IntegerValidator instance to a dictionary representation.

        This method returns a dictionary containing the name of the validator
        along with its minimum and maximum value constraints. The dictionary
        keys are "name", "min_value", and "max_value".

        Returns:
            dict: A dictionary representation of the IntegerValidator instance
            with the following structure:
                - "name": str, the name of the validator.
                - "min_value": int | None, the minimum value constraint or None if not set.
                - "max_value": int | None, the maximum value constraint or None if not set.
        """
        return {
            "name": self.name,
            "min_value": self.min_value,
            "max_value": self.max_value,
        }


@dataclass
class FloatValidator(Validator):
    name = "float_validator"
    min_value: float | None = None
    max_value: float | None = None

    def __init__(self, min_value: float | None = None, max_value: float | None = None):
        self.min_value = min_value
        self.max_value = max_value

    def to_dict(self):
        """
        Converts the validator to a dictionary representation.

        Returns:
            dict: A dictionary containing the validator name, min_value, and max_value.
        """
        return {
            "name": self.name,
            "min_value": self.min_value,
            "max_value": self.max_value,
        }


@dataclass
class TextValidator(Validator):
    name = "text_validator"
    min_length: int | None
    max_length: int | None

    def __init__(self, min_length: int | None = None, max_length: int | None = None):
        self.min_length = min_length
        self.max_length = max_length

    def to_dict(self):
        """
        Converts the text validator to a dictionary representation.

        The dictionary will contain the validator's name, minimum length,
        and maximum length.

        Returns:
            dict: A dictionary with the validator's name, min_length, and max_length.
        """
        return {
            "name": self.name,
            "min_length": self.min_length,
            "max_length": self.max_length,
        }


@dataclass
class DateValidator(Validator):
    name = "date_validator"
    date_format: DateFormatEnum

    def __init__(self, date_format: DateFormatEnum = DateFormatEnum.DD_MM_YYYY):
        self.date_format = date_format

    def to_dict(self):
        """
        Converts the validator to a dictionary representation.

        The dictionary will contain the validator's name and date_format.

        Returns:
            dict: A dictionary with the validator's name and date_format.
        """
        return {
            "name": self.name,
            "date_format": self.date_format.value,
        }


class EmailValidator(Validator):
    name = "email_validator"

    def __init__(self, *args, **kwargs):
        pass

    def to_dict(self):
        """
        Converts the validator to a dictionary representation.

        The dictionary will contain the validator's name.

        Returns:
            dict: A dictionary with the validator's name.
        """
        return {"name": self.name}


class PhoneNumberValidator(Validator):
    name = "phone_validator"

    def __init__(self, *args, **kwargs):
        pass

    def to_dict(self):
        """
        Converts the validator to a dictionary representation.

        The dictionary will contain the validator's name.

        Returns:
            dict: A dictionary representation of the validator.
        """
        return {"name": self.name}


class ValidatorsList:
    """
    A class representing a list of validators.

    This class is used to manage a list of validators. It provides methods to get
    the list of validators, get a validator by name, add a validator, remove a
    validator.
    """

    _validators: list[type[Validator]]

    def __init__(self, validators: list[type[Validator]]):
        """
        Initialize a ValidatorsList instance.

        Args:
            validators (list[type[Validator]]): A list of Validator classes.
        """
        self.validators = validators

    @property
    def validators(self):
        """
        Get the list of validators.

        Returns:
            list[type[Validator]]: A list of Validator classes.
        """
        return self._validators

    @validators.setter
    def validators(self, validators: list[type[Validator]]):
        """
        Set the validators.

        Args:
            validators (list[type[Validator]]): A list of Validator classes.

        Raises:
            TypeError: If the validators are not a list.
            TypeError: If a validator is not a class.
            TypeError: If a validator does not inherit from Validator.
        """
        if not isinstance(validators, list):
            raise TypeError("Validators must be a list")
        for validator in validators:
            if not isinstance(validator, type):
                raise TypeError("Each validator must be a class")
            if not issubclass(validator, Validator):
                raise TypeError(f"{validator} must inherit from Validator")
        self._validators = validators

    def check_for_valid_name(self, name: str):
        """
        Check that the given name is a valid Python variable name.

        Args:
            name (str): The name to check.

        Raises:
            NotValidPythonVariableNameException: If the name is not a valid Python variable name.
            PythonKeywordException: If the name is a reserved Python keyword.
        """
        try:
            is_valid_python_variable_name(name)
        except NotValidPythonVariableNameException as exc:
            raise NotValidPythonVariableNameException(
                (
                    f"Validator name '{name}' is not a valid Python variable name. ",
                    "It should start with a letter or an underscore and contain"
                    " only alphanumeric characters or underscores.",
                ),
                details={"validator_name": name},
            ) from exc
        except PythonKeywordException as exc:
            raise PythonKeywordException(
                f"Validator name '{name}' is a reserved Python keyword and cannot be used.",
                details={"validator_name": name},
            ) from exc

    def add(self, name: str):
        """
        Adds a new custom validator to the list.

        The method first checks if a validator with the given name already exists
        in the list. If it does, a ValidatorAlreadyExists exception is raised.
        It also ensures that the provided name is a valid Python variable name
        using `check_for_valid_name`. Finally, it creates a new custom validator
        and appends it to the validators list.

        Args:
            name (str): The name of the validator to add.

        Raises:
            ValidatorAlreadyExists: If a validator with the same name already exists.
            NotValidPythonVariableNameException: If the provided name is not a valid
                                                Python variable name.
            PythonKeywordException: If the name is a reserved Python keyword.
        """
        if name in [validator.name for validator in self.validators]:
            raise ValidatorAlreadyExists(name)

        self.check_for_valid_name(name)

        validator = custom_validator(name)
        self.validators.append(validator)

    def remove(self, name: str):
        """
        Removes a custom validator from the list.

        Args:
            name (str): The name of the validator to remove.

        Raises:
            ValueError: If the validator is a built-in one or not found.
        """
        if name in builtin_validators:
            raise ValueError(f"Cannot remove built-in validator {name}")
        for validator in self.validators:
            if validator.name == name:
                self.validators.remove(validator)
                return
        else:
            raise ValueError(f"Validator {name} not found")

    def change_name(self, old_name: str, new_name: str):
        """
        Changes the name of a validator.

        Args:
            old_name (str): The current name of the validator.
            new_name (str): The new name of the validator.

        Raises:
            ValueError: If the old_name is not found or if the new_name is already
                in use.
        """
        for validator in self.validators:
            if validator.name == new_name:
                raise ValidatorAlreadyExists(new_name)

        self.check_for_valid_name(new_name)

        for validator in self.validators:
            if validator.name == old_name:
                validator.name = new_name
                return
        raise ValueError("Validator not found")

    def __iter__(self):
        """
        Returns an iterator over the validators in the list.

        Yields:
            Validator: An iterator over the Validator instances.
        """
        return iter(self.validators)

    def __len__(self):
        """
        Returns the number of validators in the list.
        """
        return len(self.validators)

    def __getitem__(self, index: int | str):
        """
        Gets a validator by its name or index.

        Args:
            index (int | str): The index of the validator (int) or its name (str).

        Returns:
            Validator: The requested validator.

        Raises:
            KeyError: If the validator with the given name is not found.
            TypeError: If the index is of an unsupported type.
        """
        if isinstance(index, str):
            for validator in self.validators:
                if validator.name == index:
                    return validator
            raise KeyError("Validator not found")
        elif isinstance(index, int):
            return self.validators[index]
        else:
            raise TypeError(
                "Index must be a string (validator name) or an int (list index)"
            )

    def to_dict(self):
        """
        Converts the validators list to a list of dictionaries.

        The list of dictionaries contains the names of the validators
        that are not built-in validators. The dictionaries contain a single key-value
        pair with the key "name" and the value being the name of the validator.

        Returns:
            list[dict[str, str]]: A list of dictionaries containing the names of the validators.
        """
        return [
            {"name": validator.name}
            for validator in self.validators
            if validator.name not in builtin_validators
        ]


builtin_validators = [
    "integer_validator",
    "float_validator",
    "text_validator",
    "date_validator",
    "email_validator",
    "phone_validator",
]
"""
A list of all built-in validator names.

This list contains the names of all validators that are built into the
application. The list is used to check if a validator is built-in or custom.
"""

validators_list = ValidatorsList(
    [
        IntegerValidator,
        FloatValidator,
        TextValidator,
        DateValidator,
        EmailValidator,
        PhoneNumberValidator,
    ]
)
"""
A list of all default validators.

This list contains all built-in validators as well as custom validators created
by the user. The list is used to store and retrieve validators by name.
"""


def custom_validator(validator_name: str):
    """
    Creates a custom validator class.

    Args:
        validator_name (str): The name of the validator.

    Returns:
        CustomValidator: The custom validator class.
    """

    class CustomValidator(Validator):
        """
        A custom validator class created by the user.

        The custom validator class is a subclass of the Validator class and has
        the same attributes and methods. The only difference is that the custom
        validator class has a name attribute that is set to the given validator_name.
        """

        name = validator_name

        def __init__(self, *args, **kwargs):
            pass

        def to_dict(self):
            """
            Converts the custom validator to a dictionary representation.

            The dictionary will contain the name of the custom validator.

            Returns:
                dict: A dictionary representation of the custom validator.
            """
            return {"name": self.name}

    return CustomValidator
