class ValidatorAlreadyExists(Exception):
    def __init__(self, name):
        self.name = name
        super().__init__(f"Validator '{name}' already exists.")
