from Validators import DateValidator, FloatValidator, IntegerValidator, TextValidator, Validator, DateFormatEnum

class ValidatorFactory:
    @staticmethod
    def create(data: dict):
        if not data.get('name'):
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
            return DateValidator(
                date_format=DateFormatEnum(data.get("date_format"))
            )
        else:
            return Validator(name=data["name"])