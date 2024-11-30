from ConfigController import ConfigController
from ui.NavigationController import NavigationController

class BaseScreen:
    def __init__(self, stdscr, navigation_controller: NavigationController, config_controller: ConfigController):
        self.stdscr = stdscr
        self.navigation_controller = navigation_controller
        self.config_controller = config_controller

    def display(self):
        raise NotImplementedError("display() must be implemented in subclasses")

    def handle_input(self, key):
        raise NotImplementedError("handle_input() must be implemented in subclasses")

    def navigate_back(self, amount : int= 1):
        self.navigation_controller.go_back(amount=amount)
