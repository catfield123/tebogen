"""
A module providing a list-like container for managing a collection of Question and Group objects.

The QuestionGroupList class provides methods to add, remove, and manipulate questions and groups
within the list. It ensures that the list maintains a consistent order and allows
for operations like popping elements, moving elements up or down, and accessing
elements by index.
"""

from typing import cast

from tebogen.exceptions.question_exceptions import QuestionAlreadyExistsException
from tebogen.exceptions.question_group_list_exceptions import BoundaryReachedException
from tebogen.group import Group
from tebogen.question import Question
from tebogen.validators import Validator


class QuestionGroupList:
    """
    A list-like container for managing a collection of Question and Group objects.

    This class provides methods to add, remove, and manipulate questions and groups
    within the list. It ensures that the list maintains a consistent order and allows
    for operations like popping elements, moving elements up or down, and accessing
    elements by index.

    Attributes:
        _questions_and_groups (list[Question | Group]): The internal list holding
            the Question and Group objects.
    """

    _questions_and_groups: list[Question | Group] = []

    def __init__(self, questions_and_groups: list[Question | Group]):
        """
        Initializes the question and group list with the given list of questions and groups.

        Args:
            questions_and_groups (list[Question | Group]): A list of Question and Group instances.

        Raises:
            TypeError: If the given list contains an item that is neither a Question nor a Group instance.
        """
        for element in questions_and_groups:
            if not isinstance(element, Question) and not isinstance(element, Group):
                raise TypeError(
                    "questions_and_groups must be a list of Question or Group instances"
                )
        self._questions_and_groups = questions_and_groups

    def add(self, value: Question | Group, index: int | None = None) -> None:
        """
        Adds a question or group to the question and group list at the given index.

        Args:
            value (Question | Group): The question or group to be added.
            index (int, optional): The index to insert the question or group at.
                If not provided, the question or group is appended to the end of the list.

        Raises:
            ValueError: If a question or group already exists in the list.
            IndexError: If the index is out of range.
            TypeError: If the value is not a Question or Group instance.
        """
        if isinstance(value, Question):
            for element in self._questions_and_groups:
                if isinstance(element, Question) and element == value:
                    raise QuestionAlreadyExistsException(value.variable_name)
            if index is None:
                self._questions_and_groups.append(value)
            else:
                if index < 0 or index > len(self._questions_and_groups):
                    raise IndexError("Index out of range")
                self._questions_and_groups.insert(index, value)

        elif isinstance(value, Group):
            for element in self._questions_and_groups:
                if isinstance(element, Group) and element == value:
                    raise ValueError("Group already exists")
            if index is None:
                self._questions_and_groups.append(value)
            else:
                if index < 0 or index > len(self._questions_and_groups):
                    raise IndexError("Index out of range")
                self._questions_and_groups.insert(index, value)

        else:
            raise TypeError("value must be a Question or Group instance")

    def add_question_to_group(
        self, question: Question, group_index: int, index_in_group: int | None = None
    ) -> None:
        """
        Adds a question to a group in the question group list at the given index.

        Args:
            question (Question): The question to be added.
            group_index (int): The index of the group to add the question to.
            index_in_group (int | None): The index to insert the question at in the group.
                If None, the question is appended to the end of the group.

        Raises:
            IndexError: If the group index is out of range.
            TypeError: If the element at the given index is not a Group.
        """
        if group_index < 0 or group_index >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        if not isinstance(self._questions_and_groups[group_index], Group):
            raise TypeError("Group not found")
        group = cast(Group, self._questions_and_groups[group_index])
        group.questions.add(question, index_in_group)

    def pop(self, index: int) -> Question | Group:
        """
        Removes a question or group from the question group list at the given index.

        Args:
            index (int): The index of the question or group to be removed.

        Returns:
            Question | Group: The removed question or group.

        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0 or index >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        return self._questions_and_groups.pop(index)

    def ungroup_all_questions(self, group_index: int) -> None:
        """
        Removes all questions from a group and places them after the group in the question list.

        Args:
            group_index (int): The index of the group to ungroup.
        """
        if group_index < 0 or group_index >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        if not isinstance(self._questions_and_groups[group_index], Group):
            raise TypeError("Group not found")
        group = cast(Group, self._questions_and_groups[group_index])
        for question_index in range(len(group.questions)):
            question = group.questions.pop(0)
            self.add(question, group_index + question_index + 1)

    def ungroup_single_question(
        self, group_index: int, question_index: int, after: bool = True
    ) -> None:
        """
        Removes a single question from a group and places it after or before the group in the question list.

        Args:
            group_index (int): The index of the group to remove the question from.
            question_index (int): The index of the question to be removed from the group.
            after (bool, optional): If True (default), the question is placed after the group. If False, the question is placed before the group.

        Raises:
            IndexError: If the group or question index is out of range.
            TypeError: If the group at the given index is not a Group instance.
        """
        if group_index < 0 or group_index >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        if not isinstance(self._questions_and_groups[group_index], Group):
            raise TypeError("Group not found")
        group = cast(Group, self._questions_and_groups[group_index])
        if len(group.questions) <= question_index:
            raise IndexError("Index out of range")
        question = group.questions.pop(question_index)
        if after:
            self.add(question, group_index + 1)
        else:
            self.add(question, group_index)

    def move_question_to_group(
        self, question_index: int, group_index: int, index_in_group: int | None = None
    ) -> None:
        """
        Moves a question from the question list to a group.

        Args:
            question_index (int): The index of the question to be moved.
            group_index (int): The index of the group to move the question to.
            index_in_group (int, optional): The index to insert the question at in the group.
                If not provided, the question is appended to the end of the group.

        Raises:
            IndexError: If the question or group index is out of range.
            TypeError: If the question or group at the given index is not of the correct type.
        """
        if group_index < 0 or group_index >= len(self._questions_and_groups):
            raise IndexError("group_index out of range")
        if not isinstance(self._questions_and_groups[group_index], Group):
            raise TypeError("Group not found")
        if question_index < 0 or question_index >= len(self._questions_and_groups):
            raise IndexError("question_index out of range")
        if not isinstance(self._questions_and_groups[question_index], Question):
            raise TypeError("Question not found")

        question = cast(Question, self.pop(question_index))
        shift = -1 if question_index < group_index else 0
        group = cast(Group, self._questions_and_groups[group_index + shift])
        group.questions.add(question, index=index_in_group)

    def has_element(self, variable_name: str) -> bool:
        for element in self._questions_and_groups:
            if isinstance(element, Question) and element.variable_name == variable_name:
                return True, Question
            if isinstance(element, Group):
                if element.variable_name == variable_name:
                    return True, Group
                for sub_element in element.questions:
                    if sub_element.variable_name == variable_name:
                        return True, Question
        return False, None

    def find_element(self, variable_name: str):
        """
        Find element by variable_name.
        Returns (idx, sub_idx) where idx is the index in the top-level list,
        and sub_idx is the index inside the group (if applicable), otherwise None.
        """
        for idx, element in enumerate(self._questions_and_groups):
            if isinstance(element, Question) and element.variable_name == variable_name:
                return idx, None
            if isinstance(element, Group):
                if element.variable_name == variable_name:
                    return idx, None
                for sub_idx, sub_element in enumerate(element.questions):
                    if sub_element.variable_name == variable_name:
                        return idx, sub_idx
        raise ValueError("Element not found")

    def move_down(self, variable_name: str) -> int:
        """
        Moves a question or group down within the question group list.

        This function attempts to move the element identified by the
        provided variable name down in the list. If the element is a group,
        it swaps the group with the preceding element if possible. If the
        element is a question, it swaps the question with the preceding
        element or moves it into the preceding group if applicable.

        Args:
            variable_name (str): The variable name of the question or group
                                to be moved.

        Returns:
            int: The shift in position. A return value of 0 indicates no
                change in level, a positive value indicates a move into
                a group, and a negative value indicates a move out of a
                group.

        Raises:
            BoundaryReachedException: If the element is already at the top
                                    of the list or group and cannot be
                                    moved further up.
            RuntimeError: If an unexpected state occurs where the move
                        logic cannot be determined.
        """
        idx, sub_idx = self.find_element(variable_name)

        if sub_idx is None:  # Top-level element
            if isinstance(self._questions_and_groups[idx], Group):
                # Move group down
                if idx < len(self._questions_and_groups) - 1:
                    self.swap(idx, idx + 1)
                    if isinstance(self._questions_and_groups[idx], Group):
                        return len(self._questions_and_groups[idx])
                    return 0
                raise BoundaryReachedException
            if isinstance(self._questions_and_groups[idx], Question):
                # Move question down or into the next group
                if idx < len(self._questions_and_groups) - 1:
                    if isinstance(self._questions_and_groups[idx + 1], Question):
                        self.swap(idx, idx + 1)
                        return 0
                    if isinstance(self._questions_and_groups[idx + 1], Group):
                        self.move_question_to_group(idx, idx + 1, 0)
                        return 0
                raise BoundaryReachedException
        else:  # Inside a group
            group = self._questions_and_groups[idx]
            if sub_idx < len(group) - 1:
                # Move question down within the group
                group.swap(sub_idx, sub_idx + 1)
                return 0
            else:
                # Move question out of the group
                self.ungroup_single_question(idx, sub_idx, after=True)
                return -1
        raise RuntimeError("Unexpected state: failed to determine move_down logic")

    def move_up(self, variable_name: str) -> int:
        """
        Moves a question or group up within the question group list.

        This function attempts to move the element identified by the
        provided variable name up in the list. If the element is a group,
        it swaps the group with the preceding element if possible. If the
        element is a question, it swaps the question with the preceding
        element or moves it into the preceding group if applicable.

        Args:
            variable_name (str): The variable name of the question or group
                                to be moved.

        Returns:
            int: The shift in position. A return value of 0 indicates no
                change in level, a positive value indicates a move into
                a group, and a negative value indicates a move out of a
                group.

        Raises:
            BoundaryReachedException: If the element is already at the top
                                    of the list or group and cannot be
                                    moved further up.
            RuntimeError: If an unexpected state occurs where the move
                        logic cannot be determined.
        """
        idx, sub_idx = self.find_element(variable_name)

        if sub_idx is None:  # Top-level element
            if isinstance(self._questions_and_groups[idx], Group):
                # Move group up
                if idx > 0:
                    self.swap(idx, idx - 1)
                    if isinstance(self._questions_and_groups[idx], Group):
                        return -len(self._questions_and_groups[idx])
                    return 0
                else:
                    raise BoundaryReachedException
            elif isinstance(self._questions_and_groups[idx], Question):
                # Move question up or into the previous group
                if idx > 0:
                    if isinstance(self._questions_and_groups[idx - 1], Question):
                        self.swap(idx, idx - 1)
                        return 0
                    if isinstance(self._questions_and_groups[idx - 1], Group):
                        self.move_question_to_group(idx, idx - 1)
                        return 1
                else:
                    raise BoundaryReachedException
        else:  # Inside a group
            group = self._questions_and_groups[idx]
            if sub_idx > 0:
                # Move question up within the group
                group.swap(sub_idx, sub_idx - 1)
                return 0
            else:
                # Move question out of the group
                self.ungroup_single_question(idx, sub_idx, after=False)
                return 0
        raise RuntimeError("Unexpected state: failed to determine move_up logic")

    def delete_question(self, variable_name: str) -> None:
        idx, sub_idx = self.find_element(variable_name)
        if sub_idx is not None:
            self.ungroup_single_question(idx, sub_idx, before=True)
            self.pop(idx)
        else:
            if isinstance(self._questions_and_groups[idx], Question):
                self._questions_and_groups.pop(idx)
            else:
                raise ValueError("Element is not a question")

    def delete_group(self, variable_name: str) -> None:
        idx, sub_idx = self.find_element(variable_name)
        if sub_idx is not None:
            raise ValueError("Element is not a group")
        else:
            if isinstance(self._questions_and_groups[idx], Group):
                self._questions_and_groups.pop(idx)
            else:
                raise ValueError("Element is not a group")

    def update_question(
        self,
        question: Question,
        new_name: str,
        new_variable_name: str,
        new_validator: Validator | None,
    ) -> None:
        idx, sub_idx = self.find_element(question.variable_name)
        if sub_idx is not None:
            question = self._questions_and_groups[idx][sub_idx]
        else:
            question = self._questions_and_groups[idx]

        if (
            new_variable_name != question.variable_name
            and not self.has_element(new_variable_name)[0]
        ):
            question.variable_name = new_variable_name
        elif (
            new_variable_name != question.variable_name
            and self.has_element(new_variable_name)[0]
        ):
            raise QuestionAlreadyExistsException(new_variable_name)

        question.name = new_name
        question.validator = new_validator

        if sub_idx is not None:
            self._questions_and_groups[idx][sub_idx] = question
        else:
            self._questions_and_groups[idx] = question

    def swap(self, index1: int, index2: int) -> None:
        """
        Swaps two elements in the question group list at the given indices.

        Args:
            index1 (int): The index of the first element to be swapped.
            index2 (int): The index of the second element to be swapped.

        Raises:
            IndexError: The index is out of range.
        """
        if index1 < 0 or index1 >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        if index2 < 0 or index2 >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        self._questions_and_groups[index1], self._questions_and_groups[index2] = (
            self._questions_and_groups[index2],
            self._questions_and_groups[index1],
        )

    def __iter__(self):
        """Support iteration"""
        return iter(self._questions_and_groups)

    def __getitem__(self, index):
        """Support indexing"""
        return self._questions_and_groups[index]

    def __len__(self):
        """Support len() function"""
        return len(self._questions_and_groups)

    def __repr__(self):
        """
        Return a string representation of the QuestionGroupList instance.

        The representation includes the list of questions and groups in the
        QuestionGroupList, formatted as a string for debugging and logging
        purposes.

        Returns:
            str: A string representation of the QuestionGroupList instance.
        """
        return f"QuestionGroupList(_questions_and_groups={repr(self._questions_and_groups)})"

    def pretty_print(self):
        """
        Pretty print the QuestionGroupList instance.

        Prints the list of questions and groups. If an element is a Group,
        it will print the variable name of the group, and then recursively
        call the pretty_print method on the QuestionList instance inside
        the group.

        Args:
            None

        Returns:
            None
        """
        for idx, element in enumerate(self._questions_and_groups):
            if isinstance(element, Question):
                print(f"{idx}: {element.variable_name}")
            else:
                print(f"{idx}: {element.variable_name}")
                element.questions.pretty_print(indent=2, prefix=f"{idx}.")

    def to_dict(self):
        """
        Convert a QuestionGroupList instance to a list of dicts.

        :return: A list of dicts where each dict must contain either "questions" key or
            represent a question.
        """
        return [item.to_dict() for item in self._questions_and_groups]

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a QuestionGroupList from a list of dicts.

        :param data: list of dicts where each dict must contain either "questions" key or
            represent a question.
        :return: QuestionGroupList instance
        :raises ValueError: if unable to parse question
        """
        questions_and_groups = []
        for item in data:
            if "questions" in item:
                questions_and_groups.append(Group.from_dict(item))
            else:
                try:
                    questions_and_groups.append(Question.from_dict(item))
                except:
                    raise ValueError(f"Unable to parse question: {item}")
        obj = cls(questions_and_groups)

        return obj
