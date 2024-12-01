from dataclasses import dataclass
from enum import Enum

from tebogen.exceptions.ValidatorExceptions import ValidatorAlreadyExists
from tebogen.utils import is_valid_python_variable_name
from tebogen.exceptions.common import NotValidPythonVariableNameException, PythonKeywordException

class DateFormatEnum(Enum):
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
        elif isinstance(value, str):
            return self.name == value
        else:
            return False

    def to_dict(self):
        return {"name": self.name}

@dataclass
class IntegerValidator(Validator):
    name = "integer_validator"
    min_value: int | None
    max_value: int | None

    def __init__ (self, min_value: int | None = None, max_value: int | None = None):
        self.min_value = min_value
        self.max_value = max_value

    def to_dict(self):
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

    def __init__ (self, min_value: float | None = None, max_value: float | None = None):
        self.min_value = min_value
        self.max_value = max_value

    def to_dict(self):
        return {
            "name": self.name,
            "min_value": self.min_value,
            "max_value": self.max_value,
        }


@dataclass
class TextValidator(Validator):
    name = 'text_validator'
    min_length: int | None
    max_length: int | None

    def __init__ (self, min_length: int | None = None, max_length: int | None = None):
        self.min_length = min_length
        self.max_length = max_length

    def to_dict(self):
        return {
            "name": self.name,
            "min_length": self.min_length,
            "max_length": self.max_length,
        }

@dataclass
class DateValidator(Validator):
    name = "date_validator"
    date_format : DateFormatEnum

    def __init__(self, date_format : DateFormatEnum = DateFormatEnum.DD_MM_YYYY):
        self.date_format = date_format

    def to_dict(self):
        return {
            "name": self.name,
            "date_format": self.date_format.value,
        }


class EmailValidator(Validator):
    name = "email_validator"
    def __init__(self,*args, **kwargs):
        pass

    def to_dict(self):
        return {
            "name": self.name
        }

class PhoneNumberValidator(Validator):
    name = "phone_validator"
    def __init__(self,*args, **kwargs):
        pass

    def to_dict(self):
        return {
            "name": self.name
        }


class ValidatorsList:
    _validators: list[type[Validator]]
    def __init__(self, validators: list[type[Validator]]):
        self.validators = validators

    @property
    def validators(self):
        return self._validators

    @validators.setter
    def validators(self, validators: list[Validator]):
        if not isinstance(validators, list):
            raise TypeError("Validators must be a list")
        for validator in validators:
            if not isinstance(validator, type):
                raise TypeError("Each validator must be a class")
            if not issubclass(validator, Validator):
                raise TypeError(f"{validator.__name__} must inherit from Validator")
        self._validators = validators


    def check_for_valid_name(self, name: str):
        try:
            is_valid_python_variable_name(name)
        except NotValidPythonVariableNameException:
            raise NotValidPythonVariableNameException(f"Validator name '{name}' is not a valid Python variable name. It should start with a letter or an underscore and contain only alphanumeric characters or underscores.",
                                                      details= {
                                                          "validator_name": name
                                                      }   
                                                      )
        except PythonKeywordException:
            raise PythonKeywordException(f"Validator name '{name}' is a reserved Python keyword and cannot be used.",
                                         details= {
                                             "validator_name": name
                                         }
                                         )
    def add(self, name: str):
        if name in [validator.name for validator in self.validators]:
            raise ValidatorAlreadyExists(name)
        
        self.check_for_valid_name(name)
        
        validator = custom_validator(name)
        self.validators.append(validator)
    
    def remove(self, name: str):
        if name in builtin_validators:
            raise ValueError(f"Cannot remove built-in validator {name}")
        for validator in self.validators:
            if validator.name == name:
                self.validators.remove(validator)
                return
        else:
            raise ValueError(f"Validator {name} not found")

    def change_name(self, old_name: str, new_name: str):
        for validator in self.validators:
            if validator.name == new_name:
                raise ValidatorAlreadyExists(new_name)
            
        self.check_for_valid_name(new_name)
        
        for validator in self.validators:
            if validator.name == old_name:
                validator.name = new_name
                return
        raise ValueError(f"Validator not found")

    def __iter__(self):
        return iter(self.validators)
    
    def __len__(self):
        return len(self.validators)
    
    def __getitem__(self, index: int  | str):
        if isinstance(index, str):
            for validator in self.validators:
                if validator.name == index:
                    return validator
            raise KeyError("Validator not found")
        elif isinstance(index, int):
            return self.validators[index]
        else:
            raise TypeError("Index must be a string (validator name) or an int (list index)")
        
    def to_dict(self):
        return [{"name": validator.name} for validator in self.validators if validator.name not in builtin_validators]


builtin_validators = ['integer_validator', 'float_validator', 'text_validator', 'date_validator', 'email_validator', 'phone_validator']

validators_list = ValidatorsList([
    IntegerValidator,
    FloatValidator,
    TextValidator,
    DateValidator,
    EmailValidator,
    PhoneNumberValidator
])

def custom_validator(validator_name: str):
    class CustomValidator(Validator):
        name = validator_name
        def __init__(self,*args, **kwargs):
            pass

        def to_dict(self):
            return {
                "name": self.name
            }

    return CustomValidator