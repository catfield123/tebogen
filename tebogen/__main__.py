import curses
from ui.NavigationController import NavigationController
from ui.screens.MainMenuScreen import MainMenuScreen
from Colors import Colors

def main(stdscr):
    Colors.init_colors()
    
    navigation_controller = NavigationController(stdscr)
    main_menu_screen = MainMenuScreen(stdscr, navigation_controller)
    navigation_controller.navigate_to(main_menu_screen)

def run():
    curses.wrapper(main)

if __name__ == "__main__":
    run()
