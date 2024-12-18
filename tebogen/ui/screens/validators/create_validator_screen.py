"""
This module provides the CreateValidatorScreen class for creating a new custom validator.

The CreateValidatorScreen class is a subclass of BaseScreen and is responsible for
displaying the screen for creating a new custom validator. It provides an interface for
the user to input the name of the validator and its attributes.

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
from tebogen.ui.navigation_controller_screen import NavigationController


class CreateValidatorScreen(BaseScreen):
    """
    A screen to create a new validator.

    The CreateValidatorScreen class is responsible for rendering a UI for the user
    to create a new validator. It provides an input field for the user to enter the
    name of the validator and validates the input. The screen is used to prevent
    accidental creation of a validator with a name that is already in use.

    Attributes:
        selected_idx (int): The index of the currently selected UI element.
    """

    def __init__(
        self,
        stdscr,
        navigation_controller: NavigationController,
        config_controller: ConfigController,
    ):
        """
        Initialize the CreateValidatorScreen.

        Args:
            stdscr: The curses window to use for rendering the screen.
            navigation_controller: Manages navigation between different screens.
            config_controller: Handles configuration management for the application.

        Attributes:
            selected_idx: The index of the currently selected UI element.
            is_typing: A boolean indicating if the user is typing in the text field.
            error_messages: A list of error messages to be displayed on the screen.
            text_field: The current text entered in the input field for the validator name.
        """
        super().__init__(stdscr, navigation_controller, config_controller)
        self.selected_idx = 0
        self.is_typing = False
        self.error_messages: list[str] = []
        self.text_field = ""

    def display(self):
        """
        Displays the create custom validator screen.

        The screen displays a text field to enter the name of the validator,
        and three buttons: Confirm, Cancel, and a dummy button to navigate to.
        The screen also displays any error messages that occurred while trying
        to create the validator.

        The method redraws the entire screen, so it should be called whenever
        the state of the screen changes (e.g. when the user types something,
        or when the user navigates to a different button).

        The method also sets the cursor position to the end of the text field
        if the user is currently typing, and sets it to nowhere if the user is
        not typing.
        """
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Create custom validator")
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
            3, 0, ("> " if self.selected_idx == 2 else "  ") + "[Cancel]"
        )

        if len(self.error_messages) > 0:
            for idx, message in enumerate(self.error_messages):
                self.stdscr.addstr(5 + idx, 0, message, Colors.RED_BLACK)

        if self.is_typing:
            self.stdscr.move(1, 25 + len(self.text_field))
            curses.curs_set(1)
        else:
            curses.curs_set(0)

        self.stdscr.refresh()

    def handle_input(self, key):
        """
        Handle user input for the CreateValidatorScreen.

        Args:
            key: The key pressed by the user. This determines the action to be taken.

        Actions:
            - Moves the selection up or down between "Cancel" and "Confirm" options.
            - Executes the selected action when the Enter key is pressed.
            - Handles typing the validator name when the user is typing.
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
        elif key == curses.KEY_DOWN and self.selected_idx < 2:
            self.selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if self.selected_idx == 0:
                self.is_typing = True
            elif self.selected_idx == 1:  # Confirm
                try:
                    self.config_controller.add_validator(self.text_field)
                    self.navigate_back()
                except ValidatorAlreadyExists as e:
                    self.error_messages = [str(e)]
                except NotValidPythonVariableNameException as e:
                    self.error_messages = [str(e)]
                except PythonKeywordException as e:
                    self.error_messages = [str(e)]
            elif self.selected_idx == 2:  # Cancel
                self.navigate_back()
