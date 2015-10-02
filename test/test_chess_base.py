import unittest

from chess_board import ChessBoard


class HelperFunctionsTestCase(unittest.TestCase):

    def test_pieces_const(self):
        self.assertEqual(len(ChessBoard.PIECES), 5)

    def test_build_board_empty(self):
        self.assertEqual(ChessBoard(0, 0, []).new_board(), [])

    def test_build_board(self):
        width, height = 4, 4
        board = ChessBoard(width, height, []).new_board()
        self.assertEqual(len(board), height)
        self.assertTrue(all(len(row) == width for row in board))


class ChessBoardTestCase(unittest.TestCase):

    def test_unique_result(self):
        board = ChessBoard(3, 3, ['K', 'K', 'R'])
        board.find_combinations()
        self.assertEqual(board.get_combinations_number(), 4)


class BoardCheckersTestCase(unittest.TestCase):

    def test_check_board_general(self):
        cells = {
            (0, 0): 'K',
            (0, 1): None,
            (1, 0): None,
            (1, 1): None,
        }
        board = ChessBoard(3, 3, [])
        br1 = board.check_board(1, 1, cells, 'R')
        br2 = board.check_board_for_r(1, 1, cells)
        bk1 = board.check_board(1, 1, cells, 'K')
        bk2 = board.check_board_for_k(1, 1, cells)
        self.assertEqual(br1, br2)
        self.assertEqual(bk1, bk2)
        self.assertNotEqual(br2, bk2)

    def test_check_board_for_r(self):
        cells = {
            (0, 0): 'K',
            (0, 1): None,
            (1, 0): None,
            (1, 1): None,
        }
        board = ChessBoard(3, 3, [])
        self.assertIsNone(board.check_board_for_r(0, 2, cells))
        self.assertIsNone(board.check_board_for_r(2, 0, cells))
        self.assertEqual(board.check_board_for_r(2, 1, cells), {(2, 0), (2, 2)})

    def test_check_board_for_k(self):
        cells = {
            (0, 0): 'R',
            (0, 1): None,
            (0, 2): None,
            (1, 0): None,
            (2, 0): None,
        }
        board = ChessBoard(3, 3, [])
        self.assertIsNone(board.check_board_for_k(1, 1, cells))
        self.assertEqual(board.check_board_for_k(2, 2, cells), {(1, 1), (2, 1), (1, 2)})

    def test_check_board_for_b(self):
        cells = {
            (0, 0): 'K',
            (0, 1): None,
            (1, 0): None,
            (1, 1): None,
        }
        board = ChessBoard(3, 3, [])
        self.assertIsNone(board.check_board_for_b(2, 2, cells))
        self.assertEqual(board.check_board_for_b(2, 1, cells), {(1, 2)})
        self.assertEqual(board.check_board_for_b(0, 2, cells), {(2, 0)})

    def test_check_board_for_q(self):
        cells_1 = {
            (0, 0): 'K',
            (0, 1): None,
            (1, 0): None,
            (1, 1): None,
        }
        cells_2 = {
            (2, 2): 'K',
            (1, 1): None,
            (1, 2): None,
            (2, 1): None,
        }
        board = ChessBoard(3, 3, [])
        self.assertIsNone(board.check_board_for_q(2, 2, cells_1))
        self.assertIsNone(board.check_board_for_q(0, 2, cells_1))
        self.assertIsNone(board.check_board_for_q(2, 0, cells_1))
        self.assertIsNone(board.check_board_for_q(0, 0, cells_2))
        self.assertEqual(board.check_board_for_q(2, 1, cells_1), {(2, 0), (2, 2), (1, 2)})

    def test_check_board_for_n(self):
        cells_1 = {
            (0, 0): 'K',
            (0, 1): None,
            (1, 0): None,
            (1, 1): None,
        }
        cells_2 = {
            (2, 2): 'K',
            (1, 1): None,
            (1, 2): None,
            (2, 1): None,
        }
        board = ChessBoard(3, 3, [])
        self.assertIsNone(board.check_board_for_n(2, 1, cells_1))
        self.assertIsNone(board.check_board_for_n(1, 2, cells_1))
        self.assertIsNone(board.check_board_for_n(0, 1, cells_2))
        self.assertEqual(board.check_board_for_n(2, 0, cells_1), {(1, 2)})
