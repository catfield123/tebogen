"""
This module provides the QuestionsListScreen class for displaying a list of all questions in the application.

"""

import curses

from tebogen.colors import Colors
from tebogen.config_controller import ConfigController
from tebogen.exceptions.common import (
    NotValidPythonVariableNameException,
    PythonKeywordException,
)
from tebogen.exceptions.question_exceptions import QuestionAlreadyExistsException
from tebogen.question import Question
from tebogen.ui.base_screen import BaseScreen
from tebogen.ui.navigation_controller_screen import NavigationController
from tebogen.ui.screens.confirm_screen import ConfirmScreen
from tebogen.ui.screens.validators.choose_validator_screen import ChooseValidatorScreen
from tebogen.validators import Validator


class CreateOrEditQuestionScreen(BaseScreen):
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
        callback,
        question: Question | None = None,
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

        self.is_typing = False
        self.error_messages: list[str] = []

        self.is_moving: bool = False
        self.question: Question | None = question

        if self.question is not None:
            self.mode = "edit"
            self.edit_shift = 1
            self.name_field: str = self.question.name
            self.variable_name_field: str = self.question.variable_name
            self.validator_field: Validator | None = self.question.validator
        else:
            self.mode = "create"
            self.edit_shift = 0
            self.name_field: str = ""
            self.variable_name_field: str = ""
            self.validator_field: Validator | None = None

        self.callback = callback

    def display(self):

        self.stdscr.clear()

        if self.mode == "create":
            self.stdscr.addstr(0, 0, "Create question")
        if self.mode == "edit":
            self.stdscr.addstr(0, 0, "Edit question")

        self.stdscr.addstr(
            1,
            0,
            ("> " if (self.selected_idx == 0 and not self.is_typing) else "  ")
            + "Question name: "
            + self.name_field,
        )

        self.stdscr.addstr(
            2,
            0,
            ("> " if (self.selected_idx == 1 and not self.is_typing) else "  ")
            + "Question variable_name: "
            + self.variable_name_field,
        )

        self.stdscr.addstr(
            3,
            0,
            ("> " if (self.selected_idx == 2 and not self.is_typing) else "  ")
            + "Validator: "
            + (
                self.validator_field.name
                if self.validator_field is not None
                else "None"
            ),
        )

        self.stdscr.addstr(
            4, 0, ("> " if self.selected_idx == 3 else "  ") + "[Confirm]"
        )

        self.stdscr.addstr(
            5, 0, ("> " if self.selected_idx == 4 else "  ") + "[Cancel]"
        )

        if self.mode == "edit":
            self.stdscr.addstr(
                6,
                0,
                ("> " if self.selected_idx == 5 else "  ") + "[Delete]",
                Colors.RED_BLACK,
            )

        if len(self.error_messages) > 0:
            for i, message in enumerate(self.error_messages):
                self.stdscr.addstr(
                    7 + i - self.edit_shift, 0, f"  {message}", Colors.RED_BLACK
                )

        self.stdscr.refresh()

    def delete_symbol_from_field(self, selected_idx):
        if selected_idx == 0:
            self.name_field = self.name_field[:-1]
        elif selected_idx == 1:
            self.variable_name_field = self.variable_name_field[:-1]
        elif selected_idx == 2:
            self.validator_field = self.validator_field[:-1]

    def add_symbol_to_field(self, selected_idx, symbol):
        if selected_idx == 0:
            self.name_field += symbol
        elif selected_idx == 1:
            self.variable_name_field += symbol
        elif selected_idx == 2:
            self.validator_field += symbol

    def is_data_changed(self) -> bool:
        if self.mode == "create":
            return True
        elif self.mode == "edit":
            return not (
                self.question.name == self.name_field
                and self.question.variable_name == self.variable_name_field
                and self.question.validator == self.validator_field
            )

    def set_validator(self, validator: Validator | None):
        self.validator_field = validator

    def handle_input(self, key):
        if self.is_typing:
            if key in [curses.KEY_ENTER, 10, 13]:
                self.is_typing = False
            elif key in (curses.KEY_BACKSPACE, 127):
                self.delete_symbol_from_field(self.selected_idx)
            elif key >= 32 and key <= 126:
                self.add_symbol_to_field(self.selected_idx, chr(key))
            return

        if key == curses.KEY_UP and self.selected_idx > 0:
            self.selected_idx -= 1
        elif key == curses.KEY_DOWN and self.selected_idx < 4 + self.edit_shift:
            self.selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if self.selected_idx in [0, 1]:
                self.is_typing = True
            elif self.selected_idx == 2:  # Validator
                self.navigation_controller.navigate_to(
                    ChooseValidatorScreen(
                        self.stdscr,
                        self.navigation_controller,
                        self.config_controller,
                        callback=self.set_validator,
                    )
                )
            elif self.selected_idx == 3:  # Confirm
                self.name_field = self.name_field.strip()
                self.variable_name_field = self.variable_name_field.strip()
                self.error_messages = []

                if self.name_field == "":
                    self.error_messages.append("Question name cannot be empty")
                if self.variable_name_field == "":
                    self.error_messages.append("Question variable_name cannot be empty")
                if self.error_messages:
                    return
                try:
                    if not self.is_data_changed():
                        self.navigate_back()
                        return
                    else:
                        if self.mode == "create":
                            self.config_controller.add_question_or_group(
                                Question(
                                    self.name_field,
                                    self.variable_name_field,
                                    self.validator_field,
                                )
                            )
                        elif self.mode == "edit":
                            self.config_controller.update_question(
                                self.question,
                                self.name_field,
                                self.variable_name_field,
                                self.validator_field,
                            )
                        self.callback()
                        self.navigate_back()
                        return

                except QuestionAlreadyExistsException as e:
                    self.error_messages = [str(e)]
                except NotValidPythonVariableNameException as e:
                    self.error_messages = [str(e)]
                except PythonKeywordException as e:
                    self.error_messages = [str(e)]

            elif self.selected_idx == 4:  # Cancel
                self.navigate_back()

            elif self.selected_idx == 5:  # Delete
                self.navigation_controller.navigate_to(
                    ConfirmScreen(
                        self.stdscr,
                        self.navigation_controller,
                        self.config_controller,
                        confirm_callback=lambda: [
                            self.config_controller.delete_question(
                                self.question.variable_name
                            ),
                            self.callback(),
                            self.navigate_back(2),
                        ],
                        title="Delete Question",
                        message=f"Are you sure you want to delete question '{self.question.variable_name}'?",
                    )
                )
