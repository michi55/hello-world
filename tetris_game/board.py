# tetris_game/board.py
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    def display(self, current_piece=None):
        display_grid = [row[:] for row in self.grid]
        if current_piece:
            piece_shape = current_piece.shape
            for r_idx, piece_row in enumerate(piece_shape):
                for c_idx, cell_val in enumerate(piece_row):
                    if cell_val != 0:
                        board_y = current_piece.y + r_idx
                        board_x = current_piece.x + c_idx
                        if 0 <= board_y < self.height and 0 <= board_x < self.width:
                            display_grid[board_y][board_x] = current_piece.color

        print("-" * (self.width * 2 + 3)) # Top border adjusted for spaces
        for row in display_grid:
            display_row_chars = []
            for cell in row:
                if cell == 0:
                    display_row_chars.append(".") # Empty
                else:
                    # Potentially map colors to letters/symbols if desired, or just use a block
                    display_row_chars.append(str(cell)) # Display piece "color" number
            print(f"| {' '.join(display_row_chars)} |")
        print("-" * (self.width * 2 + 3)) # Bottom border

    def is_collision(self, piece_shape, piece_x, piece_y):
        for r_idx, row_val in enumerate(piece_shape):
            for c_idx, cell_val in enumerate(row_val):
                if cell_val != 0: # If part of the piece's shape
                    board_y = piece_y + r_idx
                    board_x = piece_x + c_idx

                    # Check side boundaries
                    if not (0 <= board_x < self.width):
                        return True
                    # Check bottom boundary (top boundary is implicitly handled by spawn location)
                    if board_y >= self.height:
                        return True
                    # Check collision with existing locked pieces on the board
                    # Ensure board_y is within grid height for this check
                    if board_y >= 0 and self.grid[board_y][board_x] != 0:
                        return True
        return False

    def merge_piece(self, piece):
        piece_shape = piece.shape
        for r_idx, row_val in enumerate(piece_shape):
            for c_idx, cell_val in enumerate(row_val):
                if cell_val != 0:
                    board_y = piece.y + r_idx
                    board_x = piece.x + c_idx
                    # Only merge if within bounds (should be guaranteed by collision checks before lock)
                    if 0 <= board_y < self.height and 0 <= board_x < self.width:
                        self.grid[board_y][board_x] = piece.color

    def clear_lines(self):
        lines_cleared_count = 0
        new_grid = []
        for r_idx in range(self.height -1, -1, -1): # Iterate from bottom up
            is_line_full = True
            for c_idx in range(self.width):
                if self.grid[r_idx][c_idx] == 0:
                    is_line_full = False
                    break
            if is_line_full:
                lines_cleared_count += 1
            else:
                new_grid.insert(0, self.grid[r_idx]) # Add non-full lines to new_grid from top

        # Add new empty lines at the top for each cleared line
        for _ in range(lines_cleared_count):
            new_grid.insert(0, [0 for _ in range(self.width)])

        self.grid = new_grid
        return lines_cleared_count
