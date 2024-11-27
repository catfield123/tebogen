from Question import Question


class QuestionList:
    _questions : list[Question]

    def __init__(self, questions : list[Question] = []):
        self._questions = questions

    def add(self, question : Question, index : int | None = None) -> None:
        """
        Adds a question to the question list at the given index.

        Args:
            question (Question): The question to be added.
            index (int, optional): The index to insert the question at. If not provided, the question is appended to the end of the list.
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

    def move(self, old_index : int, new_index : int) -> None:
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


    def pop(self, index : int) -> None:
        """
        Removes a question from the question list at the given index.

        Args:
            index (int): The index of the question to be removed.
        """
        if index < 0 or index >= len(self._questions):
            raise IndexError("Index out of range")
        return self._questions.pop(index)

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
        return repr(self._questions)
    
    def pretty_print(self, indent : int = 0, prefix : str = ""):
        for idx, question in enumerate(self._questions):
            print("  " * indent + f"{prefix}{idx}: {str(question.variable_name)}")

    def to_dict(self):
        return {"questions": [q.to_dict() for q in self._questions]}
    
    @classmethod
    def from_dict(cls, data: dict):
        questions = [Question.from_dict(q) for q in data["questions"]]
        return cls(questions)