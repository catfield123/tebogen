from Validators import ValidatorsList, validators_list
from QuestionGroupList import QuestionGroupList
import json

import os

import copy

from ConfigJSONEncoder import ConfigJSONEncoder
from ValidatorFactory import ValidatorFactory
from Question import Question
from Group import Group

class ConfigController:
    _is_admin_bot_enabled : bool = False
    _is_google_sheets_sync_enabled : bool = False

    _questions_and_groups : QuestionGroupList = QuestionGroupList([])
    _validators : ValidatorsList = copy.deepcopy(validators_list)
    _config_filename : str


    def __init__(self, is_admin_bot_enabled: bool | None,
                 is_google_sheets_sync_enabled: bool | None,
                 questions_and_groups : QuestionGroupList = QuestionGroupList([]),
                 validators : ValidatorsList = validators_list,
                 config_filename : str = 'tebogen_config.json'
                 ):
        self._config_filename = config_filename
        
        if is_admin_bot_enabled is not None:
            self.is_admin_bot_enabled = is_admin_bot_enabled
        if is_google_sheets_sync_enabled is not None:
            self.is_google_sheets_sync_enabled = is_google_sheets_sync_enabled
        self.questions_and_groups = questions_and_groups
        self.validators = validators

    

    def to_dict(self):
        return {
            "is_admin_bot_enabled": self.is_admin_bot_enabled,
            "is_google_sheets_sync_enabled": self.is_google_sheets_sync_enabled,
            "questions_and_groups": self.questions_and_groups.to_dict(),
            "validators": self.validators.to_dict(),
        }

    def save_to_file(self):
        with open(self._config_filename, 'w', encoding='utf-8') as file:
            json.dump(self.to_dict(), 
                      file, indent=4, 
                      cls=ConfigJSONEncoder, 
                      ensure_ascii=False
                      )
        
    @classmethod
    def load_from_file(cls, config_filename="tebogen_config.json"):
        if not os.path.isfile(config_filename):
            return cls(False, False, config_filename = config_filename)
        with open(config_filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        obj = cls(
                data["is_admin_bot_enabled"] if data.get("is_admin_bot_enabled") is not None else False,
                data["is_google_sheets_sync_enabled"] if data.get("is_google_sheets_sync_enabled") is not None else False,
                QuestionGroupList.from_dict(data["questions_and_groups"]),
                config_filename=config_filename

            )
        
        for validator in data["validators"]:
            obj.add_validator(validator.get("name"))
        return obj
        
        
        

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
        self.save_to_file()
    
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
        self.save_to_file()

    @property
    def questions_and_groups(self):
        return self._questions_and_groups
    
    @questions_and_groups.setter
    def questions_and_groups(self, value : QuestionGroupList) -> None:
        if not isinstance(value, QuestionGroupList):
            raise TypeError("questions_and_groups must be a QuestionGroupList")
        self._questions_and_groups = value
        self.save_to_file()


    @property
    def validators(self):
        return self._validators
    
    @validators.setter
    def validators(self, value : ValidatorsList) -> None:
        if not isinstance(value, ValidatorsList):
            raise TypeError("validators must be a ValidatorsList")
        self._validators = copy.deepcopy(value)
        self.save_to_file()

    def add_validator(self, name):
        self._validators.add(name)
        self.save_to_file()

    def remove_validator(self, name):
        self._validators.remove(name)
        for question_or_group in self._questions_and_groups:
            if isinstance(question_or_group, Question):
                if question_or_group.validator == name:
                    question_or_group.validator = None
            elif isinstance(question_or_group, Group):
                for question in question_or_group.questions:
                    if question.validator == name:
                        question.validator = None
        self.save_to_file()

    def change_validator_name(self, old_name, new_name):
        self._validators.change_name(old_name, new_name)
        for question_or_group in self._questions_and_groups:
            if isinstance(question_or_group, Question):
                if question_or_group.validator == old_name:
                    question_or_group.validator.name = new_name
            elif isinstance(question_or_group, Group):
                for question in question_or_group.questions:
                    if question.validator == old_name:
                        question.validator.name = new_name
        self.save_to_file()

    def __repr__(self):
        return f"Config(is_admin_bot_enabled={self._is_admin_bot_enabled}, is_google_sheets_sync_enabled={self._is_google_sheets_sync_enabled}, questions_and_groups={self._questions_and_groups})"
    
    def pretty_print(self):
        print(f"is_admin_bot_enabled: {self._is_admin_bot_enabled}")
        print(f"is_google_sheets_sync_enabled: {self._is_google_sheets_sync_enabled}\n")
        
        self._questions_and_groups.pretty_print()
    

