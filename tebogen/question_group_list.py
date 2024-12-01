from typing import cast

from tebogen.exceptions.question_group_list_exceptions import BoundaryReachedException
from tebogen.group import Group
from tebogen.question import Question


class QuestionGroupList:

    _questions_and_groups: list[Question | Group] = []

    def __init__(self, questions_and_groups: list[Question | Group]):
        for element in questions_and_groups:
            if not isinstance(element, Question) and not isinstance(element, Group):
                raise TypeError(
                    "questions_and_groups must be a list of Question or Group instances"
                )
        self._questions_and_groups = questions_and_groups

    def add(self, value: Question | Group, index: int | None = None) -> None:
        if isinstance(value, Question):
            for element in self._questions_and_groups:
                if isinstance(element, Question) and element == value:
                    raise ValueError("Question already exists")
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
        if group_index < 0 or group_index >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        if not isinstance(self._questions_and_groups[group_index], Group):
            raise TypeError("Group not found")
        group = cast(Group, self._questions_and_groups[group_index])
        group.questions.add(question, index_in_group)

    def pop(self, index: int) -> Question | Group:
        if index < 0 or index >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        return self._questions_and_groups.pop(index)

    def ungroup_all_questions(self, group_index: int) -> None:
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

    def swap(self, index1: int, index2: int) -> None:
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
        return f"QuestionGroupList(questions_and_groups={repr(self._questions_and_groups)})"

    def pretty_print(self):
        for idx, element in enumerate(self._questions_and_groups):
            if isinstance(element, Question):
                print(f"{idx}: {element.variable_name}")
            else:
                print(f"{idx}: {element.variable_name}")
                element.questions.pretty_print(indent=2, prefix=f"{idx}.")

    def to_dict(self):
        return [item.to_dict() for item in self._questions_and_groups]

    @classmethod
    def from_dict(cls, data: dict):
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
