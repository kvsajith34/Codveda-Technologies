# ♛ N-Queens Solver

A production-quality implementation of the classic **N-Queens Problem** built with Python 3.11, a pure-Python backtracking solver, and an interactive [Streamlit](https://streamlit.io) UI.

---

## 🎯 Problem Statement

Place **N queens** on an **N×N chessboard** such that **no two queens threaten each other** — meaning no two queens share the same row, column, or diagonal.

---

## 📸 Features

| Feature | Description |
|---|---|
| 🎨 **Interactive UI** | Streamlit app with clean, modern design |
| ♟️ **Visual Board** | Chess-coloured board with queen symbols |
| 🔄 **Backtracking Solver** | Correct, efficient, well-commented algorithm |
| 📊 **All Solutions** | Enumerates every valid arrangement for small N |
| ⚡ **Instant Solve** | O(1) constraint checks via hash sets |
| 🧠 **Algorithm Panel** | Built-in complexity analysis and explanation |
| 🛡️ **Edge Cases** | Handles N=1, N=2, N=3, and invalid input gracefully |
| ✅ **Test Suite** | Comprehensive pytest coverage |
| 🐳 **Docker Ready** | One-command containerised deployment |

---

## 🗂️ Project Structure

```
n-queens/
├── app.py                  # Streamlit entry point (UI layer)
├── src/
│   ├── __init__.py
│   ├── solver.py           # Core backtracking algorithm
│   ├── board.py            # 2D board representation & O(1) safety checks
│   └── utils.py            # Display helpers, stats, formatting
├── tests/
│   ├── __init__.py
│   └── test_solver.py      # pytest test suite (~30 tests)
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/n-queens-solver.git
cd n-queens-solver
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

Open your browser at **[http://localhost:8501](http://localhost:8501)**.

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src --cov-report=term-missing

# Run a specific test class
pytest tests/test_solver.py::TestSolveNQueensAll -v
```

Expected output (all tests pass):

```
tests/test_solver.py::TestBoardConstruction::test_valid_board_created         PASSED
tests/test_solver.py::TestBoardConstruction::test_all_cells_empty_on_init     PASSED
...
tests/test_solver.py::TestUtils::test_solution_stats_n8                        PASSED
======= 40+ passed in 1.23s =======
```

---

## 🐳 Docker Deployment

### Build & Run

```bash
# Build the image
docker build -t n-queens-solver .

# Run the container
docker run -p 8501:8501 n-queens-solver

# Access at http://localhost:8501
```

### Docker Compose (optional)

```yaml
# docker-compose.yml
version: "3.9"
services:
  app:
    build: .
    ports:
      - "8501:8501"
    restart: unless-stopped
```

```bash
docker compose up
```

---

## ☁️ Streamlit Community Cloud Deployment

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app** → select your repository.
4. Set **Main file path** to `app.py`.
5. Click **Deploy** — your app is live in ~60 seconds!

---

## 🧠 Algorithm Overview

### Backtracking

The solver places queens **one row at a time**, column by column:

```
1. Start at row 0.
2. For each column in the current row:
   a. Check if placing a queen here is safe (no column/diagonal conflict).
   b. If safe → place queen, recurse to the next row.
   c. If the recursive call fails → remove queen (backtrack), try next column.
3. If all N rows have a queen → solution found!
4. If no column works in the current row → return failure to caller.
```

### Complexity

| Metric | Value | Notes |
|---|---|---|
| **Time** | O(N!) | Bounded by permutations explored; pruning cuts actual work drastically |
| **Space** | O(N) | Recursion depth N + three O(N) constraint sets |
| **Safety Check** | O(1) | Hash-set lookup for column and both diagonals |

### Why Not Brute Force?

Brute force checks all possible placements: **O(N^N)** configurations.  
Backtracking prunes entire branches at the first conflict, achieving practical speeds even for N=15 (2,279,184 solutions).

---

## 📊 Known Solution Counts (OEIS A000170)

| N | Solutions |
|---|---|
| 1 | 1 |
| 2 | 0 |
| 3 | 0 |
| 4 | 2 |
| 5 | 10 |
| 6 | 4 |
| 7 | 40 |
| 8 | 92 |
| 9 | 352 |
| 10 | 724 |
| 12 | 14,200 |
| 15 | 2,279,184 |

---

## 🗺️ Module Reference

### `src/board.py` — `Board`

| Method | Description |
|---|---|
| `place_queen(row, col)` | Place a queen, update constraint sets |
| `remove_queen(row, col)` | Remove a queen (backtrack) |
| `is_safe(row, col)` | O(1) conflict check |
| `queen_positions()` | List of (row, col) for all queens |
| `copy()` | Deep copy of board state |
| `reset()` | Clear all queens |

### `src/solver.py` — Solver Functions

| Function | Description |
|---|---|
| `solve_n_queens(n)` | Find first solution; returns `list[int] \| None` |
| `solve_n_queens_all(n, limit)` | Find all solutions |
| `count_solutions(n)` | Count solutions memory-efficiently |
| `iter_solutions(n, limit)` | Lazy generator of solutions |
| `solution_to_board(n, placement)` | Convert list to Board object |

### `src/utils.py` — Utilities

| Function | Description |
|---|---|
| `validate_n(n)` | Input validation with error message |
| `get_solution_stats(n)` | Solve + collect statistics |
| `board_to_text(board)` | ASCII board render |
| `get_algorithm_explanation()` | UI explanation strings |
| `format_solve_time(ms)` | Human-readable time |

---

## 💡 Design Decisions

- **O(1) safety checks** — Three hash sets eliminate O(N) inner loops during conflict detection, a common beginner mistake.
- **Row-by-row placement** — Since each row must have exactly one queen, we eliminate row conflicts structurally rather than checking them.
- **Modular layers** — Board (state), Solver (algorithm), Utils (presentation) are fully decoupled for easy extension or testing.
- **Type hints everywhere** — All functions carry full type annotations for IDE support and self-documentation.
- **No global state** — All functions are pure or operate on explicit Board instances.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🎓 Acknowledgements

- [OEIS A000170](https://oeis.org/A000170) — N-Queens solution sequence
- [Streamlit](https://streamlit.io) — for the excellent Python UI framework

---

*Built with Python 3.11 .*
