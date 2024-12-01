"""
This module provides the ValidatorsListScreen class, which is a UI screen for displaying a
list of all validators in the application. It provides an interface for the user to navigate
through the list of validators and select one to edit or delete. It also provides an option
to create a new validator.

"""

import curses

from tebogen.colors import Colors
from tebogen.config_controller import ConfigController
from tebogen.ui.base_screen import BaseScreen
from tebogen.ui.navigation_controller_screen import NavigationController
from tebogen.ui.screens.validators.create_validator_screen import CreateValidatorScreen
from tebogen.ui.screens.validators.edit_validator_screen import EditValidatorScreen
from tebogen.validators import Validator, builtin_validators


class ValidatorsListScreen(BaseScreen):
    """
    A screen to display a list of all validators in the application.

    The list is scrolled and shows whether a validator is a built-in or custom
    validator. The selected validator is highlighted. The user can navigate the
    list and select a validator to view/edit its details.

    """

    def __init__(
        self,
        stdscr,
        navigation_controller: NavigationController,
        config_controller: ConfigController,
    ):
        """
        Initialize the ValidatorsListScreen.

        Args:
            stdscr: The curses window to use.
            navigation_controller: Manages navigation between screens.
            config_controller: Handles configuration management.

        Attributes:
            selected_idx: The index of the currently selected validator.
            start_idx: The starting index for scrolling the validator list.
        """
        super().__init__(stdscr, navigation_controller, config_controller)
        self.selected_idx = 0
        self.start_idx = 0
        self.fetch_validators(self.config_controller)

    def display(self):
        """
        Displays a list of all validators in the application.

        The list is scrolled and shows whether a validator is a built-in or custom
        validator. The selected validator is highlighted.

        """
        self.fetch_validators(self.config_controller)
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        if self.selected_idx >= len(self.menu_items):
            self.selected_idx = len(self.menu_items) - 1
        visible_items = height - 2
        end_idx = self.start_idx + visible_items

        self.stdscr.addstr(0, 0, "Validators")
        for idx, item in enumerate(self.menu_items[self.start_idx : end_idx]):
            actual_idx = idx + self.start_idx
            if isinstance(item, type) and issubclass(item, Validator):
                self.stdscr.addstr(
                    idx + 1,
                    0,
                    ("> " if actual_idx == self.selected_idx else "  ")
                    + f"{item.name}",
                )
                self.stdscr.addstr(
                    idx + 1,
                    2 + len(item.name),
                    " (builtin)" if item.name in builtin_validators else " (custom)",
                    (
                        Colors.GREEN_BLACK
                        if item.name in builtin_validators
                        else Colors.YELLOW_BLACK
                    ),
                )
            else:
                self.stdscr.addstr(
                    idx + 1,
                    0,
                    ("> " if actual_idx == self.selected_idx else "  ") + f"{item}",
                )
        self.stdscr.refresh()

    def fetch_validators(self, config_controller: ConfigController):
        """
        Fetch the list of validators from the config_controller and populate the menu_items with them.

        The first item in the menu_items is always "[Create custom validator]".
        Then, the list of validators is appended to the menu_items.

        Args:
            config_controller (ConfigController): The config_controller that contains the list of validators.
        """
        self.menu_items = ["[Create custom validator]"]
        for validator in config_controller.validators.validators:
            self.menu_items.append(validator)

    def handle_input(self, key):
        """
        Handle user input for the ValidatorsListScreen.

        Args:
            key: The key pressed by the user. This determines the action to be taken.

        Actions:
            - Moves the selection up or down between the list of validators.
            - Navigates to CreateValidatorScreen when the first item is selected.
            - Navigates to EditValidatorScreen when a custom validator is selected.
            - Does nothing when a built-in validator is selected.
            - Navigates back to the previous screen when the Backspace key is pressed.
        """
        height, _ = self.stdscr.getmaxyx()
        visible_items = height - 2

        if key == curses.KEY_BACKSPACE:
            self.navigate_back()
        elif key == curses.KEY_UP and self.selected_idx > 0:
            self.selected_idx -= 1
            if self.selected_idx < self.start_idx:
                self.start_idx -= 1
        elif key == curses.KEY_DOWN and self.selected_idx < len(self.menu_items) - 1:
            self.selected_idx += 1
            if self.selected_idx >= self.start_idx + visible_items:
                self.start_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if self.selected_idx == 0:
                self.navigation_controller.navigate_to(
                    CreateValidatorScreen(
                        self.stdscr, self.navigation_controller, self.config_controller
                    )
                )
            elif (
                isinstance(self.menu_items[self.selected_idx], type)
                and issubclass(self.menu_items[self.selected_idx], Validator)
                and self.menu_items[self.selected_idx].name in builtin_validators
            ):
                pass  # do nothing, it's a builtin validator
            elif isinstance(self.menu_items[self.selected_idx], type) and issubclass(
                self.menu_items[self.selected_idx], Validator
            ):
                self.navigation_controller.navigate_to(
                    EditValidatorScreen(
                        self.stdscr,
                        self.navigation_controller,
                        self.config_controller,
                        self.menu_items[self.selected_idx],
                    )
                )
            else:
                self.navigate_back()
