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


def mark_board_with_k(x, y, board):
    width, height = len(board[0]), len(board)
    for i in range(-1, 2):
        for j in range(-1, 2):
            _x, _y = x + j, y + i
            if (i or j) and (0 <= _x < width and 0 <= _y < height):
                board[_y][_x] = 1


def mark_board(board, x, y, piece):
    globals()['mark_board_with_%s' % piece.lower()](x, y, board)


class ChessBoard:

    def __init__(self, width, height, pieces):
        row = lambda x: list(0 for _ in range(x))
        self.width, self.height, self.pieces = width, height, pieces
        self.board = list(row(width) for _ in range(height))

    def step(self, pieces=None):
        board = self.board
        _pieces = pieces or self.pieces
        return


@click.command()
@click.argument('size', type=ChessboardSizeType())
@click.argument('pieces', type=PiecesType())
def build_chess(size, pieces):
    width, height = size
    assert width * height > len(pieces) / 2
    board = ChessBoard(width, height, pieces)
    board.step()
    print('\n'.join(str(row) for row in board.board))

if __name__ == '__main__':
    build_chess()
