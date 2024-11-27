from Validators import Validator
from QuestionGroupList import QuestionGroupList


class Config:
    _is_admin_bot_enabled : bool = False
    _is_google_sheets_sync_enabled : bool = False

    _questions_and_groups : QuestionGroupList = []

    def __init__(self, is_admin_bot_enabled: bool | None,
                 is_google_sheets_sync_enabled: bool | None,
                 questions_and_groups : QuestionGroupList = []
                 ):
        
        if is_admin_bot_enabled is not None:
            self.is_admin_bot_enabled = is_admin_bot_enabled
        if is_google_sheets_sync_enabled is not None:
            self.is_google_sheets_sync_enabled = is_google_sheets_sync_enabled
        self.questions_and_groups = questions_and_groups
        
        

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


    def __repr__(self):
        return f"Config(is_admin_bot_enabled={self._is_admin_bot_enabled}, is_google_sheets_sync_enabled={self._is_google_sheets_sync_enabled}, questions_and_groups={self._questions_and_groups})"
    
    def pretty_print(self):
        print(f"is_admin_bot_enabled: {self._is_admin_bot_enabled}")
        print(f"is_google_sheets_sync_enabled: {self._is_google_sheets_sync_enabled}\n")
        
        self._questions_and_groups.pretty_print()
    

