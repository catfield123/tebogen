"""
This module provides the BaseScreen class, which is the base class for all screens
in the application. It provides a common interface for all screens and is used
to define the standard methods and behaviors for all screens.

"""

from tebogen.config_controller import ConfigController
from tebogen.ui.NavigationController import NavigationController


class BaseScreen:
    """
    Base class for all screens in the application.

    This class provides a common interface for all screens in the application.
    It contains methods for displaying the screen and handling user input.
    """

    def __init__(
        self,
        stdscr,
        navigation_controller: NavigationController,
        config_controller: ConfigController,
    ):
        self.stdscr = stdscr
        self.navigation_controller = navigation_controller
        self.config_controller = config_controller

    def display(self):
        """
        Displays the screen.

        This method must be implemented by subclasses of BaseScreen to
        display the contents of the screen. It should use the stdscr object
        provided in the constructor to draw the screen contents.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("display() must be implemented in subclasses")

    def handle_input(self, key):
        """
        Handle user input for the screen.

        Args:
            key: The key pressed by the user. This can be used to determine
                the action to be taken, such as navigation or selection.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("handle_input() must be implemented in subclasses")

    def navigate_back(self, amount: int = 1):
        """
        Navigate back to the previous screen.

        Args:
            amount (int): The number of screens to go back. Defaults to 1.
        """
        self.navigation_controller.go_back(amount=amount)
