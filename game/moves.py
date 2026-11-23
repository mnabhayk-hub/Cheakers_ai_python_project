"""Legal move generation for American Checkers."""

from dataclasses import dataclass

from config import (
    RED, BLACK, RED_KING, BLACK_KING,
    EMPTY, ROWS, COLS
)


@dataclass(frozen=True)
class Move:
    path: tuple
    captured: tuple = ()

    @property
    def start(self):
        return self.path[0]

    @property
    def end(self):
        return self.path[-1]


def _inside(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS


def _directions(piece):

    if piece == RED:
        return ((-1, -1), (-1, 1))

    if piece == BLACK:
        return ((1, -1), (1, 1))

    if piece in (RED_KING, BLACK_KING):
        return (
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        )

    return ()


def _capture_sequences(board, start, player):
    """Return all complete capture paths beginning at start."""

    row, col = start
    piece = board[row][col]
    results = []

    def walk(current_board, current_pos, current_piece, path, captured):

        r, c = current_pos
        found_jump = False

        for dr, dc in _directions(current_piece):

            mid = (r + dr, c + dc)
            landing = (r + 2 * dr, c + 2 * dc)

            if not _inside(*landing) or not _inside(*mid):
                continue

            mr, mc = mid
            lr, lc = landing

            if (
                current_board[mr][mc] * player < 0
                and current_board[lr][lc] == EMPTY
            ):

                found_jump = True

                next_board = [line[:] for line in current_board]

                next_board[r][c] = EMPTY
                next_board[mr][mc] = EMPTY

                next_piece = current_piece
                promoted = False

                if current_piece == RED and lr == 0:
                    next_piece = RED_KING
                    promoted = True

                elif current_piece == BLACK and lr == ROWS - 1:
                    next_piece = BLACK_KING
                    promoted = True

                next_board[lr][lc] = next_piece

                next_path = path + (landing,)
                next_captured = captured + (mid,)

                # Promotion ends the turn under American Checkers rules.
                if promoted:

                    results.append(
                        Move(next_path, next_captured)
                    )

                else:

                    walk(
                        next_board,
                        landing,
                        next_piece,
                        next_path,
                        next_captured
                    )

        if not found_jump and captured:
            results.append(Move(path, captured))

    walk(board, start, piece, (start,), ())

    return results


def get_valid_moves(board, player):
    """Return legal moves. Captures are mandatory."""

    captures = []

    for row in range(ROWS):
        for col in range(COLS):

            if board[row][col] * player > 0:

                captures.extend(
                    _capture_sequences(
                        board,
                        (row, col),
                        player
                    )
                )

    if captures:
        return captures

    moves = []

    for row in range(ROWS):
        for col in range(COLS):

            piece = board[row][col]

            if piece * player <= 0:
                continue

            for dr, dc in _directions(piece):

                nr = row + dr
                nc = col + dc

                if _inside(nr, nc) and board[nr][nc] == EMPTY:

                    moves.append(
                        Move(
                            ((row, col), (nr, nc)),
                            ()
                        )
                    )

    return moves
