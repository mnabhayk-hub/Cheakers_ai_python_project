"""Pygame entry point for Human-vs-AI and AI-vs-AI Checkers."""

import copy
import queue
import threading
import sys

import pygame

from config import (
    WIDTH,
    HEIGHT,
    SQUARE_SIZE,
    RED,
    BLACK,
    WHITE,
    GOLD,
    GREEN,
    SEARCH_DEPTH
)

from game.board import Board
from interface.renderer import Renderer

from ai.minimax import get_best_move as minimax_move
from ai.alpha_beta import get_best_move as alpha_beta_move
from ai.greedy import get_best_move as greedy_move


def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT + 130)
    )

    pygame.display.set_caption("Checkers AI")

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(
        "Arial",
        22
    )

    small_font = pygame.font.SysFont(
        "Arial",
        16
    )

    game = Board()

    renderer = Renderer(screen)

    mode = "human"

    black_algorithm = "alpha"
    red_algorithm = "minimax"

    ai_functions = {

        "minimax": minimax_move,
        "alpha": alpha_beta_move,
        "greedy": greedy_move

    }

    selected = None
    legal_moves = []

    ai_stats = {}
    ai_error = None

    game_over = False
    winner = None

    running = True

    result_queue = queue.Queue()

    ai_thinking = False

    game_generation = 0

    def reset_game():

        nonlocal game
        nonlocal selected
        nonlocal legal_moves
        nonlocal ai_stats
        nonlocal ai_error
        nonlocal game_over
        nonlocal winner
        nonlocal ai_thinking
        nonlocal game_generation

        game_generation += 1

        game = Board()

        selected = None
        legal_moves = []

        ai_stats = {}
        ai_error = None

        game_over = False
        winner = None

        ai_thinking = False

        while True:

            try:
                result_queue.get_nowait()

            except queue.Empty:
                break

    def worker(snapshot, search_function, depth, generation):

        try:

            move, stats = search_function(
                snapshot,
                depth
            )

            result_queue.put(
                (
                    generation,
                    move,
                    stats or {},
                    None
                )
            )

        except Exception as exc:

            result_queue.put(
                (
                    generation,
                    None,
                    {},
                    exc
                )
            )

    def is_ai_turn():

        return (
            game.turn == BLACK
            or mode == "ai_vs_ai"
        )

    def current_algorithm():

        if game.turn == RED:
            return red_algorithm

        return black_algorithm

    def start_ai():

        nonlocal ai_thinking
        nonlocal ai_error

        if ai_thinking or game_over or not is_ai_turn():
            return

        ai_thinking = True
        ai_error = None

        search_function = ai_functions[
            current_algorithm()
        ]

        thread = threading.Thread(

            target=worker,

            args=(
                copy.deepcopy(game),
                search_function,
                SEARCH_DEPTH,
                game_generation
            ),

            daemon=True
        )

        thread.start()

    def draw():

        screen.fill((30, 30, 30))

        targets = [
            move.end
            for move in legal_moves
            if selected is not None
            and move.start == selected
        ]

        renderer.draw_board(
            game.board,
            selected,
            targets
        )

        if game_over:

            status = (
                "RED wins!"
                if winner == RED
                else "BLACK wins!"
            )

            status_color = (
                GREEN
                if winner == RED
                else GOLD
            )

        elif ai_error:

            status = "AI error - press R to restart"
            status_color = (255, 100, 100)

        elif ai_thinking:

            side = (
                "RED"
                if game.turn == RED
                else "BLACK"
            )

            status = (
                f"{side} AI thinking "
                f"({current_algorithm().upper()})..."
            )

            status_color = GOLD

        elif mode == "ai_vs_ai":

            status = (
                f"{'RED' if game.turn == RED else 'BLACK'} "
                "AI to move"
            )

            status_color = WHITE

        else:

            status = (
                "Your turn"
                if game.turn == RED
                else "AI turn"
            )

            status_color = WHITE

        screen.blit(

            font.render(
                status,
                True,
                status_color
            ),

            (10, HEIGHT + 7)
        )

        info = (

            f"Mode: {mode.upper()} | "
            f"RED AI: {red_algorithm.upper()} | "
            f"BLACK AI: {black_algorithm.upper()}"

        )

        screen.blit(

            small_font.render(
                info,
                True,
                GOLD
            ),

            (10, HEIGHT + 42)
        )

        stats_text = (

            f"Depth: {SEARCH_DEPTH} | "
            f"Nodes: {ai_stats.get('nodes', 0)} | "
            f"Time: {ai_stats.get('time', 0):.4f}s"

        )

        screen.blit(

            small_font.render(
                stats_text,
                True,
                WHITE
            ),

            (10, HEIGHT + 66)
        )

        controls = (
            "V: mode | 1-3: BLACK AI | "
            "4-6: RED AI | R: restart | Esc: quit"
        )

        screen.blit(

            small_font.render(
                controls,
                True,
                WHITE
            ),

            (10, HEIGHT + 92)
        )

        pygame.display.flip()

    try:

        while running:

            clock.tick(60)

            # Apply completed AI work on the main thread.

            while True:

                try:

                    (
                        generation,
                        move,
                        stats,
                        error
                    ) = result_queue.get_nowait()

                except queue.Empty:
                    break

                if generation != game_generation:
                    continue

                ai_thinking = False

                if error is not None:

                    ai_error = (
                        f"{type(error).__name__}: {error}"
                    )

                    print("AI error:", repr(error))

                    continue

                ai_stats = stats

                if game_over or not is_ai_turn():
                    continue

                if move is None:

                    if game.winner() is None:

                        ai_error = (
                            "AI returned no move, "
                            "but the position is not terminal."
                        )

                    continue

                if move not in game.get_all_moves():

                    ai_error = (
                        "AI returned a move that is not legal."
                    )

                    continue

                game.make_move(move)

            if not game_over:

                winner = game.winner()

                if winner is not None:

                    game_over = True

                    selected = None
                    legal_moves = []

            if (
                not game_over
                and not ai_thinking
                and not ai_error
                and is_ai_turn()
            ):

                start_ai()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:

                        running = False

                    elif event.key == pygame.K_r:

                        reset_game()

                    elif not ai_thinking:

                        if event.key == pygame.K_v:

                            mode = (
                                "ai_vs_ai"
                                if mode == "human"
                                else "human"
                            )

                            selected = None
                            legal_moves = []

                        elif event.key == pygame.K_1:

                            black_algorithm = "minimax"

                        elif event.key == pygame.K_2:

                            black_algorithm = "alpha"

                        elif event.key == pygame.K_3:

                            black_algorithm = "greedy"

                        elif event.key == pygame.K_4:

                            red_algorithm = "minimax"

                        elif event.key == pygame.K_5:

                            red_algorithm = "alpha"

                        elif event.key == pygame.K_6:

                            red_algorithm = "greedy"

                elif (

                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and mode == "human"
                    and not game_over
                    and not ai_thinking
                    and not ai_error
                    and game.turn == RED

                ):

                    x, y = pygame.mouse.get_pos()

                    if not (
                        0 <= x < WIDTH
                        and 0 <= y < HEIGHT
                    ):

                        continue

                    clicked = (
                        y // SQUARE_SIZE,
                        x // SQUARE_SIZE
                    )

                    if selected is None:

                        legal_moves = game.get_all_moves()

                        if any(
                            move.start == clicked
                            for move in legal_moves
                        ):

                            selected = clicked

                    else:

                        matching = [

                            move
                            for move in legal_moves

                            if (
                                move.start == selected
                                and move.end == clicked
                            )

                        ]

                        if matching:

                            game.make_move(matching[0])

                            selected = None
                            legal_moves = []

                        else:

                            legal_moves = game.get_all_moves()

                            selected = (

                                clicked
                                if any(
                                    move.start == clicked
                                    for move in legal_moves
                                )
                                else None

                            )

            draw()

    finally:

        pygame.quit()

    return 0


if __name__ == "__main__":

    sys.exit(main())

pygame.quit()
sys.exit()
