
import pygame
import sys

from config import *

from game.board import Board
from interface.renderer import Renderer

from ai.minimax import get_best_move as minimax_move
from ai.alpha_beta import get_best_move as alpha_beta_move
from ai.greedy import get_best_move as greedy_move


pygame.init()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT + 100)
)

pygame.display.set_caption("Checkers AI")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22)

game = Board()

renderer = Renderer(screen)

selected = None
legal_moves = []

algorithm = "alpha"

ai_functions = {
    "minimax": minimax_move,
    "alpha": alpha_beta_move,
    "greedy": greedy_move
}

ai_stats = {}

running = True


def reset_game():

    global game, selected, legal_moves, ai_stats

    game = Board()
    selected = None
    legal_moves = []
    ai_stats = {}


def draw():

    screen.fill((30, 30, 30))

    targets = [
        move.end for move in legal_moves
        if move.start == selected
    ]

    renderer.draw_board(
        game.board,
        selected,
        targets
    )

    status = (
        "Your turn" if game.turn == RED
        else "AI thinking..."
    )

    text = font.render(
        status, True, WHITE
    )

    screen.blit(text, (10, HEIGHT + 10))

    info = font.render(
        f"AI: {algorithm.upper()} | "
        f"Depth: 4 | "
        f"Nodes: {ai_stats.get('nodes', 0)}",
        True,
        GOLD
    )

    screen.blit(info, (10, HEIGHT + 45))

    pygame.display.flip()


while running:

    clock.tick(60)

    winner = game.winner()

    if winner is not None:

        draw()

        message = (
            "You won!" if winner == RED
            else "AI won!"
        )

        print(message)

        pygame.time.wait(1500)
        reset_game()
        continue

    if game.turn == BLACK:

        draw()

        move, ai_stats = ai_functions[algorithm](
            game, SEARCH_DEPTH
        )

        if move is None:
            continue

        game.make_move(move)

        selected = None
        legal_moves = []

        continue

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                reset_game()

            elif event.key == pygame.K_1:
                algorithm = "minimax"

            elif event.key == pygame.K_2:
                algorithm = "alpha"

            elif event.key == pygame.K_3:
                algorithm = "greedy"

        elif event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            if y >= HEIGHT:
                continue

            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE

            clicked = (row, col)

            if selected is None:

                legal_moves = game.get_all_moves()

                matching = [
                    move for move in legal_moves
                    if move.start == clicked
                ]

                if matching:
                    selected = clicked

            else:

                matching = [
                    move for move in legal_moves
                    if move.start == selected
                    and move.end == clicked
                ]

                if matching:

                    game.make_move(matching[0])

                    selected = None
                    legal_moves = []

                else:

                    legal_moves = game.get_all_moves()

                    matching = [
                        move for move in legal_moves
                        if move.start == clicked
                    ]

                    selected = (
                        clicked if matching else None
                    )

    draw()


pygame.quit()
sys.exit()
