# tetris_game/tests/test_board.py
import unittest
from tetris_game.board import Board
from tetris_game.pieces import Piece # For creating test pieces

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board_width = 10
        self.board_height = 20
        self.board = Board(self.board_width, self.board_height)

    def test_board_initialization(self):
        self.assertEqual(self.board.width, self.board_width)
        self.assertEqual(self.board.height, self.board_height)
        self.assertEqual(len(self.board.grid), self.board_height)
        self.assertEqual(len(self.board.grid[0]), self.board_width)
        for row in self.board.grid:
            for cell in row:
                self.assertEqual(cell, 0) # All cells should be empty (0)

    def test_collision_with_boundaries(self):
        # Using a simple square piece for testing collisions
        # Shape: [[1,1],[1,1]] (O piece shape)
        o_piece_shape = Piece(0,0, "O").shape

        # Collision with bottom boundary
        self.assertTrue(self.board.is_collision(o_piece_shape, 0, self.board_height - 1)) # Piece one row off bottom
        self.assertFalse(self.board.is_collision(o_piece_shape, 0, self.board_height - 2)) # Piece fully on board

        # Collision with left boundary
        self.assertTrue(self.board.is_collision(o_piece_shape, -1, 0))
        self.assertFalse(self.board.is_collision(o_piece_shape, 0, 0))

        # Collision with right boundary
        self.assertTrue(self.board.is_collision(o_piece_shape, self.board_width - 1, 0)) # Piece one col off right
        self.assertFalse(self.board.is_collision(o_piece_shape, self.board_width - 2, 0))


    def test_collision_with_other_pieces(self):
        # Place a piece on the board
        test_piece = Piece(0, self.board_height - 2, shape_name="O") # Place O-piece at bottom
        self.board.merge_piece(test_piece)

        # Try to place another piece overlapping it
        # Shape: [[1,1],[1,1]] (O piece shape)
        o_shape = Piece(0,0,"O").shape # Corrected this line
        self.assertTrue(self.board.is_collision(o_shape, 0, self.board_height - 2)) # Collision
        self.assertFalse(self.board.is_collision(o_shape, 0, 0)) # No collision at top

    def test_clear_single_line(self):
        # Fill one line completely
        line_to_fill = self.board_height - 1
        for c in range(self.board.width):
            self.board.grid[line_to_fill][c] = 1 # Fill with non-zero

        cleared_count = self.board.clear_lines()
        self.assertEqual(cleared_count, 1)
        # Check if the line is now empty (filled with 0s)
        self.assertTrue(all(cell == 0 for cell in self.board.grid[line_to_fill]))
        # Check if the top line is now empty (new line added)
        self.assertTrue(all(cell == 0 for cell in self.board.grid[0]))


    def test_clear_multiple_lines(self):
        # Fill bottom two lines
        for r in range(self.board_height - 2, self.board_height):
            for c in range(self.board.width):
                self.board.grid[r][c] = 1

        cleared_count = self.board.clear_lines()
        self.assertEqual(cleared_count, 2)
        self.assertTrue(all(cell == 0 for cell in self.board.grid[self.board_height -1]))
        self.assertTrue(all(cell == 0 for cell in self.board.grid[self.board_height -2]))
        self.assertTrue(all(cell == 0 for cell in self.board.grid[0])) # New top line
        self.assertTrue(all(cell == 0 for cell in self.board.grid[1])) # New second top line

if __name__ == '__main__':
    unittest.main()
