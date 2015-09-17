from chess_base import ChessBoard, PIECES


def test_pieces_const():
    assert len(PIECES) == 5


def test_build_board_empty():
    assert ChessBoard(0, 0, []).board == []


def test_build_board():
    width, height = 4, 4
    board = ChessBoard(width, height, []).board
    assert len(board) == height
    assert all(len(row) == width for row in board)
