"""
This module provides the NavigationController class for managing the UI navigation.

The NavigationController class is responsible for managing the navigation between
different UI screens. It uses the curses library to create a window for rendering
the UI screens and provides methods to navigate between screens and handle events.

"""


class NavigationController:
    """
    A class for managing the navigation between different UI screens.

    The NavigationController class provides methods to navigate between screens
    and handle events. It uses the curses library to create a window for rendering
    the UI screens.

    Attributes:
        stdscr: The curses window to use.
        screens_stack: A stack of BaseScreen instances. The last item in the list
            is the current screen.

    """

    def __init__(self, stdscr):
        """
        Initialize a new NavigationController.

        Args:
            stdscr: The curses window to use.

        Attributes:
            stdscr: The curses window to use.
            screens_stack: A stack of BaseScreen instances. The last item in the list
                is the current screen.
        """
        self.stdscr = stdscr
        self.screens_stack = []

    def navigate_to(self, screen):
        """
        Navigate to a new screen.

        This method appends the given screen to the stack of screens and
        runs the new current screen.

        Args:
            screen: The screen to navigate to.
        """
        self.screens_stack.append(screen)
        self.run_current_screen()

    def go_back(self, amount=1):
        """
        Navigates back in the screen stack by a specified amount.

        This method removes the specified number of screens from the top of the
        screens stack. If the stack contains more screens than the specified amount,
        it removes the screens and runs the current screen. If the stack has fewer
        than or equal to the specified amount of screens, it exits the application.

        Args:
            amount (int): The number of screens to go back. Defaults to 1.
        """
        if len(self.screens_stack) > amount:
            for _ in range(amount):
                self.screens_stack.pop()
            self.run_current_screen()
        else:
            self.exit_app()

    def run_current_screen(self):
        """
        Runs the current screen. It will display the screen and wait for input.
        Each input will be passed to the screen's handle_input method.
        """
        current_screen = self.screens_stack[-1]
        while True:
            current_screen.display()
            key = self.stdscr.getch()
            current_screen.handle_input(key)

    def exit_app(self):
        """
        Exits the application by raising a SystemExit exception.

        This method is called to terminate the program and release any
        resources in use. It clears the screen stack and ensures a clean
        shutdown of the application.
        """
        raise SystemExit("Exiting the application")
