import curses

def main(stdscr):
    # Настройка curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.clear()
    stdscr.addstr(0, 0, "Hi, i'm tebogen!", curses.color_pair(1))
    stdscr.addstr(1, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()

def run():
    # Обёртка для корректного запуска curses
    curses.wrapper(main)

if __name__ == "__main__":
    run()
