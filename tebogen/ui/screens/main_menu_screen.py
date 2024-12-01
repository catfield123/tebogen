"""
This module provides the MainMenuScreen class for displaying the main menu.

The MainMenuScreen class is a subclass of BaseScreen and is responsible for
displaying the main menu of the application. It provides an interface for the
user to navigate to different parts of the application.

"""

import curses

from tebogen.config_controller import ConfigController
from tebogen.ui.base_screen import BaseScreen
from tebogen.ui.navigation_controller_screen import NavigationController
from tebogen.ui.screens.questions.questions_list_screen import QuestionsListScreen
from tebogen.ui.screens.settings.settings_menu_screen import SettingsMenuScreen
from tebogen.ui.screens.validators.validators_list_screen import ValidatorsListScreen


class MainMenuScreen(BaseScreen):
    """
    The MainMenuScreen class for displaying the main menu.

    This class inherits from BaseScreen and provides functionality for rendering
    and handling user input on the main menu screen. It allows the user to
    navigate through the main menu and select different options to access
    various parts of the application.

    Attributes:
        menu_items (list[str]): A list of menu item names.
        selected_idx (int): The index of the currently selected menu item.
    """

    def __init__(
        self,
        stdscr,
        navigation_controller: NavigationController,
        config_controller: ConfigController,
    ):
        """
        Initialize the main menu screen.

        This method is called when a new instance of the MainMenuScreen class is created.
        It initializes the menu items and the selected index.

        Args:
            stdscr: The curses window to use.
            navigation_controller: The NavigationController instance to use.
            config_controller: The ConfigController instance to use.

        Attributes:
            menu_items: A list of the menu items.
            selected_idx: The index of the currently selected menu item.
        """
        super().__init__(stdscr, navigation_controller, config_controller)
        self.menu_items = ["Settings", "Edit Questions", "Edit Validators", "Exit"]
        self.selected_idx = 0

    def display(self):
        """
        Render the main menu on the screen.

        This method clears the screen and displays the main menu items.
        It highlights the currently selected menu item and refreshes
        the screen to reflect these changes.
        """
        self.stdscr.clear()
        curses.curs_set(0)
        self.stdscr.addstr(0, 0, "Main Menu")
        for idx, item in enumerate(self.menu_items):
            if idx == self.selected_idx:
                self.stdscr.addstr(idx + 1, 0, f"> {item}")
            else:
                self.stdscr.addstr(idx + 1, 0, f"  {item}")
        self.stdscr.refresh()

    def handle_input(self, key):
        """
        Handle input in the main menu screen.

        This method is called when the user presses a key in the main menu screen.
        It handles the following keys:

        - UP/DOWN arrow keys: move the selected item up or down
        - ENTER key: navigate to the selected item
        - BACKSPACE key: exit the app

        Args:
            key (int): The key that was pressed by the user.
        """
        if key == curses.KEY_UP and self.selected_idx > 0:
            self.selected_idx -= 1
        elif key == curses.KEY_DOWN and self.selected_idx < len(self.menu_items) - 1:
            self.selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if self.selected_idx == 0:  # Settings
                self.navigation_controller.navigate_to(
                    SettingsMenuScreen(
                        self.stdscr, self.navigation_controller, self.config_controller
                    )
                )
            elif self.selected_idx == 1:  # Edit Questions
                self.navigation_controller.navigate_to(
                    QuestionsListScreen(
                        self.stdscr, self.navigation_controller, self.config_controller
                    )
                )
            elif self.selected_idx == 2:  # Edit Validators
                self.navigation_controller.navigate_to(
                    ValidatorsListScreen(
                        self.stdscr, self.navigation_controller, self.config_controller
                    )
                )
            elif self.selected_idx == 3:  # Exit
                self.navigation_controller.exit_app()
