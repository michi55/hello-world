# tetris_game/main.py
import sys
from .game import TetrisGame

def main_run(): # Renamed to avoid conflict if we add a main function in game.py later
    """
    Initializes and runs the Tetris game.
    """
    # Default board size, can be made configurable later if needed
    game_width = 10
    game_height = 20

    print("Welcome to Text Tetris!")
    # Potentially add options here later (e.g., board size, difficulty)

    game = TetrisGame(width=game_width, height=game_height)
    game.run()

    print("Thanks for playing!")
    return 0

if __name__ == '__main__':
    sys.exit(main_run())
