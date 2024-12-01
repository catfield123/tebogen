import curses

from tebogen.config_controller import ConfigController
from tebogen.ui.base_screen import BaseScreen
from tebogen.ui.NavigationController import NavigationController
from tebogen.ui.screens.questions.questions_list_screen import QuestionsListScreen
from tebogen.ui.screens.settings.SettingsMenuScreen import SettingsMenuScreen
from tebogen.ui.screens.validators.validators_list_screen import ValidatorsListScreen


class MainMenuScreen(BaseScreen):
    def __init__(
        self,
        stdscr,
        navigation_controller: NavigationController,
        config_controller: ConfigController,
    ):
        super().__init__(stdscr, navigation_controller, config_controller)
        self.menu_items = ["Settings", "Edit Questions", "Edit Validators", "Exit"]
        self.selected_idx = 0

    def display(self):
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
