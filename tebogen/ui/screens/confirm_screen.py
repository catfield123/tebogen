"""
A module providing a screen to confirm a user action.

The ConfirmScreen class is a special screen for confirming a user action. It
displays a title and an optional message, and provides Yes and No buttons for
the user to confirm or cancel the action. The screen is used to prevent
accidental changes to the user's data.

"""

import curses
import textwrap

from tebogen.colors import Colors
from tebogen.config_controller import ConfigController
from tebogen.ui.base_screen import BaseScreen
from tebogen.ui.navigation_controller_screen import NavigationController


class ConfirmScreen(BaseScreen):
    """
    A screen to confirm a user action.

    This class provides a screen to confirm a user action. It displays a
    title and an optional message, and provides Yes and No buttons for
    the user to confirm or cancel the action.
    """

    def __init__(
        self,
        stdscr,
        navigation_controller: NavigationController,
        config_controller: ConfigController,
        confirm_callback,
        title: str,
        message: str | None = None,
    ):
        """
        Initializes a new ConfirmScreen instance.

        Args:
            stdscr: The curses window to use for displaying the screen.
            navigation_controller (NavigationController): Manages navigation between screens.
            config_controller (ConfigController): Handles configuration management.
            confirm_callback: A callback function to be executed when the action is confirmed.
            title (str): The title to display on the confirm screen.
            message (str | None): An optional message to display on the confirm screen.
        """
        super().__init__(stdscr, navigation_controller, config_controller)
        self.selected_idx = 0
        self.title = title
        self.message = message
        self.confirm_callback = confirm_callback

    def display(self):
        """
        Displays the confirm screen.

        This method displays the confirm screen, including the title and an
        optional message. It also displays the [Cancel] and [Confirm] options
        and highlights the currently selected option.

        This method should be called whenever the screen needs to be updated.
        """
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        self.stdscr.addstr(0, 0, self.title)

        if self.message:
            wrapped_message = []
            for line in self.message.split("\n"):
                wrapped_message.extend(textwrap.wrap(line, width=width))
            for i, line in enumerate(wrapped_message):
                self.stdscr.addstr(1 + i, 0, line)

        message_end_row = 1 + len(wrapped_message) if self.message else 2
        cancel_row = message_end_row + 1
        confirm_row = message_end_row + 2

        self.stdscr.addstr(
            cancel_row, 0, ("> " if self.selected_idx == 0 else "  ") + "[Cancel]"
        )
        self.stdscr.addstr(
            confirm_row,
            0,
            ("> " if self.selected_idx == 1 else "  ") + "[Confirm]",
            Colors.RED_BLACK,
        )

        curses.curs_set(0)
        self.stdscr.refresh()

    def handle_input(self, key):
        """
        Handle user input for the confirm screen.

        Args:
            key: The key pressed by the user. This determines the action to be taken.

        Actions:
            - Moves the selection up or down between "Cancel" and "Confirm" options.
            - Executes the selected action when the Enter key is pressed.
        """
        if key == curses.KEY_UP and self.selected_idx == 1:
            self.selected_idx -= 1
        elif key == curses.KEY_DOWN and self.selected_idx == 0:
            self.selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if self.selected_idx == 0:  # Cancel
                self.navigate_back()
            elif self.selected_idx == 1:  # Confirm
                self.confirm_callback()
