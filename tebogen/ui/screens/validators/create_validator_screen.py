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


class CreateValidatorScreen(BaseScreen):
    def __init__(
        self,
        stdscr,
        navigation_controller: NavigationController,
        config_controller: ConfigController,
    ):
        super().__init__(stdscr, navigation_controller, config_controller)
        self.selected_idx = 0
        self.is_typing = False
        self.error_messages: list[str] = []
        self.text_field = ""

    def display(self):
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
