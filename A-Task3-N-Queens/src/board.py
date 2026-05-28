"""
board.py — 2D Chessboard Representation and Safety Logic
=========================================================
This module defines the Board class, which encapsulates the chessboard state,
queen placement, and all constraint-checking logic for the N-Queens problem.

Every safety check is O(1) thanks to tracking sets for columns and diagonals,
making constraint validation extremely fast even for large N.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

QUEEN_SYMBOL: str = "Q"
EMPTY_SYMBOL: str = "."

MIN_BOARD_SIZE: int = 1
MAX_BOARD_SIZE: int = 20  # Beyond 20 the UI becomes impractical


# ---------------------------------------------------------------------------
# Board
# ---------------------------------------------------------------------------


@dataclass
class Board:
    """
    Represents an N×N chessboard for the N-Queens problem.

    Internally, the board is stored as a 2-D list of booleans where
    ``True`` means a queen occupies that cell.  Three auxiliary sets
    track occupied columns and both diagonals so that every ``is_safe``
    call runs in O(1) rather than O(N).

    Attributes
    ----------
    size : int
        The dimension N of the board (N×N).
    grid : list[list[bool]]
        2-D grid; ``grid[row][col] is True`` when a queen is placed there.
    """

    size: int
    grid: list[list[bool]] = field(init=False)

    # O(1) constraint sets ──────────────────────────────────────────────────
    _occupied_cols: set[int] = field(default_factory=set, init=False, repr=False)
    _occupied_diag_main: set[int] = field(
        default_factory=set, init=False, repr=False
    )  # row - col  (top-left → bottom-right)
    _occupied_diag_anti: set[int] = field(
        default_factory=set, init=False, repr=False
    )  # row + col  (top-right → bottom-left)

    def __post_init__(self) -> None:
        """Validate size and initialise an empty grid."""
        if self.size < MIN_BOARD_SIZE:
            raise ValueError(
                f"Board size must be at least {MIN_BOARD_SIZE}, got {self.size}."
            )
        if self.size > MAX_BOARD_SIZE:
            raise ValueError(
                f"Board size must be at most {MAX_BOARD_SIZE}, got {self.size}."
            )
        self.grid = [[False] * self.size for _ in range(self.size)]

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def place_queen(self, row: int, col: int) -> None:
        """
        Place a queen at (row, col) and update constraint sets.

        Parameters
        ----------
        row : int
            Zero-indexed row.
        col : int
            Zero-indexed column.

        Raises
        ------
        ValueError
            If the cell is already occupied or coordinates are out of range.
        """
        self._validate_coords(row, col)
        if self.grid[row][col]:
            raise ValueError(f"Cell ({row}, {col}) is already occupied.")
        self.grid[row][col] = True
        self._occupied_cols.add(col)
        self._occupied_diag_main.add(row - col)
        self._occupied_diag_anti.add(row + col)

    def remove_queen(self, row: int, col: int) -> None:
        """
        Remove the queen from (row, col) and update constraint sets.

        Parameters
        ----------
        row : int
            Zero-indexed row.
        col : int
            Zero-indexed column.

        Raises
        ------
        ValueError
            If the cell is not occupied or coordinates are out of range.
        """
        self._validate_coords(row, col)
        if not self.grid[row][col]:
            raise ValueError(f"Cell ({row}, {col}) has no queen to remove.")
        self.grid[row][col] = False
        self._occupied_cols.discard(col)
        self._occupied_diag_main.discard(row - col)
        self._occupied_diag_anti.discard(row + col)

    def is_safe(self, row: int, col: int) -> bool:
        """
        Check whether placing a queen at (row, col) is safe — i.e. no existing
        queen shares the same column or either diagonal.

        We place queens row by row, so a row conflict is impossible by design.

        Parameters
        ----------
        row : int
            Zero-indexed row to test.
        col : int
            Zero-indexed column to test.

        Returns
        -------
        bool
            ``True`` if no conflict exists, ``False`` otherwise.
        """
        return (
            col not in self._occupied_cols
            and (row - col) not in self._occupied_diag_main
            and (row + col) not in self._occupied_diag_anti
        )

    def queen_positions(self) -> list[tuple[int, int]]:
        """
        Return a list of (row, col) tuples for every placed queen.

        Returns
        -------
        list[tuple[int, int]]
            Queen positions in row-ascending order.
        """
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.grid[r][c]
        ]

    def queen_columns(self) -> list[int]:
        """
        Return the column index of the queen in each row.

        For a complete solution this list has exactly N entries.
        A value of ``-1`` indicates no queen in that row.

        Returns
        -------
        list[int]
            Column indices, one per row.
        """
        result: list[int] = []
        for r in range(self.size):
            col: int = -1
            for c in range(self.size):
                if self.grid[r][c]:
                    col = c
                    break
            result.append(col)
        return result

    def to_symbol_grid(self) -> list[list[str]]:
        """
        Convert the boolean grid to a human-readable symbol grid.

        Returns
        -------
        list[list[str]]
            Grid using ``QUEEN_SYMBOL`` and ``EMPTY_SYMBOL``.
        """
        return [
            [QUEEN_SYMBOL if self.grid[r][c] else EMPTY_SYMBOL for c in range(self.size)]
            for r in range(self.size)
        ]

    def copy(self) -> "Board":
        """
        Return a deep copy of this board.

        Useful when we want to snapshot a solution without sharing mutable state.

        Returns
        -------
        Board
            An independent copy.
        """
        new_board = Board(self.size)
        for r in range(self.size):
            for c in range(self.size):
                new_board.grid[r][c] = self.grid[r][c]
        new_board._occupied_cols = set(self._occupied_cols)
        new_board._occupied_diag_main = set(self._occupied_diag_main)
        new_board._occupied_diag_anti = set(self._occupied_diag_anti)
        return new_board

    def reset(self) -> None:
        """Clear all queens from the board, resetting it to an empty state."""
        self.grid = [[False] * self.size for _ in range(self.size)]
        self._occupied_cols.clear()
        self._occupied_diag_main.clear()
        self._occupied_diag_anti.clear()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _validate_coords(self, row: int, col: int) -> None:
        """Raise ``IndexError`` if (row, col) is outside the board."""
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError(
                f"Coordinates ({row}, {col}) are out of bounds for "
                f"a {self.size}×{self.size} board."
            )

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        rows = ["".join(QUEEN_SYMBOL if cell else EMPTY_SYMBOL for cell in row) for row in self.grid]
        return "\n".join(rows)

    def __str__(self) -> str:
        return self.__repr__()
