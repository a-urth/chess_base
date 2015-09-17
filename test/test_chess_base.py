import unittest

from chess_base import ChessBoard, PIECES
from chess_base import check_board_for_r, check_board_for_k, check_board, mark_cells


class HelperFunctionsTestCase(unittest.TestCase):

    def test_pieces_const(self):
        self.assertEqual(len(PIECES), 5)

    def test_build_board_empty(self):
        self.assertEqual(ChessBoard(0, 0, []).new_board(), [])

    def test_build_board(self):
        width, height = 4, 4
        board = ChessBoard(width, height, []).new_board()
        self.assertEqual(len(board), height)
        self.assertTrue(all(len(row) == width for row in board))

    def test_mark_cells(self):
        board = ChessBoard(2, 2, []).new_board()
        cells = [(0, 0), (1, 1)]
        res_board = [
            ['-', 0],
            [0, '-']
        ]
        mark_cells(cells, board)
        self.assertEqual(board, res_board)


class BoardCheckersTestCase(unittest.TestCase):

    def test_check_board_general(self):
        board = ChessBoard(3, 3, []).new_board()
        br1, br2 = check_board(1, 1, board, 'R'), check_board_for_r(1, 1, board)
        bk1, bk2 = check_board(1, 1, board, 'K'), check_board_for_k(1, 1, board)
        self.assertEqual(br1, br2)
        self.assertEqual(bk1, bk2)
        self.assertNotEqual(br2, bk2)

    def test_check_board_for_r(self):
        board = [
            ('K', '-', 0),
            ('-', '-', 0),
            (0, 0, 0)
        ]
        self.assertIsNone(check_board_for_r(0, 2, board))
        self.assertIsNone(check_board_for_r(2, 0, board))

    def test_check_board_for_k(self):
        board = [
            (0, '-', 0),
            ('-', 'R', '-'),
            (0, '-', 0)
        ]
        self.assertIsNone(check_board_for_k(0, 0, board))
        self.assertIsNone(check_board_for_k(2, 2, board))
