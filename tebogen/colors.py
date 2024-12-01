"""
This module defines the Colors class, which contains color constants used for UI elements.

The Colors class provides a centralized location for defining and managing the color
constants used throughout the application. These constants are used to set the
foreground and background colors of various UI elements, ensuring a consistent
appearance across different screens and components.
"""

import curses


class Colors:
    """
    Class containing all color constants.

    This class contains all color constants used in the application. The
    constants are used to define the colors of the different elements in the UI.
    The constants are used to define the colors of the following elements:

        - WHITE
        - RED
        - GREEN
        - BLACK
        - YELLOW
        - BLUE

    The class also contains some pre-defined color pairs:

        - WHITE_BLACK
        - BLACK_WHITE
        - RED_BLACK

    The pre-defined color pairs are used to define the colors of the different
    elements in the UI. The pre-defined color pairs are used to define the colors
    of the following elements:

        - WHITE_BLACK: The color of the default text.
        - BLACK_WHITE: The color of the highlighted text.
        - RED_BLACK: The color of the error messages.
    """

    WHITE = curses.COLOR_WHITE
    RED = curses.COLOR_RED
    GREEN = curses.COLOR_GREEN
    BLACK = curses.COLOR_BLACK
    YELLOW = curses.COLOR_YELLOW
    BLUE = curses.COLOR_BLUE

    WHITE_BLACK = None
    BLACK_WHITE = None
    RED_BLACK = None
    GREEN_BLACK = None
    YELLOW_BLACK = None
    BLUE_BLACK = None

    @staticmethod
    def init_colors() -> None:
        """
        Initializes color pairs for the application.

        This method sets up the curses color pairs using the defined colors in the
        Colors class. It maps each color pair to a unique identifier and assigns the
        corresponding curses color pair to the pre-defined color constants.

        The following color pairs are initialized:
            - WHITE_BLACK: White text on black background.
            - BLACK_WHITE: Black text on white background.
            - RED_BLACK: Red text on black background.
            - GREEN_BLACK: Green text on black background.
            - YELLOW_BLACK: Yellow text on black background.
            - BLUE_BLACK: Blue text on black background.

        After initialization, these color pairs can be used throughout the
        application for consistent styling of text elements.
        """
        curses.init_pair(1, Colors.WHITE, Colors.BLACK)
        curses.init_pair(2, Colors.BLACK, Colors.WHITE)
        curses.init_pair(3, Colors.RED, Colors.BLACK)
        curses.init_pair(4, Colors.GREEN, Colors.BLACK)
        curses.init_pair(5, Colors.YELLOW, Colors.BLACK)
        curses.init_pair(6, Colors.BLUE, Colors.BLACK)

        Colors.WHITE_BLACK = curses.color_pair(1)
        Colors.BLACK_WHITE = curses.color_pair(2)
        Colors.RED_BLACK = curses.color_pair(3)
        Colors.GREEN_BLACK = curses.color_pair(4)
        Colors.YELLOW_BLACK = curses.color_pair(5)
        Colors.BLUE_BLACK = curses.color_pair(6)
