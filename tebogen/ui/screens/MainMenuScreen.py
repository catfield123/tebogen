import curses
from ui.BaseScreen import BaseScreen

from ui.screens.settings.SettingsMenuScreen import SettingsMenuScreen
from ui.screens.questions.QuestionsListScreen import QuestionsListScreen
from ui.screens.validators.ValidatorsListScreen import ValidatorsListScreen


class MainMenuScreen(BaseScreen):
    def __init__(self, stdscr, navigation_controller):
        super().__init__(stdscr, navigation_controller)
        self.menu_items = ["Settings", "Edit Questions", "Edit Validators", "Exit"]
        self.selected_idx = 0

    def display(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Main Menu")
        for idx, item in enumerate(self.menu_items):
            if idx == self.selected_idx:
                self.stdscr.addstr(idx + 1, 0, f"> {item}")
            else:
                self.stdscr.addstr(idx + 1, 0, f"  {item}")
        self.stdscr.refresh()

    def handle_input(self, key):
        if key == curses.KEY_UP and self.selected_idx > 0:
            self.selected_idx -= 1
        elif key == curses.KEY_DOWN and self.selected_idx < len(self.menu_items) - 1:
            self.selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if self.selected_idx == 0:  # Settings
                self.navigation_controller.navigate_to(SettingsMenuScreen(self.stdscr, self.navigation_controller))
            elif self.selected_idx == 1:  # Edit Questions
                self.navigation_controller.navigate_to(QuestionsListScreen(self.stdscr, self.navigation_controller))
            elif self.selected_idx == 2:  # Edit Validators
                self.navigation_controller.navigate_to(ValidatorsListScreen(self.stdscr, self.navigation_controller))
            elif self.selected_idx == 3:  # Exit
                self.navigation_controller.exit_app()
