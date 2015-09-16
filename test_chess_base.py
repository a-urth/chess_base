from chess_base import build_board, PIECES


def test_pieces_const():
    assert len(PIECES) == 5


def test_build_board_empty():
    assert build_board(0, 0) == []


def test_build_board():
    width, height = 4, 4
    board = build_board(width, height)
    assert len(board) == height
    assert all(len(row) == width for row in board)
