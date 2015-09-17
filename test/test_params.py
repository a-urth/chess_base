import unittest

from click.exceptions import BadParameter

from chess_base import ChessboardSizeType, PiecesType


class ChessBoardSizeParamCase(unittest.TestCase):

    def test_missed_size(self):
        f = ChessboardSizeType().convert
        self.assertRaises(BadParameter, f, '', None, None)
        self.assertRaises(BadParameter, f, '3', None, None)
        self.assertRaises(BadParameter, f, '3x', None, None)
        self.assertRaises(BadParameter, f, 'x3', None, None)

    def test_wrong_delimeter(self):
        f = ChessboardSizeType().convert
        self.assertRaises(BadParameter, f, '3-3', None, None)
        self.assertRaises(BadParameter, f, '3 3', None, None)

    def test_param(self):
        self.assertEqual(ChessboardSizeType().convert('3x3', None, None), (3, 3))
        self.assertRaises(BadParameter, ChessboardSizeType().convert, '0x0', None, None)


class PiecesTypeParamCase(unittest.TestCase):

    def test_wrong_params(self):
        f = PiecesType().convert
        self.assertRaises(BadParameter, f, '', None, None)
        self.assertRaises(BadParameter, f, 'KK', None, None)
        self.assertRaises(BadParameter, f, 'K;K', None, None)
        self.assertRaises(BadParameter, f, ',K', None, None)
        self.assertRaises(BadParameter, f, 'A,K', None, None)

    def test_param(self):
        self.assertEqual(PiecesType().convert('K,K', None, None), ['K', 'K'])

    def test_param_order(self):
        self.assertEqual(PiecesType().convert('K,Q,N,B,K', None, None), ['Q', 'B', 'K', 'K', 'N'])
