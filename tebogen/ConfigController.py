from Validators import ValidatorsList, validators_list
from QuestionGroupList import QuestionGroupList
import json

from ConfigJSONEncoder import ConfigJSONEncoder

class ConfigController:
    _is_admin_bot_enabled : bool = False
    _is_google_sheets_sync_enabled : bool = False

    _questions_and_groups : QuestionGroupList
    _validators : ValidatorsList


    def __init__(self, is_admin_bot_enabled: bool | None,
                 is_google_sheets_sync_enabled: bool | None,
                 questions_and_groups : QuestionGroupList = QuestionGroupList([]),
                 validators : ValidatorsList = validators_list
                 ):
        
        if is_admin_bot_enabled is not None:
            self.is_admin_bot_enabled = is_admin_bot_enabled
        if is_google_sheets_sync_enabled is not None:
            self.is_google_sheets_sync_enabled = is_google_sheets_sync_enabled
        self.questions_and_groups = questions_and_groups
        self.validators = validators

    @classmethod
    def load_from_file(cls, filename = 'tebogen_config.json'):
        with open(filename, 'r') as file:
            data = json.load(file)
        return cls(**data)
    

    def to_dict(self):
        return {
            "is_admin_bot_enabled": self.is_admin_bot_enabled,
            "is_google_sheets_sync_enabled": self.is_google_sheets_sync_enabled,
            "questions_and_groups": self.questions_and_groups.to_dict(),
            "validators": self.validators.to_dict(),
        }

    def save_to_file(self, filename = 'tebogen_config.json'):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.to_dict(), 
                      file, indent=4, 
                      cls=ConfigJSONEncoder, 
                      ensure_ascii=False
                      )
        
        
        

    @property
    def is_admin_bot_enabled(self):
        return self._is_admin_bot_enabled
    
    @is_admin_bot_enabled.setter
    def is_admin_bot_enabled(self, value : bool) -> None:
        """
        Sets the value of the admin bot enabled flag.

        Args:
            value (bool): A boolean indicating if the admin bot should be enabled.

        Raises:
            TypeError: If the provided value is not a boolean.
        """
        if not isinstance(value, bool):
            raise TypeError("is_admin_bot_enabled must be a boolean")
        self._is_admin_bot_enabled = value
    
    @property
    def is_google_sheets_sync_enabled(self):
        return self._is_google_sheets_sync_enabled
    
    @is_google_sheets_sync_enabled.setter
    def is_google_sheets_sync_enabled(self, value : bool) -> None:
        """
        Sets the value of the Google Sheets sync enabled flag.

        Args:
            value (bool): A boolean indicating if Google Sheets sync should be enabled.

        Raises:
            TypeError: If the provided value is not a boolean.
        """
        if not isinstance(value, bool):
            raise TypeError("is_google_sheets_sync_enabled must be a boolean")
        self._is_google_sheets_sync_enabled = value

    @property
    def questions_and_groups(self):
        return self._questions_and_groups
    
    @questions_and_groups.setter
    def questions_and_groups(self, value : QuestionGroupList) -> None:
        if not isinstance(value, QuestionGroupList):
            raise TypeError("questions_and_groups must be a QuestionGroupList")
        self._questions_and_groups = value


    @property
    def validators(self):
        return self._validators
    
    @validators.setter
    def validators(self, value : ValidatorsList) -> None:
        if not isinstance(value, ValidatorsList):
            raise TypeError("validators must be a ValidatorsList")
        self._validators = value

    def add_validator(self, name):
        self._validators.add(name)

    def remove_validator(self, name):
        self._validators.remove(name)

    def __repr__(self):
        return f"Config(is_admin_bot_enabled={self._is_admin_bot_enabled}, is_google_sheets_sync_enabled={self._is_google_sheets_sync_enabled}, questions_and_groups={self._questions_and_groups})"
    
    def pretty_print(self):
        print(f"is_admin_bot_enabled: {self._is_admin_bot_enabled}")
        print(f"is_google_sheets_sync_enabled: {self._is_google_sheets_sync_enabled}\n")
        
        self._questions_and_groups.pretty_print()
    

