"""
test_solver.py — pytest Test Suite for the N-Queens Solver
===========================================================
Covers:
- Board safety checks
- Single-solution correctness
- Solution counts for known N values
- Edge cases (N=1, N=2, N=3)
- Board class functionality
- Utility function validation
- Generator / counter parity
"""

from __future__ import annotations

import pytest

from src.board import Board, MAX_BOARD_SIZE, MIN_BOARD_SIZE
from src.solver import (
    count_solutions,
    iter_solutions,
    solve_n_queens,
    solve_n_queens_all,
    solution_to_board,
)
from src.utils import (
    KNOWN_SOLUTION_COUNTS,
    format_solve_time,
    get_solution_stats,
    ordinal,
    queens_emoji_row,
    validate_n,
)


# ===========================================================================
# Board — construction and validation
# ===========================================================================


class TestBoardConstruction:
    """Tests for Board initialisation and size validation."""

    def test_valid_board_created(self) -> None:
        board = Board(8)
        assert board.size == 8
        assert len(board.grid) == 8
        assert all(len(row) == 8 for row in board.grid)

    def test_all_cells_empty_on_init(self) -> None:
        board = Board(5)
        assert all(not board.grid[r][c] for r in range(5) for c in range(5))

    def test_size_1_valid(self) -> None:
        board = Board(1)
        assert board.size == 1

    def test_size_20_valid(self) -> None:
        board = Board(20)
        assert board.size == 20

    def test_size_0_raises(self) -> None:
        with pytest.raises(ValueError, match="at least"):
            Board(0)

    def test_size_negative_raises(self) -> None:
        with pytest.raises(ValueError):
            Board(-3)

    def test_size_21_raises(self) -> None:
        with pytest.raises(ValueError, match="at most"):
            Board(21)


# ===========================================================================
# Board — queen placement and removal
# ===========================================================================


class TestBoardPlacement:
    """Tests for place_queen, remove_queen, and is_safe."""

    def test_place_queen_marks_cell(self) -> None:
        board = Board(4)
        board.place_queen(0, 1)
        assert board.grid[0][1] is True

    def test_place_queen_marks_constraints(self) -> None:
        board = Board(4)
        board.place_queen(0, 2)
        # Column 2 must be unsafe for any row
        assert not board.is_safe(1, 2), "Same column must be blocked."

    def test_diagonal_main_blocked(self) -> None:
        board = Board(4)
        board.place_queen(0, 0)
        assert not board.is_safe(1, 1), "Main diagonal must be blocked."

    def test_diagonal_anti_blocked(self) -> None:
        board = Board(4)
        board.place_queen(0, 3)
        assert not board.is_safe(1, 2), "Anti-diagonal must be blocked."

    def test_safe_cell_is_safe(self) -> None:
        board = Board(4)
        board.place_queen(0, 0)
        assert board.is_safe(1, 2), "(1, 2) should be safe after queen at (0, 0)."

    def test_remove_queen_unmarks_cell(self) -> None:
        board = Board(4)
        board.place_queen(0, 1)
        board.remove_queen(0, 1)
        assert board.grid[0][1] is False

    def test_remove_queen_restores_safety(self) -> None:
        board = Board(4)
        board.place_queen(0, 1)
        board.remove_queen(0, 1)
        assert board.is_safe(2, 1), "Column should be free after queen removal."

    def test_place_already_occupied_raises(self) -> None:
        board = Board(4)
        board.place_queen(0, 0)
        with pytest.raises(ValueError, match="already occupied"):
            board.place_queen(0, 0)

    def test_remove_empty_cell_raises(self) -> None:
        board = Board(4)
        with pytest.raises(ValueError, match="no queen"):
            board.remove_queen(0, 0)

    def test_out_of_bounds_raises(self) -> None:
        board = Board(4)
        with pytest.raises(IndexError):
            board.place_queen(4, 0)

    def test_queen_positions(self) -> None:
        board = Board(4)
        board.place_queen(0, 1)
        board.place_queen(1, 3)
        positions = board.queen_positions()
        assert (0, 1) in positions
        assert (1, 3) in positions
        assert len(positions) == 2

    def test_reset_clears_board(self) -> None:
        board = Board(4)
        board.place_queen(0, 1)
        board.place_queen(1, 3)
        board.reset()
        assert board.queen_positions() == []
        assert board.is_safe(0, 1)

    def test_copy_is_independent(self) -> None:
        board = Board(4)
        board.place_queen(0, 0)
        copy = board.copy()
        copy.place_queen(1, 2)
        # Original must be unchanged
        assert len(board.queen_positions()) == 1
        assert len(copy.queen_positions()) == 2


# ===========================================================================
# Solver — single solution
# ===========================================================================


class TestSolveNQueens:
    """Tests for solve_n_queens (first solution only)."""

    def test_n1_has_solution(self) -> None:
        result = solve_n_queens(1)
        assert result == [0]

    def test_n2_no_solution(self) -> None:
        assert solve_n_queens(2) is None

    def test_n3_no_solution(self) -> None:
        assert solve_n_queens(3) is None

    def test_n4_solution_valid(self) -> None:
        placement = solve_n_queens(4)
        assert placement is not None
        assert len(placement) == 4
        _assert_valid_placement(4, placement)

    def test_n8_solution_valid(self) -> None:
        placement = solve_n_queens(8)
        assert placement is not None
        assert len(placement) == 8
        _assert_valid_placement(8, placement)

    @pytest.mark.parametrize("n", [4, 5, 6, 7, 8, 9, 10])
    def test_solution_valid_for_various_n(self, n: int) -> None:
        placement = solve_n_queens(n)
        assert placement is not None
        _assert_valid_placement(n, placement)


# ===========================================================================
# Solver — all solutions and counts
# ===========================================================================


class TestSolveNQueensAll:
    """Tests for solve_n_queens_all and count_solutions."""

    @pytest.mark.parametrize(
        "n, expected_count",
        [
            (1, 1),
            (2, 0),
            (3, 0),
            (4, 2),
            (5, 10),
            (6, 4),
            (7, 40),
            (8, 92),
        ],
    )
    def test_solution_count_matches_known(self, n: int, expected_count: int) -> None:
        solutions = solve_n_queens_all(n)
        assert len(solutions) == expected_count, (
            f"Expected {expected_count} solutions for N={n}, got {len(solutions)}."
        )

    def test_all_solutions_are_valid_n4(self) -> None:
        solutions = solve_n_queens_all(4)
        for placement in solutions:
            _assert_valid_placement(4, placement)

    def test_all_solutions_are_valid_n8(self) -> None:
        solutions = solve_n_queens_all(8)
        for placement in solutions:
            _assert_valid_placement(8, placement)

    def test_solutions_are_unique(self) -> None:
        solutions = solve_n_queens_all(6)
        tuples = [tuple(s) for s in solutions]
        assert len(tuples) == len(set(tuples)), "Duplicate solutions found."

    def test_limit_parameter(self) -> None:
        solutions = solve_n_queens_all(8, limit=5)
        assert len(solutions) == 5

    @pytest.mark.parametrize(
        "n, expected_count",
        [
            (1, 1),
            (4, 2),
            (5, 10),
            (8, 92),
        ],
    )
    def test_count_solutions_matches_known(self, n: int, expected_count: int) -> None:
        assert count_solutions(n) == expected_count

    def test_count_matches_all_length(self) -> None:
        for n in range(1, 9):
            assert count_solutions(n) == len(solve_n_queens_all(n)), (
                f"count_solutions({n}) disagrees with len(solve_n_queens_all({n}))."
            )


# ===========================================================================
# Solver — iterator
# ===========================================================================


class TestIterSolutions:
    """Tests for the generator-based iter_solutions."""

    def test_iter_yields_correct_count_n4(self) -> None:
        solutions = list(iter_solutions(4))
        assert len(solutions) == 2

    def test_iter_limit_respected(self) -> None:
        solutions = list(iter_solutions(8, limit=10))
        assert len(solutions) == 10

    def test_iter_solutions_are_valid(self) -> None:
        for placement in iter_solutions(6):
            _assert_valid_placement(6, placement)

    def test_iter_n2_yields_nothing(self) -> None:
        solutions = list(iter_solutions(2))
        assert solutions == []


# ===========================================================================
# Solver — solution_to_board
# ===========================================================================


class TestSolutionToBoard:
    """Tests for solution_to_board conversion helper."""

    def test_converts_correctly(self) -> None:
        placement = [1, 3, 0, 2]
        board = solution_to_board(4, placement)
        assert board.grid[0][1] is True
        assert board.grid[1][3] is True
        assert board.grid[2][0] is True
        assert board.grid[3][2] is True

    def test_wrong_length_raises(self) -> None:
        with pytest.raises(ValueError, match="length"):
            solution_to_board(4, [0, 1, 2])

    def test_invalid_column_raises(self) -> None:
        with pytest.raises(ValueError, match="out of range"):
            solution_to_board(4, [0, 1, 4, 2])


# ===========================================================================
# Utilities
# ===========================================================================


class TestUtils:
    """Tests for utils.py helper functions."""

    # validate_n
    def test_validate_n_valid(self) -> None:
        ok, _ = validate_n(8)
        assert ok

    def test_validate_n_too_small(self) -> None:
        ok, msg = validate_n(0)
        assert not ok
        assert "≥" in msg

    def test_validate_n_too_large(self) -> None:
        ok, msg = validate_n(21)
        assert not ok
        assert "≤" in msg

    def test_validate_n_wrong_type(self) -> None:
        ok, msg = validate_n("eight")  # type: ignore[arg-type]
        assert not ok

    # format_solve_time
    def test_format_solve_time_sub_ms(self) -> None:
        assert format_solve_time(0.5) == "< 1 ms"

    def test_format_solve_time_ms(self) -> None:
        result = format_solve_time(123.4)
        assert "ms" in result

    def test_format_solve_time_seconds(self) -> None:
        result = format_solve_time(2500.0)
        assert "s" in result

    # ordinal
    def test_ordinal_1st(self) -> None:
        assert ordinal(1) == "1st"

    def test_ordinal_2nd(self) -> None:
        assert ordinal(2) == "2nd"

    def test_ordinal_3rd(self) -> None:
        assert ordinal(3) == "3rd"

    def test_ordinal_11th(self) -> None:
        assert ordinal(11) == "11th"

    def test_ordinal_21st(self) -> None:
        assert ordinal(21) == "21st"

    # queens_emoji_row
    def test_queens_emoji_row_queen_position(self) -> None:
        row = queens_emoji_row(4, 2)
        assert row == "⬜⬜👑⬜"

    def test_queens_emoji_row_first_col(self) -> None:
        row = queens_emoji_row(3, 0)
        assert row.startswith("👑")

    # get_solution_stats
    def test_solution_stats_n8(self) -> None:
        stats = get_solution_stats(8)
        assert stats["n"] == 8
        assert stats["has_solution"] is True
        assert stats["total_count"] == 92
        assert stats["solve_time_ms"] >= 0

    def test_solution_stats_n2_no_solution(self) -> None:
        stats = get_solution_stats(2)
        assert stats["has_solution"] is False
        assert stats["total_count"] == 0


# ===========================================================================
# Helper — verify a placement is genuinely conflict-free
# ===========================================================================


def _assert_valid_placement(n: int, placement: list[int]) -> None:
    """
    Assert that a placement list is a valid N-Queens solution.

    Checks:
    - Correct length.
    - All column values in [0, N-1].
    - No two queens share a column.
    - No two queens share a main diagonal (row - col).
    - No two queens share an anti-diagonal (row + col).
    """
    assert len(placement) == n, f"Placement length {len(placement)} != {n}."

    cols: set[int] = set()
    diag_main: set[int] = set()
    diag_anti: set[int] = set()

    for row, col in enumerate(placement):
        assert 0 <= col < n, f"Column {col} out of range for N={n}."
        assert col not in cols, f"Column {col} conflict at row {row}."
        assert (row - col) not in diag_main, f"Main diagonal conflict at ({row}, {col})."
        assert (row + col) not in diag_anti, f"Anti-diagonal conflict at ({row}, {col})."

        cols.add(col)
        diag_main.add(row - col)
        diag_anti.add(row + col)
