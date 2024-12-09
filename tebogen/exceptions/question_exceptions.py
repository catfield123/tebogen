class QuestionAlreadyExistsException(Exception):
    def __init__(self, variable_name):
        """
        Initialize a ValidatorAlreadyExists exception.

        Args:
            name (str): The name of the validator that already exists.
        """
        self.variable_name = variable_name
        super().__init__(
            f"Question with variable_name '{variable_name}' already exists."
        )
