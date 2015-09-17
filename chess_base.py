import copy

import click

PIECES = ('Q', 'R', 'B', 'K', 'N')
PIECES_MAP = dict(zip(PIECES, range(5, 0, -1)))


class ChessboardSizeType(click.ParamType):
    name = 'two dimension size'

    def convert(self, value, param, ctx):
        try:
            x, y = value.split('x')
            x, y = int(x), int(y)
            if x <= 0 or y <= 0:
                raise ValueError()
            else:
                return x, y
        except ValueError:
            self.fail('Size must be in form "WxH" where W and H  - must be more than zero')


class PiecesType(click.ParamType):
    name = 'pieces'

    def convert(self, value, param, ctx):
        try:
            pieces = value.split(',')
            wrong_pieces = any(piece not in PIECES for piece in pieces)
            if not pieces or wrong_pieces:
                raise ValueError()

            return sorted(pieces, key=lambda x: PIECES_MAP[x], reverse=True)
        except ValueError:
            self.fail('Pieces must be provided in form "K,Q,B,B"')


def check_board_for_k(y, x, board):
    width, height, cells = len(board[0]), len(board), []
    for i in range(-1, 2):
        for j in range(-1, 2):
            _x, _y = x + j, y + i
            if (i or j) and (0 <= _x < width and 0 <= _y < height):
                if board[_y][_x] in PIECES:
                    return None
                cells.append((_y, _x))
    return cells


def check_board_for_r(y, x, board):
    width, height = len(board[0]), len(board)
    cells = []
    # move horizontaly
    for i in range(width):
        if i != x:
            if board[y][i] in PIECES:
                return None
            cells.append((y, i))
    # and vertically
    for i in range(height):
        if i != y:
            if board[i][x] in PIECES:
                return None
            cells.append((i, x))
    return cells


def check_board(y, x, board, piece):
    return globals()['check_board_for_%s' % piece.lower()](y, x, board)


def mark_cells(cells, board):
    for cell in cells:
        y, x = cell
        board[y][x] = '-'


class ChessBoard:

    def __init__(self, width, height, pieces):
        self.width, self.height, self.pieces = width, height, pieces
        self.boards = []

    def new_board(self):
        row = lambda x: list(0 for _ in range(x))
        return list(row(self.width) for _ in range(self.height))

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
                # if its last piece we need to store combination if its unique and continue
                if len(pieces) == 1:
                    if board not in self.boards:
                        self.boards.append(board)
                    return
                # if not - go deeper
                self.place_pieces(board, pieces[1:])


def print_boards(boards):
    for board in boards:
        width = len(board[0])
        delimeter = '   '
        board = '\n'.join(delimeter.join(str(cell) for cell in row) for row in board)
        line = '-' * (len(delimeter) * (width - 1) + width)
        print('{0}\n{1}'.format(board, line))


@click.command()
@click.argument('size', type=ChessboardSizeType())
@click.argument('pieces', type=PiecesType())
def build_chess(size, pieces):
    width, height = size
    assert len(pieces) <= (width * height) ** 0.5
    board = ChessBoard(width, height, pieces)
    # import pudb; pu.db
    board.place_pieces(board.new_board(), pieces)
    print_boards(board.boards)

if __name__ == '__main__':
    build_chess()
