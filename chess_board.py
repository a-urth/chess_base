import copy

PIECES = ('Q', 'R', 'B', 'K', 'N')
PIECES_MAP = dict(zip(PIECES, range(5, 0, -1)))


def check_board_for_k(y, x, width, height, board):
    cells = set()
    # just move 1 step around current cell
    for i in range(-1, 2):
        for j in range(-1, 2):
            _x, _y = x + j, y + i
            if (i or j) and (0 <= _x < width and 0 <= _y < height):
                if board[_y][_x] in PIECES:
                    return None
                if not board[_y][_x]:
                    cells.add((_y, _x))
    return cells


def check_board_for_r(y, x, width, height, board):
    cells = set()
    # move horizontaly
    for i in range(width):
        if i == x:
            continue
        if board[y][i] in PIECES:
            return None
        if not board[y][i]:
            cells.add((y, i))
    # and vertically
    for i in range(height):
        if i == y:
            continue
        if board[i][x] in PIECES:
            return None
        if not board[i][x]:
            cells.add((i, x))
    return cells


def check_board_for_b(y, x, width, height, board):
    cells = set()
    for i in range(width):
        if i == x:
            continue

        _y = y + abs(x - i)
        if _y < height:
            if board[_y][i] in PIECES:
                return None
            if not board[_y][i]:
                cells.add((_y, i))

        _y = y - abs(x - i)
        if _y >= 0:
            if board[_y][i] in PIECES:
                return None
            if not board[_y][i]:
                cells.add((_y, i))
    return cells


def check_board_for_q(y, x, width, height, board):
    # since queen is intersection of bishop and rook...
    cells_r = check_board_for_r(y, x, width, height, board)
    if cells_r is None:
        return cells_r
    cells_b = check_board_for_b(y, x, width, height, board)
    if cells_b is None:
        return cells_b
    return cells_r.union(cells_b)


def check_board_for_n(y, x, width, height, board):
    cells = set()
    # very naive solve for knights
    for i, j in ((-2, 1), (-1, 2), (1, 2), (2, 1)):
        _x = x + i
        if not (_x < width and _x >= 0):
            continue

        _y = y + j
        if _y < height:
            if board[_y][_x] in PIECES:
                return None
            if not board[_y][_x]:
                cells.add((_y, _x))

        _y = y - j
        if _y >= 0:
            if board[_y][_x] in PIECES:
                return None
            if not board[_y][_x]:
                cells.add((_y, _x))
    return cells


def check_board(y, x, board, piece):
    func = globals()['check_board_for_%s' % piece.lower()]
    width, height = len(board[0]), len(board)
    return func(y, x, width, height, board)


def mark_cells(cells, board):
    for cell in cells:
        y, x = cell
        board[y][x] = '-'


class ChessBoard:

    def __init__(self, width, height, pieces):
        self.width, self.height, self.pieces = width, height, pieces
        self.correct_combinations = []

    def get_unique_result(self):
        t = []
        for c in self.correct_combinations:
            if c not in t:
                t.append(c)
        return t

    def new_board(self):
        row = lambda x: list(0 for _ in range(x))
        return list(row(self.width) for _ in range(self.height))

    def find_combinations(self):
        self.place_pieces(self.new_board(), self.pieces)

    def place_pieces(self, _board, pieces):
        for i in range(self.height):
            for j in range(self.width):
                # if this place is already under attack
                if _board[i][j]:
                    continue

                piece = pieces[0]
                # or current piece on this place will attack
                cells_to_mark = check_board(i, j, _board, piece)
                # just continue
                if cells_to_mark is None:
                    continue
                # if ok - make copy of board and mark it
                board = copy.deepcopy(_board)
                board[i][j] = piece
                mark_cells(cells_to_mark, board)
                # if its last piece we need to store combination and continue
                if len(pieces) == 1:
                    self.correct_combinations.append(board)
                    return
                # if not - go deeper
                self.place_pieces(board, pieces[1:])

    def __repr__(self):
        res = []
        for board in self.get_unique_result():
            width = len(board[0])
            delimeter = '   '
            board = '\n'.join(delimeter.join(str(cell) for cell in row) for row in board)
            res.append(board)
        line = '-' * (len(delimeter) * (width - 1) + width)
        return ("\n%s\n" % line).join(res)
