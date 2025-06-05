# tetris_game/game.py
import time
from .board import Board
from .pieces import Piece, SHAPES # Import SHAPES to calculate piece width for spawning

class TetrisGame:
    def __init__(self, width=10, height=20):
        self.board = Board(width, height)
        self.current_piece = None
        self.score = 0
        self.lines_cleared_total = 0
        self.game_over = False
        self.spawn_piece()

    def _calculate_spawn_x(self, piece_shape):
        # Calculate x for the piece to be centered based on its actual width
        if not piece_shape or not piece_shape[0]: return self.board.width // 2
        piece_width = len(piece_shape[0])
        return self.board.width // 2 - piece_width // 2

    def spawn_piece(self):
        # Create a new piece instance (randomly selected)
        new_piece = Piece(0, 0) # Initial x, y are placeholders
        # Calculate spawn x based on the actual width of the new piece's current shape
        spawn_x = self._calculate_spawn_x(new_piece.shape)
        new_piece.x = spawn_x
        new_piece.y = 0 # Spawn at the very top

        self.current_piece = new_piece

        # GAME OVER CONDITION: If the new piece collides immediately
        if self.board.is_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
            self.game_over = True
            self.current_piece = None # No active piece if game is over

    def move_piece(self, dx, dy):
        if self.current_piece and not self.game_over:
            next_x = self.current_piece.x + dx
            next_y = self.current_piece.y + dy

            if not self.board.is_collision(self.current_piece.shape, next_x, next_y):
                self.current_piece.x = next_x
                self.current_piece.y = next_y
                return True
            elif dy > 0: # Trying to move down and collided
                self.lock_piece() # Lock the piece
            return False # Move failed or piece was locked
        return False

    def rotate_piece(self):
        if self.current_piece and not self.game_over:
            original_x = self.current_piece.x
            original_y = self.current_piece.y # Though y typically doesn't change with basic rotation

            next_shape = self.current_piece.next_rotation_shape()

            # Try rotation at current position
            if not self.board.is_collision(next_shape, self.current_piece.x, self.current_piece.y):
                self.current_piece.rotate()
                return True

            # Simple wall kick: try moving 1 unit left or right
            for kick_dx in [-1, 1]:
                if not self.board.is_collision(next_shape, self.current_piece.x + kick_dx, self.current_piece.y):
                    self.current_piece.x += kick_dx
                    self.current_piece.rotate()
                    return True
            # Add more sophisticated kicks if needed (e.g., -2, 2, or SRS)
            return False
        return False

    def lock_piece(self):
        if self.current_piece:
            self.board.merge_piece(self.current_piece)
            lines_cleared = self.board.clear_lines()

            if lines_cleared > 0:
                self.lines_cleared_total += lines_cleared
                # Simple scoring: 100 per line, bonus for 4 lines (Tetris)
                if lines_cleared == 1: self.score += 100
                elif lines_cleared == 2: self.score += 300
                elif lines_cleared == 3: self.score += 500
                elif lines_cleared >= 4: self.score += 800

            self.spawn_piece() # Spawn a new piece (this will check for game over)
            # current_piece is now the new piece, or None if game over

    def update(self): # Called periodically for automatic downward movement
        if not self.game_over and self.current_piece:
            self.move_piece(0, 1) # Attempt to move down

    def run(self):
        print("Starting Tetris Game...")
        print("Controls: 'a' (left), 'd' (right), 's' (down), 'w' (rotate), 'q' (quit)")

        last_fall_time = time.time()
        fall_interval = 0.8 # Piece falls every 0.8 seconds (can be adjusted for difficulty)

        while not self.game_over:
            self.board.display(self.current_piece)
            print(f"Score: {self.score} | Lines Cleared: {self.lines_cleared_total}")

            current_time = time.time()
            # Automatic fall based on interval
            if current_time - last_fall_time > fall_interval:
                self.update()
                last_fall_time = current_time
                # Re-display after automatic fall before asking for input
                if not self.game_over: # Check if game ended after fall
                    self.board.display(self.current_piece)
                    print(f"Score: {self.score} | Lines Cleared: {self.lines_cleared_total}")


            if self.game_over: # Check again if game over after auto-fall
                break

            action = input("Move (a/d/s/w), q to quit: ").strip().lower()

            if action == 'q':
                self.game_over = True
                print("Quitting game.")
                break
            elif action == 'a': # Left
                self.move_piece(-1, 0)
            elif action == 'd': # Right
                self.move_piece(1, 0)
            elif action == 's': # Down (manual)
                self.move_piece(0, 1)
                # Reset fall timer after manual down to make it feel more responsive
                last_fall_time = time.time()
            elif action == 'w': # Rotate
                self.rotate_piece()

            # time.sleep(0.05) # Small sleep to prevent CPU hogging if input is very fast / or for future non-blocking input

        # Final display after game over
        self.board.display(self.current_piece) # current_piece might be None here
        print(f"Game Over! Final Score: {self.score}, Total Lines Cleared: {self.lines_cleared_total}")
