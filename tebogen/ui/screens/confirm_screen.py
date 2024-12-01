import curses
import textwrap

from tebogen.colors import Colors
from tebogen.config_controller import ConfigController
from tebogen.ui.base_screen import BaseScreen
from tebogen.ui.NavigationController import NavigationController


class ConfirmScreen(BaseScreen):
    def __init__(
        self,
        stdscr,
        navigation_controller: NavigationController,
        config_controller: ConfigController,
        confirm_callback,
        title: str,
        message: str | None = None,
    ):
        super().__init__(stdscr, navigation_controller, config_controller)
        self.selected_idx = 0
        self.title = title
        self.message = message
        self.confirm_callback = confirm_callback

    def display(self):
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

        if key == curses.KEY_UP and self.selected_idx == 1:
            self.selected_idx -= 1
        elif key == curses.KEY_DOWN and self.selected_idx == 0:
            self.selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if self.selected_idx == 0:  # Cancel
                self.navigate_back()
            elif self.selected_idx == 1:  # Confirm
                self.confirm_callback()
