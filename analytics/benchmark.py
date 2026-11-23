"""Repeatable benchmark of the three AI search algorithms."""

import statistics

from game.board import Board

from ai.minimax import get_best_move as minimax
from ai.alpha_beta import get_best_move as alpha_beta
from ai.greedy import get_best_move as greedy


ALGORITHMS = {
    "Minimax": minimax,
    "Alpha-Beta": alpha_beta,
    "Greedy Best-First": greedy
}


def make_positions():

    """Create several deterministic legal positions."""

    positions = [
        ("initial", Board())
    ]

    board = Board()

    for _ in range(6):

        moves = board.get_all_moves()

        if not moves:
            break

        board.make_move(moves[0])

    positions.append(
        ("after_6_plies", board.clone())
    )

    board = Board()

    for _ in range(12):

        moves = board.get_all_moves()

        if not moves:
            break

        board.make_move(
            moves[len(moves) // 2]
        )

    positions.append(
        ("after_12_plies", board.clone())
    )

    return positions


def benchmark(depth=3, trials=3):

    results = {}

    for position_name, position in make_positions():

        results[position_name] = {}

        for algorithm_name, algorithm in ALGORITHMS.items():

            times = []
            nodes = []
            scores = []
            cutoffs = []

            for _ in range(trials):

                move, stats = algorithm(
                    position.clone(),
                    depth
                )

                times.append(stats["time"])
                nodes.append(stats["nodes"])
                scores.append(stats["score"])

                if "cutoffs" in stats:
                    cutoffs.append(stats["cutoffs"])

            results[position_name][algorithm_name] = {

                "average_time": statistics.mean(times),

                "median_time": statistics.median(times),

                "average_nodes": statistics.mean(nodes),

                "score": scores[-1],

                "move": move,

                "average_cutoffs": (
                    statistics.mean(cutoffs)
                    if cutoffs else 0
                )
            }

    for position_name, algorithms in results.items():

        print(f"\nPOSITION: {position_name}")

        for algorithm_name, data in algorithms.items():

            print(
                f"{algorithm_name:20} "
                f"time={data['average_time']:.6f}s "
                f"nodes={data['average_nodes']:.1f} "
                f"score={data['score']} "
                f"cutoffs={data['average_cutoffs']:.1f}"
            )

    return results


def plot_results(results):

    import matplotlib.pyplot as plt

    names = list(ALGORITHMS)
    positions = list(results)

    for metric, title, ylabel, filename in (

        (
            "average_time",
            "Average Execution Time",
            "Seconds",
            "execution_time.png"
        ),

        (
            "average_nodes",
            "Average Nodes Explored",
            "Nodes",
            "explored_nodes.png"
        )

    ):

        for position in positions:

            values = [
                results[position][name][metric]
                for name in names
            ]

            plt.figure()

            plt.bar(names, values)

            plt.title(
                f"{title} - {position}"
            )

            plt.ylabel(ylabel)

            plt.xticks(rotation=15)

            plt.tight_layout()

            plt.savefig(
                f"{position}_{filename}"
            )

            plt.close()


if __name__ == "__main__":

    benchmark_results = benchmark(
        depth=3,
        trials=3
    )

    plot_results(benchmark_results)
