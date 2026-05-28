"""
solver.py — N-Queens Backtracking Solver
=========================================
This module contains the core algorithm for solving the N-Queens problem.

Algorithm Overview
------------------
We use **backtracking**, a depth-first search technique that:

1. Places queens one row at a time (left-to-right sweep of columns).
2. Before placing, checks if the cell is safe (no column/diagonal conflicts).
3. If safe, places the queen and recurses to the next row.
4. If no column in the current row is safe, *backtracks* to the previous row
   and tries the next column there.
5. Terminates when all N rows have a queen (a solution is found) or all
   possibilities are exhausted.

Time Complexity  : O(N!)  — bounded by the number of permutations explored.
Space Complexity : O(N)   — recursion depth + constraint sets.

This is drastically better than brute force (O(N^N)) because we prune entire
subtrees the moment a conflict is detected.
"""

from __future__ import annotations

from typing import Generator, Optional

from src.board import Board


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def solve_n_queens(n: int) -> Optional[list[int]]:
    """
    Find *one* valid solution to the N-Queens problem.

    Returns the first solution discovered by the backtracking search as a list
    of column indices (one per row).  Returns ``None`` when no solution exists
    (e.g. N == 2 or N == 3).

    Parameters
    ----------
    n : int
        Board size (N queens on an N×N board).

    Returns
    -------
    list[int] | None
        Column indices where queens are placed (index 0 = row 0), or ``None``
        if no solution exists.

    Examples
    --------
    >>> solve_n_queens(4)
    [1, 3, 0, 2]
    >>> solve_n_queens(2)
    None
    """
    board = Board(n)
    result: list[int] = []
    if _backtrack(board, row=0, placement=result):
        return result
    return None


def solve_n_queens_all(n: int, limit: Optional[int] = None) -> list[list[int]]:
    """
    Find *all* valid solutions to the N-Queens problem.

    Parameters
    ----------
    n : int
        Board size.
    limit : int | None
        Optional cap on the number of solutions returned.  Useful for large N
        where collecting all solutions is impractical.

    Returns
    -------
    list[list[int]]
        Each inner list contains N column indices (one per row).

    Examples
    --------
    >>> len(solve_n_queens_all(4))
    2
    >>> len(solve_n_queens_all(8))
    92
    """
    solutions: list[list[int]] = []
    board = Board(n)
    _backtrack_all(board, row=0, current=[], solutions=solutions, limit=limit)
    return solutions


def count_solutions(n: int) -> int:
    """
    Count the total number of distinct N-Queens solutions without storing them.

    This is more memory-efficient than ``solve_n_queens_all`` when you only
    need the count.

    Parameters
    ----------
    n : int
        Board size.

    Returns
    -------
    int
        Number of valid configurations.

    Examples
    --------
    >>> count_solutions(1)
    1
    >>> count_solutions(4)
    2
    >>> count_solutions(8)
    92
    """
    board = Board(n)
    return _count_backtrack(board, row=0)


def solution_to_board(n: int, placement: list[int]) -> Board:
    """
    Convert a placement list (column-per-row) back into a ``Board`` object.

    Parameters
    ----------
    n : int
        Board size.
    placement : list[int]
        Column index for each row.

    Returns
    -------
    Board
        A Board with queens placed according to ``placement``.

    Raises
    ------
    ValueError
        If ``placement`` has wrong length or contains invalid column indices.
    """
    if len(placement) != n:
        raise ValueError(
            f"Placement list length {len(placement)} does not match board size {n}."
        )
    board = Board(n)
    for row, col in enumerate(placement):
        if not (0 <= col < n):
            raise ValueError(
                f"Column index {col} in row {row} is out of range [0, {n - 1}]."
            )
        board.place_queen(row, col)
    return board


def iter_solutions(n: int, limit: Optional[int] = None) -> Generator[list[int], None, None]:
    """
    Generator that yields N-Queens solutions one at a time.

    Memory-efficient alternative to ``solve_n_queens_all`` — solutions are
    produced lazily, so you can stop early without computing all of them.

    Parameters
    ----------
    n : int
        Board size.
    limit : int | None
        Maximum number of solutions to yield.

    Yields
    ------
    list[int]
        Column placement per row for each valid solution.
    """
    count = 0
    board = Board(n)
    for solution in _generate_solutions(board, row=0, current=[]):
        yield solution
        count += 1
        if limit is not None and count >= limit:
            return


# ---------------------------------------------------------------------------
# Internal backtracking helpers
# ---------------------------------------------------------------------------


def _backtrack(board: Board, row: int, placement: list[int]) -> bool:
    """
    Recursive backtracking to find the *first* valid solution.

    Places one queen per row, column by column.  Returns ``True`` as soon as a
    complete solution is found, stopping the search immediately.

    Parameters
    ----------
    board : Board
        Mutable board object shared across recursive calls.
    row : int
        Current row being processed (0-indexed).
    placement : list[int]
        Accumulates the column chosen for each row.

    Returns
    -------
    bool
        ``True`` if a solution was found at or below this row.
    """
    # Base case: all N queens placed — solution complete
    if row == board.size:
        return True

    for col in range(board.size):
        if board.is_safe(row, col):
            # ── Place queen ──────────────────────────────────────────────
            board.place_queen(row, col)
            placement.append(col)

            # ── Recurse to next row ──────────────────────────────────────
            if _backtrack(board, row + 1, placement):
                return True  # Propagate success upward immediately

            # ── Backtrack: undo placement, try next column ───────────────
            board.remove_queen(row, col)
            placement.pop()

    # No valid column found in this row → signal failure to caller
    return False


def _backtrack_all(
    board: Board,
    row: int,
    current: list[int],
    solutions: list[list[int]],
    limit: Optional[int],
) -> None:
    """
    Recursive backtracking that collects *all* valid solutions.

    Unlike ``_backtrack``, this does **not** stop after finding the first
    solution — it continues until all branches are explored (or ``limit`` is
    reached).

    Parameters
    ----------
    board : Board
        Shared mutable board.
    row : int
        Current row being processed.
    current : list[int]
        Column choices so far (one per row already processed).
    solutions : list[list[int]]
        Accumulator for complete solutions.
    limit : int | None
        If set, stops collecting once this many solutions are found.
    """
    if limit is not None and len(solutions) >= limit:
        return

    if row == board.size:
        # Snapshot current placement as a new list before appending
        solutions.append(list(current))
        return

    for col in range(board.size):
        if board.is_safe(row, col):
            board.place_queen(row, col)
            current.append(col)

            _backtrack_all(board, row + 1, current, solutions, limit)

            board.remove_queen(row, col)
            current.pop()


def _count_backtrack(board: Board, row: int) -> int:
    """
    Recursive backtracking that *counts* solutions without storing them.

    Parameters
    ----------
    board : Board
        Shared mutable board.
    row : int
        Current row being processed.

    Returns
    -------
    int
        Number of valid solutions found at or below this row.
    """
    if row == board.size:
        return 1  # One complete solution found

    total = 0
    for col in range(board.size):
        if board.is_safe(row, col):
            board.place_queen(row, col)
            total += _count_backtrack(board, row + 1)
            board.remove_queen(row, col)
    return total


def _generate_solutions(
    board: Board, row: int, current: list[int]
) -> Generator[list[int], None, None]:
    """
    Generator-based backtracking for lazy solution enumeration.

    Parameters
    ----------
    board : Board
        Shared mutable board.
    row : int
        Current row being processed.
    current : list[int]
        Column choices accumulated so far.

    Yields
    ------
    list[int]
        Each complete solution as a snapshot list.
    """
    if row == board.size:
        yield list(current)
        return

    for col in range(board.size):
        if board.is_safe(row, col):
            board.place_queen(row, col)
            current.append(col)

            yield from _generate_solutions(board, row + 1, current)

            board.remove_queen(row, col)
            current.pop()
