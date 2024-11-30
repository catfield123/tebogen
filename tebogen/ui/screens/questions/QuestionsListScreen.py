import curses
from ConfigController import ConfigController
from ui.NavigationController import NavigationController
from ui.BaseScreen import BaseScreen

class QuestionsListScreen(BaseScreen):
    def __init__(self, stdscr, navigation_controller: NavigationController, config_controller: ConfigController):
        super().__init__(stdscr, navigation_controller, config_controller)
        self.question_list = ["Question 1", "Question 2", "Question 3"]
        self.selected_idx = 0

    def display(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Questions")
        for idx, item in enumerate(self.question_list):
            if idx == self.selected_idx:
                self.stdscr.addstr(idx + 1, 0, f"> {item}")
            else:
                self.stdscr.addstr(idx + 1, 0, f"  {item}")
        self.stdscr.refresh()

    def handle_input(self, key):
        if key == curses.KEY_UP and self.selected_idx > 0:
            self.selected_idx -= 1
        elif key == curses.KEY_DOWN and self.selected_idx < len(self.question_list) - 1:
            self.selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            self.navigate_back()