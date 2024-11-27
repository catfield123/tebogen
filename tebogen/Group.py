import utils
from Question import Question
from QuestionList import QuestionList


class Group:
    _name : str
    _variable_name : str
    _questions : QuestionList

    def __init__(self, name: str, variable_name: str, questions: list[Question] = []):
        self._name = name
        self._variable_name = variable_name
        self._questions = QuestionList(questions)

    def __repr__(self):
        return f"Group(name={self._name}, variable_name={self._variable_name}, questions={self._questions})"
    
    def __eq__(self, other):
        if not isinstance(other, Group):
            return NotImplemented
        return self._name == other._name or self._variable_name == other._variable_name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value : str):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self._name = value

    @property
    def variable_name(self):
        return self._variable_name
    
    @variable_name.setter
    def variable_name(self, value : str):
        if not isinstance(value, str):
            raise TypeError("variable_name must be a string")
        if utils.is_valid_python_variable_name(value):
            self._variable_name = value

    @property
    def questions(self) -> QuestionList:
        return self._questions

    def to_dict(self):
        return {
            "name": self._name,
            "variable_name": self._variable_name,
            "questions": [q.to_dict() for q in self._questions],
        }