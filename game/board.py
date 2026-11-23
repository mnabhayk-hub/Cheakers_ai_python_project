"""Game-state container for American Checkers."""

import copy

from config import ROWS, COLS, RED, BLACK, EMPTY
from game.moves import get_valid_moves
from game.rules import apply_move, get_winner


class Board:
    def __init__(self, board=None, turn=RED):
        if board is None:
            self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
            self.create_board()
        else:
            self.board = [row[:] for row in board]

        self.turn = turn

    def create_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row][col] = BLACK
                    elif row > 4:
                        self.board[row][col] = RED

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_all_moves(self):
        return get_valid_moves(self.board, self.turn)

    def make_move(self, move):
        legal_moves = self.get_all_moves()

        if move not in legal_moves:
            raise ValueError(f"Illegal move: {move}")

        self.board = apply_move(self.board, move, self.turn)
        self.turn *= -1

        return self

    def move(self, start, end):
        """Compatibility helper for a simple legal move by coordinates."""

        matches = [
            move for move in self.get_all_moves()
            if move.start == tuple(start) and move.end == tuple(end)
        ]

        if not matches:
            raise ValueError(f"Illegal move from {start} to {end}")

        return self.make_move(matches[0])

    def winner(self):
        return get_winner(self.board, self.turn)

    def clone(self):
        return copy.deepcopy(self)

    def print_board(self):
        symbols = {
            EMPTY: ".",
            RED: "R",
            BLACK: "B",
            2: "RK",
            -2: "BK",
        }

        for row in self.board:
            print(" ".join(symbols[piece] for piece in row))
