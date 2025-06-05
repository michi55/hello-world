# tetris_game/tests/test_pieces.py
import unittest
from tetris_game.pieces import Piece, SHAPES

class TestPieces(unittest.TestCase):
    def test_piece_creation(self):
        # Test creating a piece of a specific type
        piece_I = Piece(0, 0, shape_name="I")
        self.assertEqual(piece_I.shape_name, "I")
        self.assertEqual(piece_I.shape, SHAPES["I"][0]) # Initial shape
        self.assertEqual(piece_I.color, list(SHAPES.keys()).index("I") + 1)

        piece_O = Piece(0, 0, shape_name="O")
        self.assertEqual(piece_O.shape_name, "O")
        self.assertEqual(piece_O.shape, SHAPES["O"][0])
        self.assertEqual(piece_O.color, list(SHAPES.keys()).index("O") + 1)

    def test_piece_rotation_I(self):
        piece = Piece(0, 0, shape_name="I")
        initial_shape = piece.shape

        # Rotate once (I piece has 2 unique rotations, typically)
        piece.rotate()
        rotated_shape_1 = piece.shape
        self.assertNotEqual(initial_shape, rotated_shape_1, "I piece should change shape on first rotation")

        # Expected shape for I after 1 rotation (vertical)
        # Assuming base is [[1,1,1,1]]
        expected_rotated_I = [[1], [1], [1], [1]]
        # Check if current rotation logic produces this or similar
        # Note: exact shape depends on _get_all_rotations, this is an example
        self.assertEqual(len(rotated_shape_1), 4, "I piece should be 4 rows high after rotation")
        self.assertEqual(len(rotated_shape_1[0]), 1, "I piece should be 1 col wide after rotation")

        piece.rotate() # Rotate again (back to original or another state)
        rotated_shape_2 = piece.shape
        self.assertEqual(initial_shape, rotated_shape_2, "I piece should return to initial after 2/4 rotations")

    def test_piece_rotation_O(self):
        piece = Piece(0, 0, shape_name="O")
        initial_shape = piece.shape
        piece.rotate()
        # O piece should not change shape
        self.assertEqual(initial_shape, piece.shape, "O piece should not change shape on rotation")

    def test_piece_rotation_L(self):
        piece = Piece(0, 0, shape_name="L")
        # L piece base: [[[0,0,7],[7,7,7]]]
        initial_shape = piece.shape

        # Rotate once
        piece.rotate()
        rotated_shape_1 = piece.shape
        self.assertNotEqual(initial_shape, rotated_shape_1, "L piece should change shape on first rotation")
        # Example expected: [[7,0],[7,0],[7,7]] (depends on rotation logic)

        # Rotate three more times to get back to original
        piece.rotate()
        piece.rotate()
        piece.rotate()
        self.assertEqual(initial_shape, piece.shape, "L piece should return to initial after 4 rotations")

if __name__ == '__main__':
    unittest.main()
