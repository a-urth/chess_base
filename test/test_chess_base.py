import unittest

from chess_board import ChessBoard, PIECES
from chess_board import (
    check_board_for_b,
    check_board_for_r,
    check_board_for_k,
    check_board_for_q,
    check_board_for_n,
    check_board, mark_cells,
)


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


class ChessBoardTestCase(unittest.TestCase):

    def test_unique_result(self):
        board = ChessBoard(3, 3, ['K', 'K', 'R'])
        board.find_combinations()
        res = board.get_unique_result()
        self.assertEqual(len(res), 4)

    def test_print_board(self):
        solutions = [
            [
                ['K', '-', 'K'],
                ['-', '-', '-'],
                ['-', 'R', '-'],
            ],
            [
                ['K', '-', '-'],
                ['-', '-', 'R'],
                ['K', '-', '-'],
            ],
            [
                ['-', '-', 'K'],
                ['R', '-', '-'],
                ['-', '-', 'K'],
            ],
            [
                ['-', 'R', '-'],
                ['-', '-', '-'],
                ['K', '-', 'K'],
            ],
        ]
        board = ChessBoard(3, 3, ['K', 'K', 'R'])
        board.find_combinations()
        res = board.get_unique_result()
        self.assertEqual(res, solutions)


class BoardCheckersTestCase(unittest.TestCase):

    def test_check_board_general(self):
        width, height = 3, 3
        board = ChessBoard(width, height, []).new_board()
        br1, br2 = check_board(1, 1, board, 'R'), check_board_for_r(1, 1, width, height, board)
        bk1, bk2 = check_board(1, 1, board, 'K'), check_board_for_k(1, 1, width, height, board)
        self.assertEqual(br1, br2)
        self.assertEqual(bk1, bk2)
        self.assertNotEqual(br2, bk2)

    def test_check_board_for_r(self):
        board = [
            ('K', '-', 0),
            ('-', '-', 0),
            (0, 0, 0)
        ]
        width, height = len(board[0]), len(board)
        self.assertIsNone(check_board_for_r(0, 2, width, height, board))
        self.assertIsNone(check_board_for_r(2, 0, width, height, board))
        self.assertEqual(check_board_for_r(2, 1, width, height, board), {(2, 0), (2, 2)})

    def test_check_board_for_k(self):
        board = [
            ('R', '-', '-'),
            ('-', 0, 0),
            ('-', 0, 0)
        ]
        width, height = len(board[0]), len(board)
        self.assertIsNone(check_board_for_k(1, 1, width, height, board))
        self.assertEqual(check_board_for_k(2, 2, width, height, board), {(1, 1), (2, 1), (1, 2)})

    def test_check_board_for_b(self):
        board = [
            ('K', '-', 0),
            ('-', '-', 0),
            (0, 0, 0)
        ]
        width, height = len(board[0]), len(board)
        self.assertIsNone(check_board_for_b(2, 2, width, height, board))
        self.assertEqual(check_board_for_b(2, 1, width, height, board), {(1, 2)})
        self.assertEqual(check_board_for_b(0, 2, width, height, board), {(2, 0)})

    def test_check_board_for_q(self):
        board_1 = [
            ('K', '-', 0),
            ('-', '-', 0),
            (0, 0, 0)
        ]
        board_2 = [
            (0, 0, 0),
            (0, '-', '-'),
            (0, '-', 'K')
        ]
        width, height = len(board_1[0]), len(board_1)
        self.assertIsNone(check_board_for_q(2, 2, width, height, board_1))
        self.assertIsNone(check_board_for_q(0, 2, width, height, board_1))
        self.assertIsNone(check_board_for_q(2, 0, width, height, board_1))
        self.assertIsNone(check_board_for_q(0, 0, width, height, board_2))
        self.assertEqual(check_board_for_q(2, 1, width, height, board_1), {(2, 0), (2, 2), (1, 2)})

    def test_check_board_for_n(self):
        board_1 = [
            ('K', '-', 0),
            ('-', '-', 0),
            (0, 0, 0)
        ]
        board_2 = [
            (0, 0, 0),
            (0, '-', '-'),
            (0, '-', 'K')
        ]
        width, height = len(board_1[0]), len(board_1)
        self.assertIsNone(check_board_for_n(2, 1, width, height, board_1))
        self.assertIsNone(check_board_for_n(1, 2, width, height, board_1))
        self.assertIsNone(check_board_for_n(0, 1, width, height, board_2))
        self.assertEqual(check_board_for_n(2, 0, width, height, board_1), {(1, 2)})
