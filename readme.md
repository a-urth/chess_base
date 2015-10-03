ChessBase

-- install
pip install -r requirements.txt

-- tests
nosetests -v --with-coverage --cover-package=chess_board,chess_base

-- pylint
pylint --py3k chess_board.py


Problem

The problem is to find all unique configurations of a set of normal chess pieces on a chess board with dimensions M×N where none of the pieces is in a position to take any of the others. Assume the colour of the piece does not matter, and that there are no pawns among the pieces.

Solution

Main idea of solution is based around simple backtracking. First of all sort pieces by how many cells they take - from highest to lowest.

1. Take piece
2. Try to place it cell (starting upper left cell)
3. if its occupied - goto 2, if not - check if piece on this postion do not hit other pieces
4. If hit - goto 2, if no - create copy of already taken cells, merge with cells which current piece hit
5. If its last piece - print board (if verbose flag True) and increment combinations counter
6. If its not last piece - goto 1 with current cells (starting cell for next step depends on if next piece is same as current)

Time taken for solving 7x7 board with 2 Kings, 2 Queens, 2 Bishops and 1 Knight within 1 minute

UPD - current algorithm (using dict with cells as keys instead of list of lists representing full board) somewhere about 3 times faster than previous, and becuase of storing only hashes much more memory efficient.

UPD2 - huge optimisation without calculation of hash makes solution at least 10 times faster than previous
