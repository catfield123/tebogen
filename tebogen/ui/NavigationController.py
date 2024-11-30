class NavigationController:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.screens_stack = []

    def navigate_to(self, screen):
        self.screens_stack.append(screen)
        self.run_current_screen()

    def go_back(self, amount=1):
        if len(self.screens_stack) > amount:
            for _ in range(amount):
                self.screens_stack.pop()
            self.run_current_screen()
        else:
            self.exit_app()

    def run_current_screen(self):
        current_screen = self.screens_stack[-1]
        while True:
            current_screen.display()
            key = self.stdscr.getch()
            current_screen.handle_input(key)

    def exit_app(self):
        raise SystemExit("Exiting the application")
