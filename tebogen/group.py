"""
A module providing a class for managing a group of questions.

The Group class contains a question list and provides methods to manage the questions
in the list. It also provides methods to get and set the questions in the list.
"""

import tebogen.utils as utils
from tebogen.question import Question
from tebogen.question_list import QuestionList


class Group:
    """
    A group of questions.

    A group is a collection of questions that are related to each other and
    are presented to the user together. A group can be used to group questions
    by topic or to group questions that should be answered together.

    Attributes:
        name (str): The name of the group.
        variable_name (str): The variable name of the group.
        questions (QuestionList): The list of questions in the group.
    """

    _name: str
    _variable_name: str
    _questions: QuestionList

    def __init__(self, name: str, variable_name: str, questions: list[Question] = []):
        """
        Initializes a Group instance.

        Args:
            name (str): The name of the group.

            variable_name (str): The variable name of the group.

            questions (list[Question], optional): The initial list of questions.
                If not provided, an empty list is used.
        """
        self._name = name
        self._variable_name = variable_name
        self._questions = QuestionList(questions)

    def __repr__(self):
        """
        Return a string representation of the Group.

        This is a string that would be a valid Python expression to recreate the
        Group. It is also the string that is displayed when the Group is
        printed.

        Returns:
            str: A string representation of the Group.
        """
        return f"Group(name={self._name}, variable_name={self._variable_name}, questions={self._questions})"

    def __eq__(self, other):
        """
        Compare this Group with another object for equality.

        Args:
            other (Group): The object to compare with.

        Returns:
            bool: True if the 'other' is a Group instance and has the same
            name or variable name. Otherwise, False.
        """
        if not isinstance(other, Group):
            return NotImplemented
        return self._name == other._name or self._variable_name == other._variable_name

    @property
    def name(self):
        """
        The name of this group.

        Returns:
            str: The name of the group.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """
        The name of this group.

        Args:
            value (str): The name to set.

        Raises:
            TypeError: If the provided name is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self._name = value

    @property
    def variable_name(self):
        """
        The variable name for this group.

        The variable name is expected to be a valid Python variable name.
        """
        return self._variable_name

    @variable_name.setter
    def variable_name(self, value: str):
        """
        The variable name for this group.

        The variable name is expected to be a valid Python variable name.

        Args:
            value (str): The variable name to set.

        Raises:
            TypeError: If the provided variable name is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("variable_name must be a string")
        if utils.is_valid_python_variable_name(value):
            self._variable_name = value

    @property
    def questions(self) -> QuestionList:
        """
        The questions in the group.

        Returns:
            QuestionList: A QuestionList containing all the questions in the group.
        """
        return self._questions

    def __iter__(self):
        """
        Returns an iterator over the questions in the group.

        Yields:
            Question: A question in the group.
        """
        return iter(self._questions)

    def __len__(self):
        """
        Returns the number of questions in the group.

        Returns:
            int: The number of questions in the group.
        """
        return len(self._questions)

    def to_dict(self):
        """
        Converts the Group to a dictionary representation.

        Returns:
            dict: A dictionary with keys "name", "variable_name", and "questions".
                  The "questions" key contains a list of dictionaries, where each
                  dictionary represents a question in the Group.
        """
        return {
            "name": self._name,
            "variable_name": self._variable_name,
            "questions": [q.to_dict() for q in self._questions],
        }

    def swap(self, index1: int, index2: int) -> None:
        """
        Swaps two questions in the group at the given indices.

        Args:
            index1 (int): The index of the first question to be swapped.
            index2 (int): The index of the second question to be swapped.

        Raises:
            IndexError: If either index is out of range.
        """
        self.questions.swap(index1, index2)

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a Group from a dictionary representation.

        Args:
            data (dict): A dictionary with keys "name", "variable_name", and
                "questions" containing a list of dictionaries, where each
                dictionary represents a question.

        Returns:
            Group: A Group populated with the questions from the dictionary.

        Raises:
            ValueError: If the dictionary does not contain the required keys.
        """
        questions = [Question.from_dict(q) for q in data["questions"]]
        if not data.get("name"):
            raise ValueError(f"Unable to parse group name. Provided data: {data}")
        if not data.get("variable_name"):
            raise ValueError(
                f"Unable to parse group variable name. Provided data: {data}"
            )
        return cls(
            name=data["name"],
            variable_name=data["variable_name"],
            questions=questions,
        )
