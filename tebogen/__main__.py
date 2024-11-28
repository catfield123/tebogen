import argparse
import curses

from Colors import Colors

from ui.NavigationController import NavigationController
from ui.screens.MainMenuScreen import MainMenuScreen
from ConfigController import ConfigController

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

    # navigation_controller = NavigationController(stdscr)
    # main_menu_screen = MainMenuScreen(stdscr, navigation_controller)
    # navigation_controller.navigate_to(main_menu_screen)

    stdscr.getch()
def configure(config_filename):
    curses.wrapper(main, config_filename)


def generate(config_filename):
    print(f"Generated based on {config_filename}")


def run():
    # Основной парсер
    parser = argparse.ArgumentParser(
        description="Tebogen: a powerful tool for creating data-collecting Telegram bots."
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        default=None,  # Позже обработаем значение по умолчанию
        help="Path to configuration file."
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Команда configure
    configure_parser = subparsers.add_parser(
        "configure",
        help="Run configuration wizard."
    )

    # Команда generate
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate data based on configuration."
    )

    args = parser.parse_args()

    # Логика определения команды по умолчанию
    if args.command is None:
        args.command = "configure"

    # Устанавливаем значение по умолчанию для файла
    if args.file is None:
        args.file = "tebogen_config.json"

    # Выполняем команды
    if args.command == "configure":
        configure(args.file)
    elif args.command == "generate":
        generate(args.file)


if __name__ == "__main__":
    run()