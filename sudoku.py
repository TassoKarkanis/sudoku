import curses
import json

class Board:
    def __init__(self):
        # values, index [y][x]
        self._v = [[0]*9 for i in range(9)]

        # eliminations as a map of (x,y) -> set
        self._e = {}
        self._reset_eliminations()

        # cursor position as (x,y)
        self._cursor = (0, 0)

    def load(self, filename):
        # load the values
        with open(filename) as fp:
            self._v = json.load(fp)
            
        self._compute_eliminations()
        
    def draw(self, stdscr):
        # horizontal major dividers
        for y in [0, 12, 24, 36]:
            stdscr.addstr(y, 0, "X"*55)

        # vertical major dividers
        for x in [0, 18, 36, 54]:
            for y in range(36):
                stdscr.addstr(y, x, "X")

        # horizontal minor dividers
        for y in [4, 8, 16, 20, 28, 32]:
            for x in range(9):
                stdscr.addstr(y, 6*x + 1, "-"*5)

        # vertical minor dividers
        for y in range(36):
            for x in [6, 12, 24, 30, 42, 48]:
                if (y % 4) != 0:
                    stdscr.addstr(y, x, "|")

        # minor divider crosses
        for y in [4, 8, 16, 20, 28, 32]:
            for x in [6, 12, 24, 30, 42, 48]:
                stdscr.addstr(y, x, "+")

        # draw the values
        for y in range(9):
            for x in range(9):
                self.draw_value(stdscr, x, y)

    def draw_value(self, stdscr, x, y):
        v = self._v[y][x]
        if v == 0:
            self.draw_elimination(stdscr, x, y)
        else:
            v = str(v)
            stdscr.addstr(4*y+2, 6*x+3, v)

    def draw_elimination(self, stdscr, x, y):
        p = (x, y)
        e = self._e[p]
        for j in range(3):
            v = ""
            for i in range(3):
                if 3*j+i+1 in e:
                    v += " "
                else:
                    v += "."
            stdscr.addstr(4*y+j+1, 6*x+2, v)

    def draw_cursor(self, stdscr):
        x, y = self._cursor
        stdscr.move(4*y + 2, 6*x + 3)

    def set_cursor(self, key):
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

    def set_value(self, stdscr, v):
        x, y = self._cursor
        self._v[y][x] = v
        self.draw_value(stdscr, x, y)

    def _reset_eliminations(self):
        for x in range(9):
            for y in range(9):
                self._e[(x,y)] = set()

    def _compute_eliminations(self):
        self._reset_eliminations()

        # direct eliminations
        for x in range(9):
            for y in range(9):
                self._compute_value_eliminations(x, y)

        # only-possible-value
        for x in range(9):
            for y in range(9):
                self._compute_only_possible_value_eliminations(x, y)
        

    def _compute_value_eliminations(self, x0, y0):
        # get the eliminations
        p = (x0, y0)
        e = self._e[p]

        # eliminate values in the same row
        for x in range(9):
            v = self._v[y0][x]
            if v != 0:
                e.add(v)

        # eliminate values in the same column
        for y in range(9):
            v = self._v[y][x0]
            if v != 0:
                e.add(v)
        
        # eliminate values in the same square
        for j in range(3):
            y = 3*(y0 // 3) + j
            for i in range(3):
                x = 3*(x0 // 3) + i
                v = self._v[y][x]
                if v != 0:
                    e.add(v)

    def _compute_only_possible_value_eliminations(self, x0, y0):
        # get the eliminations
        p = (x0, y0)
        e0 = self._e[p]

        # if all other undetermined values in the 
        
    


def main(stdscr):
    curses.initscr()
    curses.noecho()
    curses.cbreak()

    b = Board()
    b.load("boards/moderate1.json")
    b.draw(stdscr)
    b.draw_cursor(stdscr)

    # receive input
    cursor_keys = (curses.KEY_UP, curses.KEY_DOWN,
                   curses.KEY_LEFT, curses.KEY_RIGHT)
    value_keys = list(range(48,58))
    while True:
        key = stdscr.getch()
        if key in cursor_keys:
            b.set_cursor(key)
            b.draw_cursor(stdscr)
        elif key in value_keys:
            b.set_value(stdscr, key - 48)

curses.wrapper(main)
      

