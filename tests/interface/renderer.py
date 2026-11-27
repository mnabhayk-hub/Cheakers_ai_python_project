"""Pygame board renderer."""

import pygame

from config import (
    ROWS,
    COLS,
    SQUARE_SIZE,
    EMPTY,
    LIGHT,
    DARK,
    RED_COLOR,
    BLACK_COLOR,
    WHITE,
    GOLD,
    GREEN
)


class Renderer:

    def __init__(self, screen):

        self.screen = screen

        self.font = pygame.font.SysFont(
            "Arial",
            30,
            bold=True
        )

    def draw_board(self, board, selected=None, targets=None):

        targets = targets or []

        for row in range(ROWS):
            for col in range(COLS):

                color = (
                    DARK if (row + col) % 2 else LIGHT
                )

                rect = pygame.Rect(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )

                pygame.draw.rect(
                    self.screen,
                    color,
                    rect
                )

                if selected == (row, col):

                    pygame.draw.rect(
                        self.screen,
                        GOLD,
                        rect,
                        5
                    )

                if (row, col) in targets:

                    pygame.draw.circle(
                        self.screen,
                        GREEN,
                        rect.center,
                        10
                    )

                piece = board[row][col]

                if piece != EMPTY:
                    self.draw_piece(row, col, piece)

    def draw_piece(self, row, col, piece):

        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2

        color = RED_COLOR if piece > 0 else BLACK_COLOR

        pygame.draw.circle(
            self.screen,
            color,
            (x, y),
            30
        )

        pygame.draw.circle(
            self.screen,
            WHITE,
            (x, y),
            30,
            2
        )

        if abs(piece) == 2:

            text = self.font.render(
                "K",
                True,
                GOLD
            )

            self.screen.blit(
                text,
                text.get_rect(center=(x, y))
            )
