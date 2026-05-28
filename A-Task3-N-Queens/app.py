"""
app.py — N-Queens Solver · Streamlit Application
==================================================
Entry point for the Streamlit interactive UI.

Run locally:
    streamlit run app.py

Deploy to Streamlit Community Cloud:
    Push this repo to GitHub, connect on share.streamlit.io, set app.py as
    the entry point.
"""

from __future__ import annotations

import streamlit as st

from src.solver import solution_to_board
from src.utils import (
    ALL_SOLUTIONS_THRESHOLD,
    KNOWN_SOLUTION_COUNTS,
    board_to_text,
    format_solve_time,
    get_algorithm_explanation,
    get_solution_stats,
    ordinal,
    queens_emoji_row,
    validate_n,
)

# ---------------------------------------------------------------------------
# Page configuration (must be the first Streamlit call)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="N-Queens Solver",
    page_icon="♛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — minimal, modern, internship-demo ready
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }

    /* ── Header ── */
    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #64748b;
        margin-top: 0.4rem;
    }
    .badge {
        display: inline-block;
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 9999px;
        padding: 2px 12px;
        font-size: 0.78rem;
        font-weight: 500;
        color: #475569;
        margin-right: 6px;
        margin-bottom: 4px;
    }

    /* ── Chessboard ── */
    .chess-wrapper {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0;
    }
    .chess-table {
        border-collapse: collapse;
        border: 3px solid #334155;
        border-radius: 6px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.18);
    }
    .chess-cell {
        width: 54px;
        height: 54px;
        text-align: center;
        vertical-align: middle;
        font-size: 1.9rem;
        line-height: 54px;
        position: relative;
        transition: transform 0.15s ease;
    }
    .chess-cell:hover { transform: scale(1.08); cursor: default; }
    .cell-light  { background-color: #f0d9b5; }
    .cell-dark   { background-color: #b58863; }
    .cell-queen-light { background-color: #f6f669; }
    .cell-queen-dark  { background-color: #baca2b; }

    /* ── Stat cards ── */
    .stat-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.4rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .stat-label { font-size: 0.78rem; color: #94a3b8; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
    .stat-value { font-size: 1.8rem; font-weight: 700; color: #1e293b; margin-top: 2px; }

    /* ── Algorithm card ── */
    .algo-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-left: 4px solid #6366f1;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .algo-card h4 { color: #4338ca; font-weight: 600; margin-bottom: 0.4rem; font-size: 0.95rem; }

    /* ── Solution grid (all solutions) ── */
    .sol-mini-board {
        font-family: monospace;
        font-size: 0.82rem;
        background: #1e293b;
        color: #f8fafc;
        border-radius: 8px;
        padding: 0.6rem 0.8rem;
        line-height: 1.6;
        white-space: pre;
    }

    /* ── Sidebar ── */
    .sidebar-section { margin-bottom: 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Sidebar — controls
# ---------------------------------------------------------------------------


def render_sidebar() -> tuple[int, bool, bool]:
    """
    Render the sidebar input controls.

    Returns
    -------
    tuple[int, bool, bool]
        ``(n, show_all_solutions, show_explanation)``
    """
    st.sidebar.markdown("## ♛ N-Queens Solver")
    st.sidebar.markdown("---")

    st.sidebar.markdown("### Board Configuration")
    n = st.sidebar.slider(
        label="Board size (N)",
        min_value=1,
        max_value=20,
        value=8,
        step=1,
        help="Select the board size N. The solver places N queens on an N×N board.",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Display Options")

    show_all = st.sidebar.checkbox(
        "Show all solutions",
        value=True,
        help=f"Enumerate every valid solution (available for N ≤ {ALL_SOLUTIONS_THRESHOLD}).",
    )

    show_explanation = st.sidebar.checkbox(
        "Show algorithm explanation",
        value=True,
        help="Display the backtracking algorithm explanation and complexity analysis.",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='font-size:0.8rem; color:#94a3b8;'>
        <b>Internship Project</b><br>
        Codveda Technologies · Level 3<br>
        Task 3: N-Queens Problem<br><br>
        Algorithm: Backtracking<br>
        Language: Python 3.11+<br>
        UI: Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )

    return n, show_all, show_explanation


# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------


def render_header() -> None:
    """Render the page title and badge strip."""
    st.markdown(
        """
        <div style="margin-bottom:1.5rem;">
            <p class="hero-title">♛ N-Queens Solver</p>
            <p class="hero-subtitle">
                Place N queens on an N×N chessboard so no two queens threaten each other.
            </p>
            <span class="badge">🐍 Python 3.11</span>
            <span class="badge">🔄 Backtracking</span>
            <span class="badge">📊 Streamlit</span>
            <span class="badge">🎓 Codveda Internship</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Board renderer
# ---------------------------------------------------------------------------


def render_chessboard(n: int, placement: list[int], title: str = "Solution") -> None:
    """
    Render a chessboard with queen placements using HTML.

    Parameters
    ----------
    n : int
        Board size.
    placement : list[int]
        Column index per row.
    title : str
        Section title displayed above the board.
    """
    cells_html = ""
    for row in range(n):
        cells_html += "<tr>"
        for col in range(n):
            is_queen = placement[row] == col
            is_light = (row + col) % 2 == 0

            if is_queen:
                css_class = "chess-cell cell-queen-light" if is_light else "chess-cell cell-queen-dark"
                content = "♛"
            else:
                css_class = "chess-cell cell-light" if is_light else "chess-cell cell-dark"
                content = ""

            cells_html += f'<td class="{css_class}">{content}</td>'
        cells_html += "</tr>"

    # Column labels
    col_labels = "".join(
        f'<th style="text-align:center;font-size:0.75rem;color:#94a3b8;font-weight:500;padding:4px 0;">'
        f'{chr(65 + c)}</th>'
        for c in range(n)
    )
    row_labels_map = {r: str(n - r) for r in range(n)}

    full_rows = ""
    for row in range(n):
        full_rows += (
            f'<tr><td style="text-align:right;font-size:0.72rem;color:#94a3b8;'
            f'padding-right:6px;font-weight:500;">{row_labels_map[row]}</td>'
        )
        for col in range(n):
            is_queen = placement[row] == col
            is_light = (row + col) % 2 == 0
            if is_queen:
                css_class = "chess-cell cell-queen-light" if is_light else "chess-cell cell-queen-dark"
                content = "♛"
            else:
                css_class = "chess-cell cell-light" if is_light else "chess-cell cell-dark"
                content = ""
            full_rows += f'<td class="{css_class}">{content}</td>'
        full_rows += "</tr>"

    board_html = f"""
    <div class="chess-wrapper">
      <div>
        <table>
          <tr><td></td>{col_labels}</tr>
          {full_rows}
        </table>
      </div>
    </div>
    """
    st.markdown(f"#### {title}")
    st.markdown(board_html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Stats row
# ---------------------------------------------------------------------------


def render_stats(stats: dict) -> None:
    """
    Render key metrics as a row of stat cards.

    Parameters
    ----------
    stats : dict
        Output of ``get_solution_stats``.
    """
    n = stats["n"]
    total = stats["total_count"]
    solve_time = format_solve_time(stats["solve_time_ms"])
    has_solution = stats["has_solution"]
    count_is_exact = stats["count_is_exact"]

    count_display = (
        f"{total:,}" if total >= 0 else "N/A"
    )
    if not count_is_exact and total >= 0:
        count_display = f"~{count_display}"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f'<div class="stat-card">'
            f'<div class="stat-label">Board Size</div>'
            f'<div class="stat-value">{n}×{n}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="stat-card">'
            f'<div class="stat-label">Total Solutions</div>'
            f'<div class="stat-value">{count_display}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with col3:
        status_icon = "✅" if has_solution else "❌"
        status_text = "Solvable" if has_solution else "No Solution"
        st.markdown(
            f'<div class="stat-card">'
            f'<div class="stat-label">Status</div>'
            f'<div class="stat-value" style="font-size:1.3rem;">{status_icon} {status_text}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f'<div class="stat-card">'
            f'<div class="stat-label">Solve Time</div>'
            f'<div class="stat-value" style="font-size:1.4rem;">{solve_time}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# All solutions grid
# ---------------------------------------------------------------------------


def render_all_solutions(n: int, solutions: list[list[int]]) -> None:
    """
    Render a compact grid of mini-boards for all solutions.

    Parameters
    ----------
    n : int
        Board size.
    solutions : list[list[int]]
        All valid placements.
    """
    if not solutions:
        return

    st.markdown(f"### All {len(solutions):,} Solutions")

    cols_per_row = min(4, len(solutions))
    groups = [solutions[i : i + cols_per_row] for i in range(0, len(solutions), cols_per_row)]

    for group in groups:
        cols = st.columns(len(group))
        for idx, (col, placement) in enumerate(zip(cols, group)):
            sol_number = solutions.index(placement) + 1
            with col:
                mini = "\n".join(queens_emoji_row(n, placement[r]) for r in range(n))
                st.markdown(
                    f'<div class="sol-mini-board">{mini}</div>',
                    unsafe_allow_html=True,
                )
                st.caption(f"Solution {sol_number}")


# ---------------------------------------------------------------------------
# Algorithm explanation panel
# ---------------------------------------------------------------------------


def render_explanation() -> None:
    """Render the algorithm explanation section."""
    exp = get_algorithm_explanation()

    st.markdown("### 🧠 Algorithm Explanation")

    st.markdown(
        f'<div class="algo-card"><h4>📖 Overview</h4><p style="color:#334155;font-size:0.92rem;">'
        f'{exp["overview"]}</p></div>',
        unsafe_allow_html=True,
    )

    with st.expander("🔢 Step-by-Step Algorithm", expanded=True):
        st.markdown(exp["steps"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="algo-card"><h4>⏱ Time Complexity</h4>'
            f'<p style="color:#334155;font-size:0.9rem;">{exp["time_complexity"]}</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="algo-card"><h4>💾 Space Complexity</h4>'
            f'<p style="color:#334155;font-size:0.9rem;">{exp["space_complexity"]}</p></div>',
            unsafe_allow_html=True,
        )

    with st.expander("⚡ Why Backtracking?"):
        st.markdown(exp["why_backtracking"])

    with st.expander("✂️ Constraint Pruning Details"):
        st.markdown(exp["pruning"])

    # Known counts table
    st.markdown("#### 📊 Known Solution Counts (OEIS A000170)")
    table_rows = ""
    for board_n, count in KNOWN_SOLUTION_COUNTS.items():
        highlight = "background:#eef2ff;" if board_n == 8 else ""
        table_rows += (
            f"<tr style='{highlight}'>"
            f"<td style='padding:6px 16px;text-align:center;'>{board_n}</td>"
            f"<td style='padding:6px 16px;text-align:center;'>{count:,}</td>"
            f"</tr>"
        )
    st.markdown(
        f"""
        <table style='border-collapse:collapse;width:100%;max-width:400px;
                      border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;'>
          <thead>
            <tr style='background:#f8fafc;'>
              <th style='padding:8px 16px;color:#475569;font-size:0.85rem;'>N</th>
              <th style='padding:8px 16px;color:#475569;font-size:0.85rem;'>Solutions</th>
            </tr>
          </thead>
          <tbody>{table_rows}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Edge-case info banners
# ---------------------------------------------------------------------------


def render_edge_case_info(n: int, has_solution: bool) -> None:
    """
    Display contextual information for edge cases (N=1, N=2, N=3).

    Parameters
    ----------
    n : int
        Board size.
    has_solution : bool
        Whether a solution exists.
    """
    if n == 1:
        st.info(
            "**N = 1:** Trivial case — a single queen on a 1×1 board is always safe. "
            "1 solution exists.",
            icon="♟️",
        )
    elif n in (2, 3):
        st.warning(
            f"**N = {n}:** No valid arrangement exists for a {n}×{n} board. "
            "Queens inevitably conflict. Try N ≥ 4.",
            icon="⚠️",
        )
    elif not has_solution:
        st.error(f"No solution found for N = {n}.", icon="❌")


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------


def main() -> None:
    """Main Streamlit application entry point."""
    n, show_all, show_explanation = render_sidebar()
    render_header()

    # ── Validate ──────────────────────────────────────────────────────────
    valid, error_msg = validate_n(n)
    if not valid:
        st.error(f"Invalid input: {error_msg}")
        return

    # ── Solve ─────────────────────────────────────────────────────────────
    with st.spinner(f"Solving {n}-Queens..."):
        stats = get_solution_stats(n)

    # ── Edge case banners ─────────────────────────────────────────────────
    render_edge_case_info(n, stats["has_solution"])

    # ── Stats ─────────────────────────────────────────────────────────────
    st.markdown("### 📈 Results")
    render_stats(stats)

    if not stats["has_solution"]:
        st.markdown("---")
        if show_explanation:
            render_explanation()
        return

    st.markdown("---")

    # ── Primary board ─────────────────────────────────────────────────────
    left_col, right_col = st.columns([3, 2])

    with left_col:
        render_chessboard(
            n,
            stats["first_solution"],
            title=f"First Solution — {n}-Queens Board",
        )

    with right_col:
        st.markdown("#### ♛ Queen Placement")
        st.markdown(
            "Column of the queen in each row (0-indexed):"
        )
        placement = stats["first_solution"]
        for row_idx, col_idx in enumerate(placement):
            col_letter = chr(65 + col_idx)
            row_number = n - row_idx
            st.markdown(
                f"&nbsp;&nbsp;`Row {row_idx + 1}` → **Column {col_idx}** ({col_letter}{row_number})"
            )

        st.markdown("---")
        st.markdown("#### 📋 Text Representation")
        board_obj = solution_to_board(n, placement)
        st.code(board_to_text(board_obj), language=None)

    st.markdown("---")

    # ── All solutions ─────────────────────────────────────────────────────
    if show_all and n <= ALL_SOLUTIONS_THRESHOLD:
        render_all_solutions(n, stats["all_solutions"])
        st.markdown("---")
    elif show_all and n > ALL_SOLUTIONS_THRESHOLD:
        known = KNOWN_SOLUTION_COUNTS.get(n)
        msg = (
            f"Enumerating all solutions for N={n} is computationally intensive. "
            f"The known total is **{known:,}** solutions (OEIS A000170)."
            if known
            else f"Enumerating all solutions for N={n} is computationally intensive."
        )
        st.info(msg, icon="ℹ️")

    # ── Algorithm ─────────────────────────────────────────────────────────
    if show_explanation:
        render_explanation()


if __name__ == "__main__":
    main()
