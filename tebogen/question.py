"""
This module contains the Question class, which is used to represent a question
in a QuestionGroup or QuestionGroupList.

"""

from tebogen import utils
from tebogen.validator_factory import ValidatorFactory
from tebogen.validators import Validator


class Question:
    """
    A question in a QuestionGroup or QuestionGroupList.

    Attributes:
        name (str): The name of the question.
        variable_name (str): The variable name of the question.
        validator (Validator | None): The validator of the question.
    """

    _name: str
    _variable_name: str
    _validator: Validator | None

    def __init__(
        self, name: str, variable_name: str, validator: Validator | None = None
    ):
        """
        Initialize a Question instance.

        Args:
            name (str): The name of the question.

            variable_name (str): The variable name of the question.

            validator (Validator | None): The validator associated with this question. Defaults to None.
        """
        self.name = name
        self.variable_name = variable_name
        self.validator = validator

    def __repr__(self):
        """
        Return a string representation of the Question.

        This is a string that would be a valid Python expression to recreate the
        Question. It is also the string that is displayed when the Question is
        printed.

        Returns:
            str: A string representation of the Question.
        """
        return f"Question(name={self._name}, variable_name={self._variable_name}, validator={self._validator})"

    def __eq__(self, other):
        """
        Compare this Question with another object for equality.

        Args:
            other (Union[str, Question]): The object to compare with. It can be a string
            representing a name or another Question instance.

        Returns:
            bool: True if the 'other' is a string and matches the question name, or if
            it's a Question instance and has the same name or variable name. Otherwise, False.
        """
        if isinstance(other, str):
            return self._name == other
        if not isinstance(other, Question):
            return NotImplemented
        return self._name == other._name or self._variable_name == other._variable_name

    @property
    def name(self):
        """
        Get the name of the question.

        Returns:
            str: The name of the question.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """
        Set the name for this question.

        Args:
            value (str): The name to set. It must be a string.

        Raises:
            TypeError: If the provided name is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self._name = value

    @property
    def variable_name(self):
        """
        The variable name for this question.

        Returns:
            str: The variable name.

        Note:
            The variable name is expected to be a valid Python variable name.
        """
        return self._variable_name

    @variable_name.setter
    def variable_name(self, value: str):
        """
        Sets the variable name for the question.

        Args:
            value (str): A string which is a valid Python variable name.

        Raises:
            TypeError: If the provided value is not a string.
            ValueError: If the provided value is not a valid Python variable name.
        """
        if not isinstance(value, str):
            raise TypeError("variable_name must be a string")
        if utils.is_valid_python_variable_name(value):
            self._variable_name = value

    @property
    def validator(self):
        """
        Gets the validator associated with this question.

        Returns:
            Validator or None: The validator associated with this question, or None
            if no validator is associated.
        """
        return self._validator

    @validator.setter
    def validator(self, value: Validator | None):
        """
        Sets the validator for the question.

        Args:
            value (Validator | None): A Validator instance or None to remove the validator.

        Raises:
            TypeError: If the provided value is not a Validator instance or None.
        """
        if not isinstance(value, Validator) and value is not None:
            raise TypeError("validator must be a Validator instance")
        self._validator = value

    @validator.getter
    def validator(self):
        """
        Gets the validator associated with this question.

        Returns:
            Validator or None: The validator associated with this question, or None
            if no validator is associated.
        """
        return self._validator

    @validator.__eq__
    def validator(self, other):
        """
        Compares the current validator with another validator or a string.

        Args:
            other (Validator or str): The other object to compare with.

        Returns:
            bool: True if the validators are equal, False if not. If `other` is a string,
            it returns True if the string matches the name of the validator.
        """
        return self._validator == other

    def to_dict(self):
        """
        Converts the question to a dictionary representation.

        The dictionary will contain the question's name and variable name as well
        as its validator if it has one.

        Returns:
            dict: A dictionary representation of the question.
        """
        result = {
            "name": self._name,
            "variable_name": self._variable_name,
        }
        if self.validator:
            result["validator"] = self.validator.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a Question from a dictionary representation.

        Args:
            data (dict): A dictionary with keys "name", "variable_name", and
                optionally "validator".

        Returns:
            Question: A Question populated with the data from the dictionary.

        Raises:
            ValueError: If the dictionary does not contain the required keys.
        """
        validator = None
        if data.get("validator"):
            validator = ValidatorFactory.create(data["validator"])
        if not data.get("name"):
            raise ValueError(f"Unable to parse question name. Provided data: {data}")
        if not data.get("variable_name"):
            raise ValueError(
                f"Unable to parse question variable name. Provided data: {data}"
            )
        return cls(
            name=data["name"],
            variable_name=data["variable_name"],
            validator=validator,
        )
