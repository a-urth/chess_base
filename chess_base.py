from datetime import datetime

import click

from chess_board import ChessBoard


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
            wrong_pieces = any(piece not in ChessBoard.PIECES for piece in pieces)
            if not pieces or wrong_pieces:
                raise ValueError()

            return sorted(pieces, key=lambda x: ChessBoard.PIECES_MAP[x], reverse=True)
        except ValueError:
            self.fail('Pieces must be provided in form "K,Q,B,B"')


@click.command()
@click.option('--verbose', is_flag=True)
@click.argument('size', type=ChessboardSizeType())
@click.argument('pieces', type=PiecesType())
def build_chess(size, pieces, verbose):
    width, height = size
    # assert len(pieces) <= (width * height) / 2
    board = ChessBoard(width, height, pieces, verbose=verbose)
    t = datetime.now()
    board.find_combinations()
    print(board.get_combinations_number(), datetime.now() - t)


if __name__ == '__main__':
    build_chess()
