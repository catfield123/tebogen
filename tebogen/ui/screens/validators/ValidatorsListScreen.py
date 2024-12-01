from tebogen.ConfigController import ConfigController
from tebogen.Validators import Validator, builtin_validators
from tebogen.Colors import Colors
from tebogen.ui.screens.validators.EditValidatorScreen import EditValidatorScreen
from tebogen.ui.screens.validators.CreateValidatorScreen import CreateValidatorScreen
from tebogen.ui.NavigationController import NavigationController

from tebogen.ui.BaseScreen import BaseScreen
import curses


class ValidatorsListScreen(BaseScreen):
    def __init__(self, stdscr, navigation_controller: NavigationController, config_controller: ConfigController):
        super().__init__(stdscr, navigation_controller, config_controller)
        self.selected_idx = 0
        self.start_idx = 0
        self.fetch_validators(self.config_controller)

    def display(self):
        self.fetch_validators(self.config_controller)
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        if self.selected_idx >= len(self.menu_items):
            self.selected_idx = len(self.menu_items) - 1
        visible_items = height - 2
        end_idx = self.start_idx + visible_items

        self.stdscr.addstr(0, 0, "Validators")
        for idx, item in enumerate(self.menu_items[self.start_idx:end_idx]):
            actual_idx = idx + self.start_idx
            if isinstance(item, type) and issubclass(item, Validator):
                self.stdscr.addstr(
                    idx + 1, 0,
                    ("> " if actual_idx == self.selected_idx else "  ") + f"{item.name}"
                )
                self.stdscr.addstr(
                    idx + 1, 2 + len(item.name),
                    " (builtin)" if item.name in builtin_validators else " (custom)",
                    Colors.GREEN_BLACK if item.name in builtin_validators else Colors.YELLOW_BLACK
                )
            else:
                self.stdscr.addstr(
                    idx + 1, 0,
                    ("> " if actual_idx == self.selected_idx else "  ") + f"{item}"
                )
        self.stdscr.refresh()

    def fetch_validators(self, config_controller: ConfigController):
        self.menu_items = ['[Create custom validator]']
        for validator in config_controller.validators.validators:
            self.menu_items.append(validator)

    def handle_input(self, key):
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
                self.navigation_controller.navigate_to(CreateValidatorScreen(self.stdscr, self.navigation_controller, self.config_controller))
            elif isinstance(self.menu_items[self.selected_idx], type) and issubclass(self.menu_items[self.selected_idx], Validator) and self.menu_items[self.selected_idx].name in builtin_validators:
                pass  # do nothing, it's a builtin validator
            elif isinstance(self.menu_items[self.selected_idx], type) and issubclass(self.menu_items[self.selected_idx], Validator):
                self.navigation_controller.navigate_to(EditValidatorScreen(self.stdscr, self.navigation_controller, self.config_controller, self.menu_items[self.selected_idx]))
            else:
                self.navigate_back()
