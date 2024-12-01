"""
Encoding of tebogen objects to JSON format.

This module provides a custom JSON encoder that converts tebogen objects to
JSON by calling their to_dict method if available.

"""

import json


class ConfigJSONEncoder(json.JSONEncoder):
    """
    Encode objects to JSON by calling their to_dict method if available

    The class is derived from json.JSONEncoder and overrides its default
    method to call the to_dict method of objects that have it. This allows
    to easily serialize objects of custom classes to JSON.

    Example:
        >>> import json
        >>> class Person:
        ...     def __init__(self, name, age):
        ...         self.name = name
        ...         self.age = age
        ...     def to_dict(self):
        ...         return {"name": self.name, "age": self.age}
        >>> person = Person("John Doe", 42)
        >>> json.dumps(person, cls=ConfigJSONEncoder)
        {"name": "John Doe", "age": 42}

    """

    def default(self, o):
        """
        Encode object to JSON by calling its to_dict method if available

        The method is used by json.dumps to serialize objects. It is
        called with an object o to encode. If o has a to_dict method,
        it is called to get a dictionary representing the object. Otherwise
        the method of the base class is called.

        :param o: object to encode
        :return: a dictionary representing the object
        """
        if hasattr(o, "to_dict"):
            return o.to_dict()
        return super().default(o)
