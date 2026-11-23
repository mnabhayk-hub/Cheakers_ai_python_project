"""Heuristic-prioritised Greedy Best-First Search."""

import heapq
import itertools
import time

from game.rules import get_winner
from game.moves import get_valid_moves
from ai.evaluation import evaluate


def _position_score(board, root_player, depth_remaining):

    winner = get_winner(board.board, board.turn)

    if winner == root_player:
        return 100000 + depth_remaining

    if winner == -root_player:
        return -100000 - depth_remaining

    if winner is not None:
        return 0

    return evaluate(board.board, root_player)


def greedy_search(board, depth=4):

    stats = {"nodes": 0}

    root_player = board.turn
    sequence = itertools.count()

    # Heap item:
    # (-heuristic score, tie breaker, state, first move, level)

    frontier = []

    root_score = _position_score(
        board,
        root_player,
        depth
    )

    heapq.heappush(
        frontier,
        (
            -root_score,
            next(sequence),
            board.clone(),
            None,
            0
        )
    )

    while frontier:

        _, _, current, first_move, level = heapq.heappop(frontier)

        stats["nodes"] += 1

        winner = get_winner(
            current.board,
            current.turn
        )

        if winner is not None or level >= depth:

            score = _position_score(
                current,
                root_player,
                depth - level
            )

            stats["score"] = score

            return first_move, stats

        moves = get_valid_moves(
            current.board,
            current.turn
        )

        for move in moves:

            child = current.clone()
            child.make_move(move)

            root_move = (
                move if first_move is None else first_move
            )

            heuristic = _position_score(
                child,
                root_player,
                depth - level - 1
            )

            heapq.heappush(
                frontier,
                (
                    -heuristic,
                    next(sequence),
                    child,
                    root_move,
                    level + 1
                )
            )

    stats["score"] = _position_score(
        board,
        root_player,
        depth
    )

    return None, stats


def get_best_move(board, depth=4):

    start = time.perf_counter()

    move, stats = greedy_search(board, depth)

    stats["time"] = time.perf_counter() - start

    return move, stats
