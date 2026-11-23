from config import RED, BLACK
from game.board import Board


def test_initial_board_has_twelve_pieces_each():

    board = Board()

    assert sum(
        piece > 0
        for row in board.board
        for piece in row
    ) == 12

    assert sum(
        piece < 0
        for row in board.board
        for piece in row
    ) == 12

    assert board.turn == RED


def test_initial_red_moves_are_available():

    board = Board()

    moves = board.get_all_moves()

    assert len(moves) == 7

    assert all(
        board.board[r][c] == RED
        for r, c in (m.start for m in moves)
    )


def test_move_switches_turn_and_does_not_mutate_clone():

    board = Board()

    clone = board.clone()

    move = board.get_all_moves()[0]

    board.make_move(move)

    assert board.turn == BLACK

    assert clone.turn == RED

    assert clone.board != board.board
