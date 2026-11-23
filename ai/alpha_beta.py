"""Minimax with Alpha-Beta pruning."""

import time

from game.rules import get_winner
from game.moves import get_valid_moves
from ai.evaluation import evaluate


def alpha_beta(
    board,
    depth,
    alpha,
    beta,
    maximizing,
    player,
    stats
):

    stats["nodes"] += 1

    winner = get_winner(board.board, board.turn)

    if winner is not None:

        if winner == player:
            return 100000 + depth, None

        return -100000 - depth, None

    if depth == 0:
        return evaluate(board.board, player), None

    moves = get_valid_moves(board.board, board.turn)

    if not moves:
        return (-100000 if maximizing else 100000), None

    best_move = None

    if maximizing:

        best_score = float("-inf")

        for move in moves:

            child = board.clone()
            child.make_move(move)

            score, _ = alpha_beta(
                child,
                depth - 1,
                alpha,
                beta,
                False,
                player,
                stats
            )

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

            if beta <= alpha:
                stats["cutoffs"] += 1
                break

        return best_score, best_move

    best_score = float("inf")

    for move in moves:

        child = board.clone()
        child.make_move(move)

        score, _ = alpha_beta(
            child,
            depth - 1,
            alpha,
            beta,
            True,
            player,
            stats
        )

        if score < best_score:
            best_score = score
            best_move = move

        beta = min(beta, best_score)

        if beta <= alpha:
            stats["cutoffs"] += 1
            break

    return best_score, best_move


def get_best_move(board, depth=4):

    stats = {
        "nodes": 0,
        "cutoffs": 0
    }

    start = time.perf_counter()

    score, move = alpha_beta(
        board,
        depth,
        float("-inf"),
        float("inf"),
        True,
        board.turn,
        stats
    )

    stats["time"] = time.perf_counter() - start
    stats["score"] = score

    return move, stats
