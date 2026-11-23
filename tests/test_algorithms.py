from game.board import Board

from ai.minimax import get_best_move as minimax
from ai.alpha_beta import get_best_move as alpha_beta
from ai.greedy import get_best_move as greedy


def test_all_algorithms_return_legal_moves():

    board = Board()

    legal = board.get_all_moves()

    for algorithm in (
        minimax,
        alpha_beta,
        greedy
    ):

        move, stats = algorithm(
            board.clone(),
            depth=2
        )

        assert move in legal

        assert stats["nodes"] > 0

        assert stats["time"] >= 0


def test_minimax_and_alpha_beta_scores_match():

    board = Board()

    _, mm_stats = minimax(
        board.clone(),
        depth=3
    )

    _, ab_stats = alpha_beta(
        board.clone(),
        depth=3
    )

    assert mm_stats["score"] == ab_stats["score"]

    assert ab_stats["nodes"] <= mm_stats["nodes"]
