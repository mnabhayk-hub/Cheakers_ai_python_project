from config import RED, BLACK, EMPTY, RED_KING

from game.moves import Move, get_valid_moves
from game.board import Board


def empty_board():

    return [
        [EMPTY for _ in range(8)]
        for _ in range(8)
    ]


def test_mandatory_capture_excludes_quiet_moves():

    board = empty_board()

    board[5][0] = RED
    board[4][1] = BLACK
    board[2][3] = BLACK

    moves = get_valid_moves(board, RED)

    assert len(moves) == 1

    assert moves[0].start == (5, 0)

    assert moves[0].end == (1, 4)

    assert moves[0].captured == (
        (4, 1),
        (2, 3)
    )


def test_red_man_cannot_capture_backward():

    board = empty_board()

    board[3][2] = RED
    board[4][3] = BLACK

    moves = get_valid_moves(board, RED)

    assert all(
        not move.captured
        for move in moves
    )


def test_king_moves_both_directions():

    board = empty_board()

    board[3][2] = RED_KING

    moves = get_valid_moves(board, RED)

    ends = {
        move.end
        for move in moves
    }

    assert (2, 1) in ends
    assert (4, 1) in ends


def test_promotion_ends_capture_sequence():

    board = empty_board()

    board[2][1] = RED
    board[1][2] = BLACK
    board[1][4] = BLACK

    moves = get_valid_moves(board, RED)

    # Red reaches row 0 after the first jump.
    # Under American rules, the turn ends immediately.

    assert any(
        move.path == ((2, 1), (0, 3))
        for move in moves
    )

    assert all(
        len(move.captured) == 1
        for move in moves
    )
