from dataclasses import dataclass
from enum import Enum

class DateFormat(Enum):
    DD_MM_YYYY = "dd.mm.yyyy"
    MM_DD_YYYY = "mm.dd.yyyy"
    YYYY_MM_DD = "yyyy.mm.dd"
    DD_MM_YY = "dd.mm.yy"
    MM_DD_YY = "mm.dd.yy"
    YY_MM_DD = "yy.mm.dd"

@dataclass
class Validator:
    name: str

@dataclass
class IntegerValidator(Validator):
    name = "integer_validator"
    min_value: int | None = None
    max_value: int | None = None

@dataclass
class FloatValidator(Validator):
    name = "float_validator"
    min_value: float | None = None
    max_value: float | None = None


@dataclass
class TextValidator(Validator):
    name = 'text_validator'
    min_length: int | None = None
    max_length: int | None = None

    def __init__ (self, min_length: int | None = None, max_length: int | None = None):
        self.min_length = min_length
        self.max_length = max_length

@dataclass
class DateValidator(Validator):
    name = "date_validator"
    date_format : DateFormat = DateFormat.DD_MM_YYYY

    def __init__(self, date_format : DateFormat = DateFormat.DD_MM_YYYY):
        self.date_format = date_format


class EmailValidator(Validator):
    name = "email_validator"
    def __init__(self,*args, **kwargs):
        pass

class PhoneNumberValidator(Validator):
    name = "phone_validator"
    def __init__(self,*args, **kwargs):
        pass


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

    def add(self, name: str):
        if name in [validator.name for validator in self.validators]:
            raise ValueError(f"Validator {name} already exists")
        validator = custom_validator(name)
        self.validators.append(validator)
    
    def remove(self, name: str):
        if name in ['integer_validator', 'float_validator', 'text_validator', 'date_validator', 'email_validator', 'phone_validator']:
            raise ValueError(f"Cannot remove built-in validator {name}")
        for validator in self.validators:
            if validator.name == name:
                self.validators.remove(validator)
                return
        else:
            raise ValueError(f"Validator {name} not found")


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
    return CustomValidator