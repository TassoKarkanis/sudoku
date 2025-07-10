import curses
from .sudoku import sudoku
      
curses.wrapper(sudoku)
