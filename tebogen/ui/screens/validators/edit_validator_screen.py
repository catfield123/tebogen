"""
EditValidatorScreen class.

This class provides a UI screen for editing a validator. The screen displays a
form with fields for the validator's name, description, and attributes. The user
can edit the fields and save the changes to the validator.

"""

import curses

from tebogen.colors import Colors
from tebogen.config_controller import ConfigController
from tebogen.exceptions.common import (
    NotValidPythonVariableNameException,
    PythonKeywordException,
)
from tebogen.exceptions.validator_exceptions import ValidatorAlreadyExists
from tebogen.ui.base_screen import BaseScreen
from tebogen.ui.NavigationController import NavigationController
from tebogen.ui.screens.confirm_screen import ConfirmScreen
from tebogen.validators import Validator


class EditValidatorScreen(BaseScreen):
    """
    This class provides a screen for editing existing validators.

    The EditValidatorScreen class allows users to modify the attributes of a given
    validator. It provides an interface for users to interact with the validator's
    details and save any changes made.

    Attributes:
        validator (Validator): The validator being edited.
        selected_idx (int): The index of the currently selected menu item.
        is_typing (bool): Indicates if the user is in typing mode.
        error_messages (list[str]): A collection of error messages to display.
        text_field (str): Contains the current input text, initialized with the validator's name.
    """

    def __init__(
        self,
        stdscr,
        navigation_controller: NavigationController,
        config_controller: ConfigController,
        validator: Validator,
    ):
        """
        Initializes an EditValidatorScreen instance.

        Args:
            stdscr: The curses window to use for displaying the screen.
            navigation_controller (NavigationController): Manages navigation between screens.
            config_controller (ConfigController): Handles configuration management.
            validator (Validator): The validator to be edited.

        Attributes:
            selected_idx (int): The index of the currently selected menu item.
            is_typing (bool): Indicates whether the user is currently typing.
            error_messages (list[str]): A list of error messages to display.
            text_field (str): The current text in the text field, initialized with the validator name.
        """
        super().__init__(stdscr, navigation_controller, config_controller)
        self.validator = validator
        self.selected_idx = 0
        self.is_typing = False
        self.error_messages: list[str] = []
        self.text_field = self.validator.name

    def display(self):
        """
        Displays the edit validator screen.

        This method clears the screen and displays the current state of the
        edit validator interface. It provides options to enter a validator
        name, confirm the changes, delete the validator, or cancel the action.
        The user can navigate through the options, and any error messages are
        displayed in red.

        Highlights:
            - Displays the current validator name being edited.
            - Indicates the selected option with a '>' symbol.
            - Shows error messages, if any, below the options.
            - Controls cursor visibility based on typing state.
        """
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f"Edit validator {self.validator.name}")
        self.stdscr.addstr(
            1,
            0,
            ("> " if (self.selected_idx == 0 and not self.is_typing) else "  ")
            + "[Enter validator name]",
        )

        if self.selected_idx == 0:
            self.stdscr.addstr(1, 25, f"{self.text_field}")
        else:
            self.stdscr.addstr(1, 25, self.text_field)

        self.stdscr.addstr(
            2, 0, ("> " if self.selected_idx == 1 else "  ") + "[Confirm]"
        )
        self.stdscr.addstr(
            3, 0, ("> " if self.selected_idx == 2 else "  ") + "[Delete validator]"
        )
        self.stdscr.addstr(
            4, 0, ("> " if self.selected_idx == 3 else "  ") + "[Cancel]"
        )

        if len(self.error_messages) > 0:
            for idx, message in enumerate(self.error_messages):
                self.stdscr.addstr(6 + idx, 0, message, Colors.RED_BLACK)

        if self.is_typing:
            self.stdscr.move(1, 25 + len(self.text_field))
            curses.curs_set(1)
        else:
            curses.curs_set(0)

        self.stdscr.refresh()

    def handle_input(self, key):
        """
        Handle user input for the screen.

        Args:
            key: The key pressed by the user. This can be used to determine
                the action to be taken, such as navigation or selection.

        Actions:
            - Moves the selection up or down between "Cancel" and "Confirm" options.
            - Executes the selected action when the Enter key is pressed.
        """
        if self.is_typing:
            if key in [curses.KEY_ENTER, 10, 13]:
                self.is_typing = False
            elif key in (curses.KEY_BACKSPACE, 127):
                self.text_field = self.text_field[:-1]
            elif key >= 32 and key <= 126:
                self.text_field += chr(key)
            return

        if key == curses.KEY_UP and self.selected_idx > 0:
            self.selected_idx -= 1
        elif key == curses.KEY_DOWN and self.selected_idx < 3:
            self.selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if self.selected_idx == 0:
                self.is_typing = True
            elif self.selected_idx == 1:
                self.text_field = self.text_field.strip()
                try:
                    if self.validator.name == self.text_field:
                        self.navigate_back()
                    if not self.text_field == self.validator.name:
                        self.config_controller.change_validator_name(
                            self.validator.name, self.text_field
                        )
                        self.navigate_back()
                except ValidatorAlreadyExists as e:
                    self.error_messages = [str(e)]
                except NotValidPythonVariableNameException as e:
                    self.error_messages = [str(e)]
                except PythonKeywordException as e:
                    self.error_messages = [str(e)]
            elif self.selected_idx == 2:
                self.navigation_controller.navigate_to(
                    ConfirmScreen(
                        self.stdscr,
                        self.navigation_controller,
                        self.config_controller,
                        confirm_callback=lambda: [
                            self.config_controller.remove_validator(
                                self.validator.name
                            ),
                            self.navigate_back(2),
                        ],
                        title="Delete Validator",
                        message=f"Are you sure you want to delete validator '{self.validator.name}'?",
                    )
                )
            elif self.selected_idx == 3:
                self.navigate_back()
