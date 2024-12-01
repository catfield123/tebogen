"""
This module provides the QuestionsListScreen class for displaying a list of all questions in the application.

"""

import curses

from tebogen.colors import Colors
from tebogen.config_controller import ConfigController
from tebogen.exceptions.question_group_list_exceptions import BoundaryReachedException
from tebogen.group import Group
from tebogen.question import Question
from tebogen.ui.base_screen import BaseScreen
from tebogen.ui.navigation_controller_screen import NavigationController


class QuestionsListScreen(BaseScreen):
    """
    This class provides a screen for displaying a list of all questions in the application.

    It provides an interface for the user to navigate through the list of questions and
    select one to view or edit. It also provides an option to create a new question.

    Attributes:
        selected_idx (int): The index of the currently selected question.
    """

    def __init__(
        self,
        stdscr,
        navigation_controller: NavigationController,
        config_controller: ConfigController,
    ):
        """
        Initialize the QuestionsListScreen.

        Args:
            stdscr: The curses window to use for displaying the screen.
            navigation_controller (NavigationController): Manages navigation between screens.
            config_controller (ConfigController): Handles configuration management.

        Attributes:
            selected_idx (int): The index of the currently selected question or group.
            start_idx (int): The starting index for scrolling the question list.
            menu_items (list[tuple[Question | Group, int]]): A list of questions and groups with their indentation levels.
            is_moving (bool): Indicates whether a question or group is currently being moved.
        """
        super().__init__(stdscr, navigation_controller, config_controller)
        self.selected_idx: int = 0
        self.start_idx: int = 0
        self.menu_items: list[tuple[Question | Group, int]] = []
        self.fetch_questions_and_groups()
        self.is_moving: bool = False

    def fetch_questions_and_groups(self):
        """
        Recursively traverses the list of questions and groups from the config controller,
        and creates a flat list of tuples containing the question or group and its depth.
        It then calls `self.display()` to display the list.
        """
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
        """
        Renders the questions and groups list on the screen.

        This method clears the screen, and then renders the questions and groups
        list on the screen. It also handles displaying the currently selected
        item and the currently selected group.

        It also handles the indentation of the questions and groups based on
        their depth in the questions and groups tree.

        Finally, it handles displaying the validator name of each question and
        the number of questions in each group.

        It does not handle user input. User input is handled in the handle_input
        method.

        :return: None
        """
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        visible_items = height - 2
        end_idx = self.start_idx + visible_items

        self.stdscr.addstr(0, 0, "Questions and Groups")
        for idx, (item, depth) in enumerate(self.menu_items[self.start_idx : end_idx]):
            actual_idx = idx + self.start_idx

            indent = " " * (depth * 2)

            is_selected = actual_idx == self.selected_idx
            prefix = "> " if is_selected else "  "
            font_weight_attribute = (
                curses.A_BOLD | curses.A_UNDERLINE if is_selected else curses.A_NORMAL
            )
            self.stdscr.addstr(idx + 1, 0, f"{indent}{prefix}", Colors.WHITE_BLACK)

            if isinstance(item, Question):
                display_text = f"{item.variable_name}"
                self.stdscr.addstr(
                    idx + 1,
                    len(indent) + len(prefix),
                    f"{display_text}",
                    Colors.GREEN_BLACK | font_weight_attribute,
                )
            elif isinstance(item, Group):
                display_text = f"{item.variable_name}" + (
                    " (Empty group)" if len(item) == 0 else " (Group)"
                )
                self.stdscr.addstr(
                    idx + 1,
                    len(indent) + len(prefix),
                    f"{display_text}",
                    Colors.YELLOW_BLACK | font_weight_attribute,
                )
            if isinstance(item, Question) and item.validator is not None:
                self.stdscr.addstr(
                    idx + 1,
                    len(indent) + len(prefix) + len(display_text),
                    f" ({item.validator.name})",
                    Colors.BLUE_BLACK | font_weight_attribute,
                )

        self.stdscr.refresh()

    def handle_input(self, key):
        """
        Handle user input for the questions list screen.

        Args:
            key: The key pressed by the user. This determines the action to be taken.

        Actions:
            - Moves the selection up or down between the list of questions or groups.
            - Navigates to the previous screen when the Backspace key is pressed.
            - Toggles the selection mode when the Enter key is pressed.
            - Moves the selected question or group up or down when the Up or Down arrow keys
              are pressed, respectively, in selection mode.
        """
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
            elif (
                key == curses.KEY_DOWN and self.selected_idx < len(self.menu_items) - 1
            ):
                self.selected_idx += 1
                if self.selected_idx >= self.start_idx + visible_items:
                    self.start_idx += 1
            self.display()
        else:

            if key == curses.KEY_UP:
                try:
                    shift = self.config_controller.move_qustion_or_group_up(
                        self.menu_items[self.selected_idx][0].variable_name
                    )
                    self.selected_idx -= 1
                    self.selected_idx += shift
                    if self.selected_idx < self.start_idx:
                        self.start_idx = self.selected_idx
                    self.fetch_questions_and_groups()
                except BoundaryReachedException:
                    pass
            elif key == curses.KEY_DOWN:
                try:
                    shift = self.config_controller.move_qustion_or_group_down(
                        self.menu_items[self.selected_idx][0].variable_name
                    )
                    self.selected_idx += 1
                    self.selected_idx += shift
                    if self.selected_idx >= self.start_idx + visible_items:
                        self.start_idx = self.selected_idx - visible_items + 1
                    self.fetch_questions_and_groups()
                except BoundaryReachedException:
                    pass
