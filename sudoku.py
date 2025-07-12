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

    def animate_eliminations(self, stdscr):
        # generate the list of eliminations, add None in between
        emaps = []
        for emap in compute_eliminations(self._b):
            apply_eliminations(self._b, emap)
            emaps.append(emap)
            emaps.append(None)

        # initialize the index
        index = 0

        # reset and redraw
        self._b.reset_eliminations()
        self._draw_emap(stdscr, index, emaps)

        # handle input
        while True:
            key = stdscr.getch()
            if key == 27: # escape or alt
                break
            
            elif key in (curses.KEY_DOWN, curses.KEY_RIGHT, ord(' ')):
                # advance!
                if index+1 < len(emaps):
                    index += 1
                    emap = emaps[index]
                    if emap is None:
                        emap = emaps[index-1]
                        apply_eliminations(self._b, emap)
                    self._draw_emap(stdscr, index, emaps)

            elif key in (curses.KEY_UP, curses.KEY_LEFT):
                # retreat!
                if index > 0:
                    index -= 1
                    emap = emaps[index]
                    if emap is None:
                        emap = emaps[index-1]
                    else:
                        unapply_eliminations(self._b, emap)
                    self._draw_emap(stdscr, index, emaps)

        # reset
        self._compute_eliminations()
        self._draw(stdscr)

    def fill_single_values(self, stdscr):
        for p in all_cells():
            if not self._b.has_value(p):
                e = self._b.eliminations(p)
                if len(e) == 8:
                    # determine the value
                    v = [v for v in all_values() if v not in e][0]

                    # set it
                    self._b.set_value(p, v)

        # reset eliminations and redraw
        self._compute_eliminations()
        self._draw(stdscr)
        
    def _draw(self, stdscr):
        # compute a modeline
        filled = len([p for p in all_cells() if self._b.has_value(p)])
        if filled < 81:
            modeline = f"Completed {filled}/81"
        else:
            modeline = "Done!"
        
        draw = Draw(self._b,
                    cursor=self._cursor,
                    show_eliminations=self._show_eliminations,
                    modeline=modeline)
        draw(stdscr)

    def _draw_emap(self, stdscr, index, emaps):
        # get the emap
        emap = emaps[index]
        if emaps[index] is None:
            emap = emaps[index-1]
        
        # highlight the representative
        h1 = set()
        h1.add(emap["rep"])

        # highlight the group
        h2 = set()
        iterator = emap["iterator"]
        for p in iterator(emap["rep"]):
            h2.add(p)

        # compute the modeline
        name = emap["name"]
        group = emap["type"]
        i = index//2 + 1
        j = len(emaps)//2
        modeline = f"Elimination {i}/{j}: type {name} in {group}"
        draw = Draw(self._b,
                    show_eliminations=self._show_eliminations,
                    highlit1=h1,
                    highlit2=h2,
                    modeline=modeline)
        draw(stdscr)

    def _compute_eliminations(self):
        for emap in compute_eliminations(self._b):
            apply_eliminations(self._b, emap)

        
def get_board_filename(name):
    current_file_path = __file__
    current_module_directory = os.path.dirname(os.path.abspath(current_file_path))
    return os.path.join(current_module_directory, "boards", name)

        
def sudoku(stdscr):
    curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()

    # define some color pairs
    curses.init_color(1, 750, 750, 750) # white?
    curses.init_color(2, 0, 0, 750) # blue
    curses.init_color(3, 0, 500, 0)   # green
    curses.init_pair(1, 1, 2)
    curses.init_pair(2, 1, 3)

    g = Game()
    g.load(stdscr, get_board_filename("moderate3.json"))

    # receive input
    cursor_keys = (curses.KEY_UP, curses.KEY_DOWN,
                   curses.KEY_LEFT, curses.KEY_RIGHT)
    value_keys = list(range(48,58))
    while True:
        key = stdscr.getch()
        if key in cursor_keys:
            g.set_cursor(stdscr, key)
        elif key == ord('a'):
            g.animate_eliminations(stdscr)
        if key == ord('e'):
            show = g.get_show_eliminations()
            g.set_show_eliminations(stdscr, not show)
        if key == ord('f'):
            g.fill_single_values(stdscr)
        elif key in value_keys:
            g.set_value(stdscr, key - 48)
