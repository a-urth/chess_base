import click


PIECES = ('Q', 'R', 'B', 'N', 'K')
PIECES_MAP = dict(zip(PIECES, range(5, 0, -1)))


class ChessboardSizeType(click.ParamType):
    name = 'two dimension size'

    def convert(self, value, param, ctx):
        try:
            x, y = value.split('x')
            x, y = int(x), int(y)
            if x <= 0 or y <= 0:
                raise Exception()
            else:
                return x, y
        except Exception:
            self.fail('Size must be in form "WxH" where W and H  - must be more than zero')


class PiecesMapType(click.ParamType):
    name = 'pieces'

    def convert(self, value, param, ctx):
        try:
            pieces = value.split(',')
            wrong_pieces = any(piece not in PIECES for piece in pieces)
            if not pieces or wrong_pieces:
                raise Exception()

            return sorted(pieces, key=lambda x: PIECES_MAP[x], reverse=True)
        except Exception as e:
            print(e)
            self.fail('Pieces must be provided in form "K,Q,B,B"')


def build_board(width, height):
    row = lambda x: list(0 for _ in range(x))
    return list(row(width) for _ in range(height))


@click.command()
@click.argument('size', type=ChessboardSizeType())
@click.argument('pieces', type=PiecesMapType())
def build_chess(size, pieces):
    print(size, pieces)
    width, height = size
    assert width * height > len(pieces) / 2
    board = build_board(width, height)
    print(board)

if __name__ == '__main__':
    build_chess()
