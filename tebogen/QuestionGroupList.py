from Question import Question
from Group import Group

class QuestionGroupList:

    _questions_and_groups : list[Question | Group] = []

    def __init__(self, questions_and_groups : list[Question | Group]):
        for element in questions_and_groups:
            if not isinstance(element, Question) and not isinstance(element, Group):
                raise TypeError("questions_and_groups must be a list of Question or Group instances")
        self._questions_and_groups = questions_and_groups

    def __repr__(self):
        return f"QuestionGroupList(questions_and_groups={self._questions_and_groups})"
    

    def add(self, value : Question | Group, index : int | None = None) -> None:
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
        
    def add_question_to_group(self, question : Question, group_index : int, index_in_group : int | None = None) -> None:
        if group_index < 0 or group_index >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        if not isinstance(self._questions_and_groups[group_index], Group):
            raise TypeError("Group not found")
        
        self._questions_and_groups[group_index].questions.add(question, index_in_group)

    def pop(self, index : int) -> None:
        if index < 0 or index >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        return self._questions_and_groups.pop(index)

    
    def ungroup_all_questions(self, group_index : int) -> None:
        if group_index < 0 or group_index >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        if not isinstance(self._questions_and_groups[group_index], Group):
            raise TypeError("Group not found")
        for question_index in range(len(self._questions_and_groups[group_index].questions)):
            question = self._questions_and_groups[group_index].questions.pop(0)
            self.add(question, group_index + question_index + 1)

    def ungroup_single_question(self, group_index : int, question_index : int) -> None:
        if group_index < 0 or group_index >= len(self._questions_and_groups):
            raise IndexError("Index out of range")
        if not isinstance(self._questions_and_groups[group_index], Group):
            raise TypeError("Group not found")
        if len(self._questions_and_groups[group_index].questions) <= question_index:
            raise IndexError("Index out of range")
        question = self._questions_and_groups[group_index].questions.pop(question_index)
        self.add(question, group_index+1)

    def move_question_to_group(self, question_index : int, group_index : int) -> None:
        if group_index < 0 or group_index >= len(self._questions_and_groups):
            raise IndexError("group_index out of range")
        if not isinstance(self._questions_and_groups[group_index], Group):
            raise TypeError("Group not found")
        if question_index < 0 or question_index >= len(self._questions_and_groups):
            raise IndexError("question_index out of range")
        if not isinstance(self._questions_and_groups[question_index], Question):
            raise TypeError("Question not found")
        
        question = self.pop(question_index)
        self._questions_and_groups[group_index].questions.add(question)

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
        return repr(self._questions_and_groups)
    
    def pretty_print(self):
        for idx, element in enumerate(self._questions_and_groups):
            if isinstance(element, Question):
                print(f"{idx}: {element.variable_name}")
            else:
                print(f"{idx}: {element.variable_name}")
                element.questions.pretty_print(indent=2, prefix=f"{idx}.")


    def to_dict(self):
        return [
                item.to_dict() for item in self._questions_and_groups
            ]
    
    @classmethod
    def from_dict(cls, data: dict):
        obj = cls(
                [
                Question.from_dict(item) if "questions" not in item else Group.from_dict(item)
                for item in data
                ]
        )
        
        return obj

