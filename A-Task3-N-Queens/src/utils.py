"""
utils.py — Display Helpers, Statistics, and Formatting Utilities
================================================================
This module provides pure functions for formatting solutions, generating
board statistics, and building UI-ready data structures.  All functions
are stateless and have no side effects.
"""

from __future__ import annotations

import math
import time
from typing import Any

from src.board import Board, QUEEN_SYMBOL, EMPTY_SYMBOL
from src.solver import solution_to_board, solve_n_queens, solve_n_queens_all


# ---------------------------------------------------------------------------
# Known solution counts (OEIS A000170) used for instant validation
# ---------------------------------------------------------------------------

KNOWN_SOLUTION_COUNTS: dict[int, int] = {
    1: 1,
    2: 0,
    3: 0,
    4: 2,
    5: 10,
    6: 4,
    7: 40,
    8: 92,
    9: 352,
    10: 724,
    11: 2680,
    12: 14200,
    13: 73712,
    14: 365596,
    15: 2279184,
}

# Threshold below which we enumerate all solutions in the UI
ALL_SOLUTIONS_THRESHOLD: int = 10


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def validate_n(n: Any) -> tuple[bool, str]:
    """
    Validate the user-supplied board size N.

    Parameters
    ----------
    n : Any
        Raw input value (may be int, float, str, etc.).

    Returns
    -------
    tuple[bool, str]
        ``(True, "")`` when valid; ``(False, reason)`` when invalid.
    """
    if not isinstance(n, int):
        return False, f"N must be an integer, got {type(n).__name__}."
    if n < 1:
        return False, f"N must be ≥ 1, got {n}."
    if n > 20:
        return False, f"N must be ≤ 20 to keep computation and display practical, got {n}."
    return True, ""


# ---------------------------------------------------------------------------
# Board formatting helpers
# ---------------------------------------------------------------------------


def board_to_text(board: Board) -> str:
    """
    Render a Board as a plain-text string suitable for printing or logging.

    Example output for N=4::

        . Q . .
        . . . Q
        Q . . .
        . . Q .

    Parameters
    ----------
    board : Board
        The board to render.

    Returns
    -------
    str
        Multi-line string representation.
    """
    symbol_grid = board.to_symbol_grid()
    separator = "+" + "+".join(["-" * 3] * board.size) + "+"
    rows: list[str] = [separator]
    for row in symbol_grid:
        rows.append("| " + " | ".join(f"{cell:^1}" for cell in row) + " |")
        rows.append(separator)
    return "\n".join(rows)


def placement_to_board_html_classes(
    n: int, placement: list[int]
) -> list[list[dict[str, Any]]]:
    """
    Build a grid of cell metadata dicts for rendering a chessboard in the UI.

    Each cell dict contains:
    - ``is_queen`` (bool): queen is placed here.
    - ``is_light`` (bool): light square (standard chessboard colouring).
    - ``row`` (int): zero-indexed row.
    - ``col`` (int): zero-indexed column.

    Parameters
    ----------
    n : int
        Board size.
    placement : list[int]
        Column index per row for a valid solution.

    Returns
    -------
    list[list[dict[str, Any]]]
        2-D list of cell metadata, row-major order.
    """
    grid: list[list[dict[str, Any]]] = []
    for r in range(n):
        row_cells: list[dict[str, Any]] = []
        for c in range(n):
            row_cells.append(
                {
                    "is_queen": placement[r] == c,
                    "is_light": (r + c) % 2 == 0,
                    "row": r,
                    "col": c,
                }
            )
        grid.append(row_cells)
    return grid


# ---------------------------------------------------------------------------
# Solution statistics
# ---------------------------------------------------------------------------


def get_solution_stats(n: int) -> dict[str, Any]:
    """
    Compute or retrieve statistics about N-Queens solutions for board size N.

    For N ≤ ``ALL_SOLUTIONS_THRESHOLD``, the exact count and all solutions are
    computed.  For larger N, only the first solution is found, and the known
    count (if available) is used without re-computing.

    Parameters
    ----------
    n : int
        Board size.

    Returns
    -------
    dict[str, Any]
        Keys: ``n``, ``first_solution``, ``all_solutions``, ``total_count``,
        ``has_solution``, ``solve_time_ms``, ``count_is_exact``.
    """
    start = time.perf_counter()

    first_solution = solve_n_queens(n)
    has_solution = first_solution is not None

    if n <= ALL_SOLUTIONS_THRESHOLD:
        all_solutions = solve_n_queens_all(n)
        total_count = len(all_solutions)
        count_is_exact = True
    else:
        all_solutions = [first_solution] if first_solution else []
        total_count = KNOWN_SOLUTION_COUNTS.get(n, -1)
        count_is_exact = n in KNOWN_SOLUTION_COUNTS

    elapsed_ms = (time.perf_counter() - start) * 1_000

    return {
        "n": n,
        "first_solution": first_solution,
        "all_solutions": all_solutions,
        "total_count": total_count,
        "has_solution": has_solution,
        "solve_time_ms": round(elapsed_ms, 3),
        "count_is_exact": count_is_exact,
    }


# ---------------------------------------------------------------------------
# Algorithm explanation
# ---------------------------------------------------------------------------


def get_algorithm_explanation() -> dict[str, str]:
    """
    Return a structured algorithm explanation for display in the UI.

    Returns
    -------
    dict[str, str]
        Keys: ``overview``, ``steps``, ``time_complexity``, ``space_complexity``,
        ``why_backtracking``, ``pruning``.
    """
    return {
        "overview": (
            "The N-Queens problem asks: how can N chess queens be placed on an N×N "
            "board so that no two queens threaten each other? Queens attack along "
            "rows, columns, and both diagonals, so the solution must ensure all four "
            "directions are conflict-free."
        ),
        "steps": (
            "1. **Start at row 0.** Try placing a queen in each column.\n"
            "2. **Check safety.** Before placing, verify no existing queen shares "
            "the same column or diagonal.\n"
            "3. **Recurse.** If safe, place the queen and move to the next row.\n"
            "4. **Backtrack.** If no column works in the current row, remove the "
            "last queen and try the next column in the previous row.\n"
            "5. **Terminate.** When all N rows have queens, a solution is recorded."
        ),
        "time_complexity": (
            "**O(N!)** — In the worst case we explore N choices for row 0, "
            "(N−1) for row 1 (one column is blocked), and so on.  Pruning via "
            "diagonal checks cuts the actual search space far below N!."
        ),
        "space_complexity": (
            "**O(N)** — Recursion depth is at most N (one level per row), and the "
            "three constraint sets each hold at most N elements."
        ),
        "why_backtracking": (
            "Brute force would check every permutation of N queens across N² cells — "
            "O(N^N) — which is completely impractical.  Backtracking prunes entire "
            "subtrees the moment a conflict is detected, reducing the search to O(N!)."
        ),
        "pruning": (
            "Three O(1) hash sets track occupied columns, main-diagonals (row−col), "
            "and anti-diagonals (row+col).  This eliminates inner loops for conflict "
            "detection, making each safety check a constant-time set lookup."
        ),
    }


# ---------------------------------------------------------------------------
# Miscellaneous helpers
# ---------------------------------------------------------------------------


def format_solve_time(ms: float) -> str:
    """
    Format a solve time in milliseconds to a human-readable string.

    Parameters
    ----------
    ms : float
        Time in milliseconds.

    Returns
    -------
    str
        Formatted string such as ``"< 1 ms"`` or ``"1.234 s"``.
    """
    if ms < 1:
        return "< 1 ms"
    if ms < 1_000:
        return f"{ms:.1f} ms"
    return f"{ms / 1_000:.3f} s"


def ordinal(n: int) -> str:
    """
    Return the ordinal string for a positive integer (e.g. 1 → '1st').

    Parameters
    ----------
    n : int
        Positive integer.

    Returns
    -------
    str
        Ordinal representation.
    """
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def queens_emoji_row(n: int, queen_col: int) -> str:
    """
    Build a single emoji row string for quick terminal/text display.

    Parameters
    ----------
    n : int
        Board width.
    queen_col : int
        Column index (0-based) where the queen sits.

    Returns
    -------
    str
        A string like ``'⬜👑⬜⬜'``.
    """
    return "".join("👑" if c == queen_col else "⬜" for c in range(n))
