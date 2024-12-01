from tebogen.ConfigController import ConfigController
from tebogen.Colors import Colors
from tebogen.Question import Question
from tebogen.Group import Group
from tebogen.exceptions.QuestionGroupListExceptions import BoundaryReachedException
from tebogen.ui.NavigationController import NavigationController

from tebogen.ui.BaseScreen import BaseScreen
import curses


class QuestionsListScreen(BaseScreen):
    def __init__(self, stdscr, navigation_controller: NavigationController, config_controller: ConfigController):
        super().__init__(stdscr, navigation_controller, config_controller)
        self.selected_idx = 0
        self.start_idx = 0
        self.menu_items = []
        self.fetch_questions_and_groups()
        self.is_moving = False

    def fetch_questions_and_groups(self):

        self.menu_items = []
        def process_item(item, depth=0):
            if isinstance(item, Question):
                self.menu_items.append((item, depth))
            elif isinstance(item, Group):
                self.menu_items.append((item, depth))
                for question in item:
                    process_item(question, depth + 1)

        for item in self.config_controller.questions_and_groups:
            process_item(item)

        self.display()

    def display(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        visible_items = height - 2
        end_idx = self.start_idx + visible_items

        self.stdscr.addstr(0, 0, "Questions and Groups")
        for idx, (item, depth) in enumerate(self.menu_items[self.start_idx:end_idx]):
            actual_idx = idx + self.start_idx

            indent = " " * (depth*2)
            
            is_selected = actual_idx == self.selected_idx
            prefix = "> " if is_selected else "  "
            font_weight_attribute = curses.A_BOLD | curses.A_UNDERLINE if is_selected else   curses.A_NORMAL
            self.stdscr.addstr(idx + 1, 0, f"{indent}{prefix}", Colors.WHITE_BLACK)

            if isinstance(item, Question):
                display_text = f"{item.variable_name}"
                self.stdscr.addstr(idx + 1, len(indent)+len(prefix), f"{display_text}", Colors.GREEN_BLACK | font_weight_attribute)
            elif isinstance(item, Group):
                display_text = f"{item.variable_name}" + (" (Empty group)" if len(item) == 0 else " (Group)")
                self.stdscr.addstr(idx + 1,  len(indent)+len(prefix), f"{display_text}", Colors.YELLOW_BLACK | font_weight_attribute)
            if isinstance(item, Question) and item.validator is not None:
                self.stdscr.addstr(idx + 1, len(indent)+len(prefix)+len(display_text), f" ({item.validator.name})", Colors.BLUE_BLACK | font_weight_attribute)

        self.stdscr.refresh()

    def handle_input(self, key):
        height, _ = self.stdscr.getmaxyx()
        visible_items = height - 2

        if key == curses.KEY_ENTER or key in [10, 13]:
            self.is_moving = not self.is_moving
            
            if not self.is_moving:
                if self.selected_idx < self.start_idx:
                    self.start_idx = self.selected_idx
                elif self.selected_idx >= self.start_idx + visible_items:
                    self.start_idx = self.selected_idx - visible_items + 1
                self.display()

        elif key == curses.KEY_BACKSPACE:
            self.navigate_back()

        if not self.is_moving:
            
            if key == curses.KEY_UP and self.selected_idx > 0:
                self.selected_idx -= 1
                if self.selected_idx < self.start_idx:
                    self.start_idx -= 1
            elif key == curses.KEY_DOWN and self.selected_idx < len(self.menu_items) - 1:
                self.selected_idx += 1
                if self.selected_idx >= self.start_idx + visible_items:
                    self.start_idx += 1
            self.display()
        else:
            
            if key == curses.KEY_UP:
                try:
                    shift = self.config_controller.move_qustion_or_group_up(self.menu_items[self.selected_idx][0].variable_name)
                    self.selected_idx -= 1
                    self.selected_idx += shift
                    if self.selected_idx < self.start_idx:
                        self.start_idx = self.selected_idx
                    self.fetch_questions_and_groups()
                except BoundaryReachedException:
                    pass
            elif key == curses.KEY_DOWN:
                try:
                    shift = self.config_controller.move_qustion_or_group_down(self.menu_items[self.selected_idx][0].variable_name)
                    self.selected_idx += 1
                    self.selected_idx += shift
                    if self.selected_idx >= self.start_idx + visible_items:
                        self.start_idx = self.selected_idx - visible_items + 1
                    self.fetch_questions_and_groups()
                except BoundaryReachedException:
                    pass
