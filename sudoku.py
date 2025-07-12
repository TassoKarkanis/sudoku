import curses
import os

from .board import *
from .eliminations import *
from .draw import Draw

class Game:
    def __init__(self):
        self._b = Board()

        # cursor position as (x,y)
        self._cursor = (0, 0)

        # whether to draw eliminations
        self._show_eliminations = True

    def load(self, stdscr, filename):
        self._b.load(filename)
        self._compute_eliminations()
        self._draw(stdscr)

    def set_cursor(self, stdscr, key):
        # determine the delta
        dx = 0
        dy = 0
        if key == curses.KEY_UP:
            dy = -1
        elif key == curses.KEY_DOWN:
            dy = 1
        elif key == curses.KEY_LEFT:
            dx = -1
        elif key == curses.KEY_RIGHT:
            dx = 1
        else:
            return

        # compute and set the cursor position
        x, y = self._cursor
        x += dx
        y += dy
        x = min(x, 8)
        x = max(x, 0)
        y = min(y, 8)
        y = max(y, 0)
        self._cursor = (x, y)
        self._draw(stdscr)

    def set_value(self, stdscr, v):
        self._b.set_value(self._cursor, v)
        self._compute_eliminations()
        self._draw(stdscr)

    def get_show_eliminations(self):
        return self._show_eliminations

    def set_show_eliminations(self, stdscr, show):
        self._show_eliminations = show
        self._draw(stdscr)
        
    def _draw(self, stdscr):
        draw = Draw(self._b, self._cursor, self._show_eliminations)
        draw(stdscr)

    def _compute_eliminations(self):
        compute_eliminations(self._b)

        
def get_board_filename(name):
    current_file_path = __file__
    current_module_directory = os.path.dirname(os.path.abspath(current_file_path))
    return os.path.join(current_module_directory, "boards", name)

        
def sudoku(stdscr):
    curses.initscr()
    curses.noecho()
    curses.cbreak()

    g = Game()
    g.load(stdscr, get_board_filename("moderate1.json"))

    # receive input
    cursor_keys = (curses.KEY_UP, curses.KEY_DOWN,
                   curses.KEY_LEFT, curses.KEY_RIGHT)
    value_keys = list(range(48,58))
    while True:
        key = stdscr.getch()
        if key in cursor_keys:
            g.set_cursor(stdscr, key)
        if key == 101:
            show = g.get_show_eliminations()
            g.set_show_eliminations(stdscr, not show)
        elif key in value_keys:
            g.set_value(stdscr, key - 48)
