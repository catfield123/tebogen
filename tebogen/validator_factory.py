"""
A factory class for creating Validator instances from dictionary representations.

The ValidatorFactory class provides a static method to create different types of
validators based on the data provided in a dictionary. It supports creating
integer, float, text, and date validators based on the specified attributes.
"""

from tebogen.validators import (
    DateFormatEnum,
    DateValidator,
    FloatValidator,
    IntegerValidator,
    TextValidator,
    Validator,
)


class ValidatorFactory:
    """
    A factory class for creating Validator instances from dictionary representations.

    The ValidatorFactory class provides a static method to create different types of
    validators based on the data provided in a dictionary. It supports creating
    integer, float, text, and date validators based on the specified attributes.
    """

    @staticmethod
    def create(data: dict):
        """
        Creates a validator from a dictionary representation.

        Args:
            data (dict): A dictionary with key "name" and optionally
                "min_value", "max_value", "min_length", "max_length", or
                "date_format".

        Returns:
            Validator: A validator populated with the data from the dictionary.

        Raises:
            ValueError: If the dictionary does not contain the required key
                "name".
        """
        if not data.get("name"):
            raise ValueError(f"Unable to parse validator name. Provided data: {data}")
        if data["name"] == "integer_validator":
            return IntegerValidator(
                min_value=data.get("min_value"),
                max_value=data.get("max_value"),
            )
        elif data["name"] == "float_validator":
            return FloatValidator(
                min_value=data.get("min_value"),
                max_value=data.get("max_value"),
            )
        elif data["name"] == "text_validator":
            return TextValidator(
                min_length=data.get("min_length"),
                max_length=data.get("max_length"),
            )
        elif data["name"] == "date_validator":
            return DateValidator(date_format=DateFormatEnum(data.get("date_format")))
        else:
            return Validator(name=data["name"])
