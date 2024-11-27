import curses

class Colors:
    WHITE = curses.COLOR_WHITE
    RED = curses.COLOR_RED
    GREEN = curses.COLOR_GREEN
    BLACK = curses.COLOR_BLACK

    WHITE_BLACK = None
    BLACK_WHITE = None
    RED_BLACK = None
    GREEN_BLACK = None

    @staticmethod
    def init_colors():
        curses.init_pair(1, Colors.WHITE, Colors.BLACK)
        curses.init_pair(2, Colors.BLACK, Colors.WHITE)
        curses.init_pair(3, Colors.RED, Colors.BLACK)
        curses.init_pair(4, Colors.GREEN, Colors.BLACK)

        Colors.WHITE_BLACK = curses.color_pair(1)
        Colors.BLACK_WHITE = curses.color_pair(2)
        Colors.RED_BLACK = curses.color_pair(3)
        Colors.GREEN_BLACK = curses.color_pair(4)
