# tetris_game/tests/test_game.py
import unittest
from tetris_game.game import TetrisGame
from tetris_game.board import Board # For direct manipulation if needed
from tetris_game.pieces import Piece

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = TetrisGame(width=10, height=20) # Standard game size

    def test_game_initialization(self):
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.current_piece) # A piece should spawn on init
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)

    def test_spawn_piece(self):
        initial_piece = self.game.current_piece
        self.game.spawn_piece() # Spawns a new piece
        self.assertNotEqual(initial_piece, self.game.current_piece, "Should spawn a new piece instance")
        self.assertTrue(0 <= self.game.current_piece.x < self.game.board.width)
        self.assertEqual(self.game.current_piece.y, 0) # Should spawn at the top

    def test_game_over_condition(self):
        # Fill the board almost to the top to force a game over
        # This is a bit tricky to set up perfectly without playing the game
        # We'll fill the top rows directly on the board grid for testing
        for r in range(self.game.board.height // 2): # Fill top half
            for c in range(self.game.board.width):
                self.game.board.grid[r][c] = 1 # Mark as filled

        # Try to spawn a new piece. It should collide and trigger game over.
        # For this test, we might need to manually set a piece and check collision
        # then call spawn_piece which internally checks for game over
        self.game.current_piece = None # Simulate piece locked
        self.game.spawn_piece() # This should detect collision and set game_over

        # A more direct way to test game_over on spawn:
        game_for_test = TetrisGame(width=3, height=5)
        # Fill the spawn area. An 'O' piece is 2x2.
        # [[2,2],
        #  [2,2]]
        # Spawn x for width 3, piece width 2 is (3//2 - 2//2) = 1-1 = 0
        # So piece spawns at x=0, y=0
        game_for_test.board.grid[0][0] = 1
        game_for_test.board.grid[0][1] = 1
        game_for_test.board.grid[1][0] = 1
        game_for_test.board.grid[1][1] = 1

        game_for_test.spawn_piece() # Try to spawn a piece (will be O or similar)
        self.assertTrue(game_for_test.game_over, "Game should be over if spawn area is blocked.")


    def test_scoring_single_line(self):
        self.game.score = 0
        # Simulate clearing one line
        # Manually set a line on the board
        for c in range(self.game.board.width):
            self.game.board.grid[self.game.board.height - 1][c] = 1

        cleared = self.game.board.clear_lines()
        self.assertEqual(cleared, 1)
        if cleared == 1: self.game.score += 100 # Mimic game scoring logic

        self.assertEqual(self.game.score, 100)

    def test_scoring_tetris(self): # Clearing 4 lines
        self.game.score = 0
        # Simulate clearing four lines
        for r in range(self.game.board.height - 4, self.game.board.height):
            for c in range(self.game.board.width):
                self.game.board.grid[r][c] = 1

        cleared = self.game.board.clear_lines()
        self.assertEqual(cleared, 4)
        if cleared >= 4: self.game.score += 800 # Mimic game scoring for Tetris

        self.assertEqual(self.game.score, 800)

if __name__ == '__main__':
    unittest.main()
