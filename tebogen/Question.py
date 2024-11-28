from ValidatorFactory import ValidatorFactory
import utils
from Validators import Validator


class Question:
    _name : str
    _variable_name : str
    _validator : Validator | None

    def __init__(self, name: str, variable_name: str, validator: Validator | None = None):
        self.name = name
        self.variable_name = variable_name
        self.validator = validator

    def __repr__(self):
        return f"Question(name={self._name}, variable_name={self._variable_name}, validator={self._validator})"
    
    def __eq__(self, other):
        if not isinstance(other, Question):
            return NotImplemented
        return self._name == other._name or self._variable_name == other._variable_name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value : str):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self._name = value

    @property
    def variable_name(self):
        return self._variable_name
    
    @variable_name.setter
    def variable_name(self, value : str):
        if not isinstance(value, str):
            raise TypeError("variable_name must be a string")
        if utils.is_valid_python_variable_name(value):
            self._variable_name = value

    @property
    def validator(self):
        return self._validator
    
    @validator.setter
    def validator(self, value : Validator | None):
        if not isinstance(value, Validator) and  value is not None:
            raise TypeError("validator must be a Validator instance")
        self._validator = value

    def to_dict(self):
        return {
            "name": self._name,
            "variable_name": self._variable_name,
            "validator": self._validator.to_dict()
        }


    @classmethod
    def from_dict(cls, data: dict):
        validator = None
        if data.get("validator"):
            validator = ValidatorFactory.create(data["validator"])
        if not data.get('name'):
            raise ValueError(f"Unable to parse question name. Provided data: {data}")
        if not data.get('variable_name'):
            raise ValueError(f"Unable to parse question variable name. Provided data: {data}")
        return cls(
            name=data["name"],
            variable_name=data["variable_name"],
            validator=validator,
        )