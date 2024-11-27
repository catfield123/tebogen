import curses
from Colors import Colors

def main(stdscr):
    Colors.init_colors()
    stdscr.clear()
    stdscr.addstr(0, 0, "Hi, i'm tebogen!", Colors.RED_BLACK)
    stdscr.addstr(1, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()

def run():
    curses.wrapper(main)

if __name__ == "__main__":
    run()
