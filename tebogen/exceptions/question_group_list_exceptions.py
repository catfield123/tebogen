class BoundaryReachedException(Exception):
    def __init__(self):
        super().__init__("Boundary reached.")
