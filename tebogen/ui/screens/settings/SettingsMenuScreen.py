"""
This module provides the SettingsMenuScreen class for displaying the settings menu.

The SettingsMenuScreen class is a subclass of BaseScreen and is responsible for
displaying the settings menu of the application. It provides an interface for the
user to navigate to different parts of the application.

"""

import curses

from tebogen.config_controller import ConfigController
from tebogen.ui.base_screen import BaseScreen
from tebogen.ui.NavigationController import NavigationController


class SettingsMenuScreen(BaseScreen):
    """
    The SettingsMenuScreen class for displaying the settings menu.

    This class inherits from BaseScreen and provides functionality for rendering
    and handling user input on the settings menu screen. It allows the user to
    navigate through the settings menu and select different options to access
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
        Initialize the settings menu screen.

        Args:
            stdscr: The curses window to use.
            navigation_controller: The NavigationController instance to use.
            config_controller: The ConfigController instance to use.

        Attributes:
            menu_items: A list of the settings menu items.
            selected_idx: The index of the currently selected menu item.
        """
        super().__init__(
            stdscr, navigation_controller, config_controller=config_controller
        )
        self.menu_items = ["Setting 1", "Setting 2", "Setting 3"]
        self.selected_idx = 0

    def display(self):
        """
        Render the settings menu on the screen.

        Clears the screen, displays the settings menu items, and highlights
        the currently selected menu item. Refreshes the screen to reflect these changes.
        """
        self.stdscr.clear()
        curses.curs_set(0)
        self.stdscr.addstr(0, 0, "Settings")
        for idx, item in enumerate(self.menu_items):
            if idx == self.selected_idx:
                self.stdscr.addstr(idx + 1, 0, f"> {item}")
            else:
                self.stdscr.addstr(idx + 1, 0, f"  {item}")
        self.stdscr.refresh()

    def handle_input(self, key):
        """
        Handle user input for the SettingsMenuScreen.

        This method changes the selected index and navigates to the previous screen
        when the user presses the UP/DOWN arrow keys and the ENTER key, respectively.

        Args:
            key: The key pressed by the user.
        """
        if key == curses.KEY_UP and self.selected_idx > 0:
            self.selected_idx -= 1
        elif key == curses.KEY_DOWN and self.selected_idx < len(self.menu_items) - 1:
            self.selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            self.navigate_back()
