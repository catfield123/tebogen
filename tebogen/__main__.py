import argparse
import curses

from tebogen.colors import Colors
from tebogen.config_controller import ConfigController
from tebogen.ui.navigation_controller_screen import NavigationController
from tebogen.ui.screens.main_menu_screen import MainMenuScreen


def main(stdscr, config_filename: str):
    Colors.init_colors()
    config_controller = ConfigController.load_from_file(config_filename)
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
        help="Command to run (default: configure).",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="tebogen_config.json",
        help="Path to configuration file (default: tebogen_config.json).",
    )

    args = parser.parse_args()

    if args.command == "configure":
        configure(args.file)
    elif args.command == "generate":
        generate(args.file)


if __name__ == "__main__":
    run()
