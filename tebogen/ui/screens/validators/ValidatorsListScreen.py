from ui.BaseScreen import BaseScreen
import curses

class ValidatorsListScreen(BaseScreen):
    def __init__(self, stdscr, navigation_controller):
        super().__init__(stdscr, navigation_controller)
        self.menu_items = ["[Create custom validator]", "Validator 1", "Validator 2", "Validator 3"]
        self.selected_idx = 0

    def display(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Validators")
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
            self.navigate_back()