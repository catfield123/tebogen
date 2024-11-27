class BaseScreen:
    def __init__(self, stdscr, navigation_controller):
        self.stdscr = stdscr
        self.navigation_controller = navigation_controller

    def display(self):
        raise NotImplementedError("display() must be implemented in subclasses")

    def handle_input(self, key):
        raise NotImplementedError("handle_input() must be implemented in subclasses")

    def navigate_back(self):
        self.navigation_controller.go_back()
