import curses

class Draw:
    def __init__(self, board, cursor, show_eliminations):
        self._b = board
        self._cursor = cursor
        self._show_eliminations = show_eliminations

    def __call__(self, stdscr):
        stdscr.clear()
        
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
                self._draw_value(stdscr, (x, y))

        self._draw_cursor(stdscr)
        
    def _draw_value(self, stdscr, p):
        v = self._b.value(p)
        if v == 0:
            self._draw_elimination(stdscr, p)
        else:
            v = str(v)
            x, y = p
            stdscr.addstr(4*y+2, 6*x+3, v)

    def _draw_elimination(self, stdscr, p):
        x, y = p
        e = self._b.eliminations(p)
        for j in range(3):
            v = ""
            for i in range(3):
                if 3*j+i+1 in e:
                    v += " "
                else:
                    v += "."

            if not self._show_eliminations:
                v = "   "
            stdscr.addstr(4*y+j+1, 6*x+2, v)

    def _draw_cursor(self, stdscr):
        x, y = self._cursor
        stdscr.move(4*y + 2, 6*x + 3)
