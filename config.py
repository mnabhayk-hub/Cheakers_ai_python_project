
"""Central configuration for the American Checkers project."""

# Board dimensions
ROWS = 8
COLS = 8
SQUARE_SIZE = 80

# Game window dimensions
WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

# Player identifiers
RED = 1
BLACK = -1

# Piece identifiers
EMPTY = 0
RED_KING = 2
BLACK_KING = -2

# GUI colours (RGB)
LIGHT = (240, 217, 181)
DARK = (101, 67, 33)

RED_COLOR = (210, 45, 45)
BLACK_COLOR = (35, 35, 35)

WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GREEN = (30, 180, 80)

# Game settings
FPS = 60
SEARCH_DEPTH = 4
