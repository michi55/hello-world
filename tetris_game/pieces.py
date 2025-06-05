# tetris_game/pieces.py
import random

# Standard Tetris piece shapes and their initial orientation.
# Colors are represented by numbers 1-7, corresponding to the keys.
# Each shape is a list of lists (rows of the piece).
SHAPES = {
    "I": [[[1, 1, 1, 1]]],  # Cyan
    "O": [[[2, 2], [2, 2]]],  # Yellow
    "T": [[[0, 3, 0], [3, 3, 3]]],  # Purple
    "S": [[[0, 4, 4], [4, 4, 0]]],  # Green
    "Z": [[[5, 5, 0], [0, 5, 5]]],  # Red
    "J": [[[6, 0, 0], [6, 6, 6]]],  # Blue
    "L": [[[0, 0, 7], [7, 7, 7]]]   # Orange
}

class Piece:
    def __init__(self, x, y, shape_name=None):
        if shape_name is None:
            self.shape_name = random.choice(list(SHAPES.keys()))
        else:
            self.shape_name = shape_name

        self.x = x
        self.y = y

        # Store all rotation states for the piece type
        # The first item in SHAPES[self.shape_name] is the base shape
        self.base_shape = SHAPES[self.shape_name][0]
        self.rotations = self._get_all_rotations(self.base_shape)
        self.rotation_index = 0
        self.shape = self.rotations[self.rotation_index]
        # Assign a unique number (1-7) as color based on the shape name
        self.color = list(SHAPES.keys()).index(self.shape_name) + 1

    def _get_all_rotations(self, base_shape):
        # Generates 4 rotations for a given shape
        rotations = [base_shape]
        current_shape = base_shape

        # O-piece doesn't rotate, return its base shape only
        if self.shape_name == "O":
            return rotations

        for _ in range(3): # Generate 3 more rotations
            rows = len(current_shape)
            if rows == 0: # Should not happen with valid shapes
                return [[]]
            cols = len(current_shape[0])
            if cols == 0: # Should not happen with valid shapes
                 return [[]]

            new_shape = [[0 for _ in range(rows)] for _ in range(cols)]
            for r in range(rows):
                for c in range(cols):
                    new_shape[c][rows - 1 - r] = current_shape[r][c]
            rotations.append(new_shape)
            current_shape = new_shape
        return rotations

    def rotate(self):
        if self.shape_name == "O": # O piece does not rotate
            return
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)
        self.shape = self.rotations[self.rotation_index]

    def next_rotation_shape(self):
        if self.shape_name == "O":
            return self.shape
        next_idx = (self.rotation_index + 1) % len(self.rotations)
        return self.rotations[next_idx]
