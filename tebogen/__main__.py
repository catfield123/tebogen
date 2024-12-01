import argparse
import curses

from tebogen.Colors import Colors

from tebogen.ui.NavigationController import NavigationController
from tebogen.ui.screens.MainMenuScreen import MainMenuScreen
from tebogen.ConfigController import ConfigController

def main(stdscr, config_filename : str):
    Colors.init_colors()
    
    
    try:
        config_controller = ConfigController.load_from_file(config_filename)
    except:
        config_controller = ConfigController(False, False, config_filename = config_filename)


    stdscr.clear()
    stdscr.addstr(0, 0, f"{config_filename=}")
    stdscr.refresh()
    config_controller.save_to_file()

    navigation_controller = NavigationController(stdscr)
    main_menu_screen = MainMenuScreen(stdscr, navigation_controller, config_controller)
    navigation_controller.navigate_to(main_menu_screen)

    stdscr.getch()
def configure(config_filename):
    curses.wrapper(main, config_filename)


def generate(config_filename):
    print(f"Generated based on {config_filename}")


def run():
    parser = argparse.ArgumentParser(
        description="Tebogen: a powerful tool for creating data-collecting Telegram bots."
    )
    parser.add_argument(
        "command",
        nargs="?", 
        choices=["configure", "generate"],
        default="configure",
        help="Command to run (default: configure)."
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        default="tebogen_config.json",
        help="Path to configuration file (default: tebogen_config.json)."
    )

    args = parser.parse_args()

    if args.command == "configure":
        configure(args.file)
    elif args.command == "generate":
        generate(args.file)


if __name__ == "__main__":
    run()