"""
QuestionList

A list of questions.

"""

from tebogen.question import Question


class QuestionList:
    """
    A list of questions.

    Provides methods to add, remove, move, swap and iterate over the questions.

    Attributes:
        _questions (list[Question]): The list of questions.
    """

    _questions: list[Question]

    def __init__(self, questions: list[Question] | None = None):
        """
        Initializes the question list.

        Args:
            questions (list[Question] | None): The initial list of questions.
                If None, an empty list is created.
        """
        if questions is None:
            self._questions = []
        else:
            self._questions = questions

    def add(self, question: Question, index: int | None = None) -> None:
        """
        Adds a question to the question list at the given index.

        Args:
            question (Question): The question to be added.
            index (int, optional): The index to insert the question at.
            If not provided, the question is appended to the end of the list.
        """
        for q in self._questions:
            if q == question:
                raise ValueError("Question already exists")
        if index is None:
            self._questions.append(question)
        else:
            if index < 0 or index > len(self._questions):
                raise IndexError("Index out of range")
            self._questions.insert(index, question)

    def move(self, old_index: int, new_index: int) -> None:
        """
        Moves a question from the old index to the new index in the question list.

        Args:
            old_index (int): The current index of the question to be moved.
            new_index (int): The target index to move the question to.
        """
        if old_index < 0 or old_index >= len(self._questions):
            raise IndexError("Index out of range")
        if new_index < 0 or new_index >= len(self._questions):
            raise IndexError("Index out of range")
        element = self._questions.pop(old_index)
        self._questions.insert(new_index, element)

    def pop(self, index: int) -> Question:
        """
        Removes a question from the question list at the given index.

        Args:
            index (int): The index of the question to be removed.
        """
        if index < 0 or index >= len(self._questions):
            raise IndexError("Index out of range")
        return self._questions.pop(index)

    def swap(self, index1: int, index2: int) -> None:
        """
        Swaps two questions in the question list at the given indices.

        Args:
            index1 (int): The index of the first question to be swapped.
            index2 (int): The index of the second question to be swapped.
        """

        if index1 < 0 or index1 >= len(self._questions):
            raise IndexError("Index out of range")
        if index2 < 0 or index2 >= len(self._questions):
            raise IndexError("Index out of range")
        self._questions[index1], self._questions[index2] = (
            self._questions[index2],
            self._questions[index1],
        )

    def __iter__(self):
        """Support iteration (e.g., for question in questions)"""
        return iter(self._questions)

    def __getitem__(self, index):
        """Support indexing"""
        return self._questions[index]

    def __len__(self):
        """Support len() function"""
        return len(self._questions)

    def __repr__(self):
        """
        Return a string representation of the QuestionList.

        This is a string that would be a valid Python expression to recreate the
        QuestionList. It is also the string that is displayed when the
        QuestionList is printed.

        For example, if the QuestionList contains the questions q1 and q2, the
        string representation would be:

            QuestionList([q1, q2])

        Returns:
            str: The string representation of the QuestionList.
        """
        return f"QuestionList(_questions={self._questions})"

    def pretty_print(self, indent: int = 0, prefix: str = ""):
        """
        Prints a formatted representation of the questions in the list.

        Each question is printed with an optional indentation and a prefix followed by
        its index in the list. This method is useful for displaying the questions in a
        structured and human-readable format.

        Args:
            indent (int, optional): Number of indentations to apply before each question.
            prefix (str, optional): A string to prepend to each question's index.
        """
        for idx, question in enumerate(self._questions):
            print("  " * indent + f"{prefix}{idx}: {str(question.variable_name)}")

    def to_dict(self):
        """
        Converts the QuestionList to a dictionary representation.

        Returns:
            dict: A dictionary with a key "questions" containing a list of
            dictionaries, where each dictionary represents a question in the
            QuestionList.
        """
        return {"questions": [q.to_dict() for q in self._questions]}

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a QuestionList from a dictionary representation.

        Args:
            data (dict): A dictionary with a key "questions" containing a list of
                dictionaries, where each dictionary represents a question.

        Returns:
            QuestionList: A QuestionList populated with the questions from the
                dictionary.
        """
        questions = [Question.from_dict(q) for q in data["questions"]]
        return cls(questions)
