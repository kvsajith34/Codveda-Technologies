import { useState, useCallback, useEffect, useRef } from "react";

// ─── Types ──────────────────────────────────────────────────────────────────

interface SolverStats {
  n: number;
  firstSolution: number[] | null;
  allSolutions: number[][];
  totalCount: number;
  hasSolution: boolean;
  solveTimeMs: number;
  countIsExact: boolean;
}

interface BacktrackStep {
  row: number;
  col: number;
  action: "place" | "remove" | "conflict";
  board: number[];
}

// ─── Constants ───────────────────────────────────────────────────────────────

const KNOWN_COUNTS: Record<number, number> = {
  1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92,
  9: 352, 10: 724, 11: 2680, 12: 14200, 13: 73712, 14: 365596, 15: 2279184,
};

// ─── Pure Backtracking Solver (TypeScript port of the Python logic) ──────────

function isSafe(placement: number[], row: number, col: number): boolean {
  for (let r = 0; r < row; r++) {
    const c = placement[r];
    if (c === col) return false;
    if (Math.abs(r - row) === Math.abs(c - col)) return false;
  }
  return true;
}

function solveFirst(n: number): number[] | null {
  const placement: number[] = new Array(n).fill(-1);

  function backtrack(row: number): boolean {
    if (row === n) return true;
    for (let col = 0; col < n; col++) {
      if (isSafe(placement, row, col)) {
        placement[row] = col;
        if (backtrack(row + 1)) return true;
        placement[row] = -1;
      }
    }
    return false;
  }

  return backtrack(0) ? [...placement] : null;
}

function solveAll(n: number, limit = 200): number[][] {
  const solutions: number[][] = [];
  const placement: number[] = new Array(n).fill(-1);

  function backtrack(row: number): void {
    if (solutions.length >= limit) return;
    if (row === n) { solutions.push([...placement]); return; }
    for (let col = 0; col < n; col++) {
      if (solutions.length >= limit) return;
      if (isSafe(placement, row, col)) {
        placement[row] = col;
        backtrack(row + 1);
        placement[row] = -1;
      }
    }
  }

  backtrack(0);
  return solutions;
}

function generateSteps(n: number, maxSteps = 300): BacktrackStep[] {
  const steps: BacktrackStep[] = [];
  const placement: number[] = new Array(n).fill(-1);

  function backtrack(row: number): boolean {
    if (steps.length >= maxSteps) return false;
    if (row === n) return true;
    for (let col = 0; col < n; col++) {
      if (steps.length >= maxSteps) return false;
      if (isSafe(placement, row, col)) {
        placement[row] = col;
        steps.push({ row, col, action: "place", board: [...placement] });
        if (backtrack(row + 1)) return true;
        steps.push({ row, col, action: "remove", board: [...placement] });
        placement[row] = -1;
      } else {
        steps.push({ row, col, action: "conflict", board: [...placement] });
      }
    }
    return false;
  }

  backtrack(0);
  return steps;
}

// ─── Chessboard Component ────────────────────────────────────────────────────

function ChessBoard({
  n,
  placement,
  highlightRow = -1,
  highlightCol = -1,
  conflictCell = null,
  showCoords = true,
  small = false,
}: {
  n: number;
  placement: number[];
  highlightRow?: number;
  highlightCol?: number;
  conflictCell?: { row: number; col: number } | null;
  showCoords?: boolean;
  small?: boolean;
}) {
  const cellSize = small ? 28 : Math.min(54, Math.floor(480 / n));
  const fontSize = small ? "0.9rem" : `${Math.min(1.8, cellSize / 28)}rem`;

  return (
    <div className="flex flex-col items-center">
      {showCoords && (
        <div className="flex" style={{ marginLeft: cellSize + 4 }}>
          {Array.from({ length: n }, (_, c) => (
            <div
              key={c}
              style={{ width: cellSize, fontSize: "0.65rem" }}
              className="text-center text-slate-400 font-medium"
            >
              {String.fromCharCode(65 + c)}
            </div>
          ))}
        </div>
      )}
      <div className="flex">
        {showCoords && (
          <div className="flex flex-col" style={{ width: cellSize / 1.5 }}>
            {Array.from({ length: n }, (_, r) => (
              <div
                key={r}
                style={{ height: cellSize, fontSize: "0.65rem" }}
                className="flex items-center justify-end pr-1 text-slate-400 font-medium"
              >
                {n - r}
              </div>
            ))}
          </div>
        )}
        <div
          className="border-2 border-slate-700 rounded overflow-hidden shadow-xl"
          style={{ display: "grid", gridTemplateColumns: `repeat(${n}, ${cellSize}px)` }}
        >
          {Array.from({ length: n }, (_, r) =>
            Array.from({ length: n }, (_, c) => {
              const isLight = (r + c) % 2 === 0;
              const hasQueen = placement[r] === c;
              const isConflict =
                conflictCell?.row === r && conflictCell?.col === c;
              const isHighlighted = r === highlightRow || c === highlightCol;

              let bg = isLight ? "bg-amber-100" : "bg-amber-800";
              if (hasQueen) bg = isLight ? "bg-yellow-300" : "bg-yellow-500";
              if (isConflict) bg = "bg-red-400";
              if (isHighlighted && !hasQueen && !isConflict)
                bg = isLight ? "bg-indigo-100" : "bg-indigo-700";

              return (
                <div
                  key={`${r}-${c}`}
                  style={{ width: cellSize, height: cellSize, fontSize }}
                  className={`${bg} flex items-center justify-center transition-all duration-150 select-none`}
                >
                  {hasQueen && "♛"}
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Mini Board for All Solutions ────────────────────────────────────────────

function MiniBoard({ n, placement, index }: { n: number; placement: number[]; index: number }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className={`flex flex-col items-center gap-1 p-2 rounded-lg border transition-all duration-200 cursor-default
        ${hovered ? "border-indigo-400 shadow-md bg-indigo-50" : "border-slate-200 bg-white"}`}
    >
      <ChessBoard n={n} placement={placement} showCoords={false} small />
      <span className="text-xs text-slate-500 font-medium">#{index + 1}</span>
    </div>
  );
}

// ─── Stat Card ───────────────────────────────────────────────────────────────

function StatCard({ label, value, icon, sub }: {
  label: string; value: string | number; icon: string; sub?: string;
}) {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm flex flex-col gap-1">
      <div className="flex items-center gap-2 text-slate-500 text-xs font-semibold uppercase tracking-wide">
        <span>{icon}</span>
        <span>{label}</span>
      </div>
      <div className="text-2xl font-bold text-slate-800">{value}</div>
      {sub && <div className="text-xs text-slate-400">{sub}</div>}
    </div>
  );
}

// ─── Algorithm Explanation ───────────────────────────────────────────────────

function AlgorithmPanel() {
  const [open, setOpen] = useState(false);

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-xl">🧠</span>
          <span className="font-semibold text-slate-800">Algorithm Explanation & Complexity</span>
        </div>
        <span className={`text-slate-400 transition-transform duration-200 ${open ? "rotate-180" : ""}`}>▼</span>
      </button>

      {open && (
        <div className="px-6 pb-6 space-y-5 border-t border-slate-100">
          <div className="mt-5 p-4 bg-indigo-50 border-l-4 border-indigo-500 rounded-r-lg">
            <h4 className="font-semibold text-indigo-800 mb-1">Overview</h4>
            <p className="text-sm text-slate-700">
              The N-Queens problem asks: how can N chess queens be placed on an N×N board so that no
              two queens threaten each other? Queens attack along rows, columns, and both diagonals.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-slate-700 mb-2">🔢 Backtracking Steps</h4>
            <ol className="space-y-2 text-sm text-slate-600">
              {[
                "Start at row 0. Try placing a queen in each column (left to right).",
                "Before placing, check: no queen in same column or diagonal.",
                "If safe → place the queen, recurse to the next row.",
                "If no column works → backtrack to the previous row, try the next column.",
                "When all N rows have a queen → solution recorded!",
              ].map((step, i) => (
                <li key={i} className="flex gap-3">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold flex items-center justify-center">
                    {i + 1}
                  </span>
                  <span>{step}</span>
                </li>
              ))}
            </ol>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              {
                title: "⏱ Time Complexity",
                value: "O(N!)",
                desc: "Bounded by permutations explored. Pruning cuts actual work drastically below N! for most N.",
              },
              {
                title: "💾 Space Complexity",
                value: "O(N)",
                desc: "Recursion depth is at most N (one level per row), plus O(N) constraint sets.",
              },
              {
                title: "🔍 Safety Check",
                value: "O(1)",
                desc: "Three hash sets track occupied columns and both diagonals — constant-time lookup.",
              },
              {
                title: "❌ vs Brute Force",
                value: "O(N^N)",
                desc: "Brute force would be impractical even for N=10 (10 billion configs). Backtracking prunes early.",
              },
            ].map((card) => (
              <div key={card.title} className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <div className="font-semibold text-slate-700 text-sm">{card.title}</div>
                <div className="text-xl font-bold text-indigo-600 my-1">{card.value}</div>
                <div className="text-xs text-slate-500">{card.desc}</div>
              </div>
            ))}
          </div>

          <div>
            <h4 className="font-semibold text-slate-700 mb-2">📊 Known Solution Counts (OEIS A000170)</h4>
            <div className="overflow-x-auto">
              <table className="text-sm w-full border-collapse">
                <thead>
                  <tr className="bg-slate-100">
                    <th className="px-3 py-2 text-left font-semibold text-slate-600">N</th>
                    {Object.keys(KNOWN_COUNTS).map((k) => (
                      <th key={k} className={`px-3 py-2 text-center font-semibold ${k === "8" ? "text-indigo-700 bg-indigo-50" : "text-slate-600"}`}>{k}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-t border-slate-200">
                    <td className="px-3 py-2 font-medium text-slate-600">Solutions</td>
                    {Object.entries(KNOWN_COUNTS).map(([k, v]) => (
                      <td key={k} className={`px-3 py-2 text-center ${k === "8" ? "font-bold text-indigo-700 bg-indigo-50" : "text-slate-700"}`}>
                        {v.toLocaleString()}
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Step-by-step Visualiser ─────────────────────────────────────────────────

function StepVisualiser({ n }: { n: number }) {
  const [steps, setSteps] = useState<BacktrackStep[]>([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(200);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    const s = generateSteps(n, 300);
    setSteps(s);
    setCurrentStep(0);
    setPlaying(false);
  }, [n]);

  useEffect(() => {
    if (playing) {
      timerRef.current = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= steps.length - 1) {
            setPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, speed);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [playing, speed, steps.length]);

  const step = steps[currentStep];
  if (!steps.length || !step) return null;

  const displayBoard = [...step.board];
  for (let i = displayBoard.length; i < n; i++) displayBoard.push(-1);

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 space-y-4">
      <div className="flex items-center gap-3">
        <span className="text-xl">🎬</span>
        <h3 className="font-semibold text-slate-800">Step-by-Step Backtracking</h3>
      </div>

      <div className="flex items-center gap-2 flex-wrap">
        <button
          onClick={() => { setPlaying(false); setCurrentStep(0); }}
          className="px-3 py-1.5 text-xs font-medium bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
        >⏮ Reset</button>
        <button
          onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
          disabled={playing}
          className="px-3 py-1.5 text-xs font-medium bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors disabled:opacity-40"
        >◀ Prev</button>
        <button
          onClick={() => setPlaying(!playing)}
          className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
            playing ? "bg-red-100 hover:bg-red-200 text-red-700" : "bg-indigo-600 hover:bg-indigo-700 text-white"
          }`}
        >{playing ? "⏸ Pause" : "▶ Play"}</button>
        <button
          onClick={() => setCurrentStep(Math.min(steps.length - 1, currentStep + 1))}
          disabled={playing}
          className="px-3 py-1.5 text-xs font-medium bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors disabled:opacity-40"
        >Next ▶</button>
        <button
          onClick={() => { setPlaying(false); setCurrentStep(steps.length - 1); }}
          className="px-3 py-1.5 text-xs font-medium bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
        >⏭ End</button>

        <div className="flex items-center gap-2 ml-auto">
          <label className="text-xs text-slate-500">Speed:</label>
          <select
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
            className="text-xs border border-slate-200 rounded px-2 py-1"
          >
            <option value={500}>Slow</option>
            <option value={200}>Normal</option>
            <option value={80}>Fast</option>
            <option value={20}>Turbo</option>
          </select>
        </div>
      </div>

      <div className="flex items-center gap-2 text-xs">
        <div className={`px-2 py-1 rounded font-semibold ${
          step.action === "place" ? "bg-green-100 text-green-700" :
          step.action === "remove" ? "bg-orange-100 text-orange-700" :
          "bg-red-100 text-red-700"
        }`}>
          {step.action === "place" ? "✅ Place" : step.action === "remove" ? "↩ Backtrack" : "❌ Conflict"}
        </div>
        <span className="text-slate-500">
          Row {step.row + 1}, Col {String.fromCharCode(65 + step.col)}
          {step.action === "conflict" && " — unsafe, skipping"}
          {step.action === "place" && " — safe, placing queen"}
          {step.action === "remove" && " — removing, backtracking"}
        </span>
        <span className="ml-auto text-slate-400">{currentStep + 1} / {steps.length}</span>
      </div>

      <div className="w-full bg-slate-100 rounded-full h-1.5">
        <div
          className="bg-indigo-500 h-1.5 rounded-full transition-all"
          style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
        />
      </div>

      <div className="flex justify-center">
        <ChessBoard
          n={n}
          placement={displayBoard}
          highlightRow={step.action !== "conflict" ? step.row : -1}
          conflictCell={step.action === "conflict" ? { row: step.row, col: step.col } : null}
          showCoords
        />
      </div>

      <div className="flex gap-3 text-xs flex-wrap">
        {[
          { color: "bg-yellow-300", label: "Queen placed" },
          { color: "bg-indigo-100", label: "Current row" },
          { color: "bg-red-400", label: "Conflict (skipped)" },
          { color: "bg-amber-100 border border-slate-200", label: "Empty (light)" },
          { color: "bg-amber-800", label: "Empty (dark)" },
        ].map(({ color, label }) => (
          <div key={label} className="flex items-center gap-1">
            <div className={`w-3 h-3 rounded ${color}`} />
            <span className="text-slate-500">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Main App ────────────────────────────────────────────────────────────────

export default function App() {
  const [n, setN] = useState(8);
  const [inputN, setInputN] = useState("8");
  const [stats, setStats] = useState<SolverStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"solution" | "all" | "stepwise">("solution");
  const [selectedSolution, setSelectedSolution] = useState(0);
  const [inputError, setInputError] = useState("");

  const solve = useCallback((size: number) => {
    setLoading(true);
    // Use setTimeout to allow React to render the loading state
    setTimeout(() => {
      const start = performance.now();
      const firstSolution = solveFirst(size);
      const hasSolution = firstSolution !== null;
      const allSolutions = size <= 10 ? solveAll(size) : firstSolution ? [firstSolution] : [];
      const totalCount = KNOWN_COUNTS[size] ?? (size <= 10 ? allSolutions.length : -1);
      const solveTimeMs = performance.now() - start;

      setStats({
        n: size,
        firstSolution,
        allSolutions,
        totalCount,
        hasSolution,
        solveTimeMs,
        countIsExact: size in KNOWN_COUNTS || size <= 10,
      });
      setSelectedSolution(0);
      setLoading(false);
    }, 10);
  }, []);

  useEffect(() => { solve(8); }, [solve]);

  const handleNChange = (raw: string) => {
    setInputN(raw);
    const val = parseInt(raw, 10);
    if (isNaN(val) || raw.trim() === "") {
      setInputError("Please enter a valid integer.");
      return;
    }
    if (val < 1) { setInputError("N must be ≥ 1."); return; }
    if (val > 20) { setInputError("N must be ≤ 20 for practical display."); return; }
    setInputError("");
    setN(val);
  };

  const handleSolve = () => {
    if (inputError || !inputN) return;
    const val = parseInt(inputN, 10);
    if (!isNaN(val) && val >= 1 && val <= 20) {
      setActiveTab("solution");
      solve(val);
    }
  };

  const currentPlacement = stats?.allSolutions[selectedSolution] ?? stats?.firstSolution ?? [];
  const displayPlacement = currentPlacement.length > 0 ? currentPlacement : new Array(n).fill(-1);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
      {/* ── Header ── */}
      <div className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xl shadow-lg shadow-indigo-200">
              ♛
            </div>
            <div>
              <h1 className="text-lg font-bold text-slate-900 leading-tight">N-Queens Solver</h1>
              <p className="text-xs text-slate-500">Codveda Technologies · Level 3 · Task 3</p>
            </div>
          </div>
          <div className="hidden sm:flex items-center gap-2">
            {["Python 3.11", "Backtracking", "Streamlit", "pytest"].map((tag) => (
              <span key={tag} className="px-2.5 py-1 bg-slate-100 border border-slate-200 rounded-full text-xs font-medium text-slate-600">
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-6">

        {/* ── Hero ── */}
        <div className="text-center space-y-3">
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-900">
            Place N Queens on an N×N Board
          </h2>
          <p className="text-slate-500 max-w-2xl mx-auto">
            No two queens may share the same <strong>row</strong>, <strong>column</strong>, or <strong>diagonal</strong>.
            Uses pure backtracking with O(1) constraint checks.
          </p>
        </div>

        {/* ── Controls ── */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div className="flex flex-col sm:flex-row items-start sm:items-end gap-4">
            <div className="flex-1 space-y-1">
              <label className="text-sm font-semibold text-slate-700">Board Size (N)</label>
              <p className="text-xs text-slate-400">Enter a value between 1 and 20</p>
              <div className="flex items-center gap-3">
                <input
                  type="number"
                  value={inputN}
                  min={1}
                  max={20}
                  onChange={(e) => handleNChange(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSolve()}
                  className={`w-28 px-4 py-2.5 text-lg font-semibold border rounded-xl focus:outline-none focus:ring-2 transition-colors ${
                    inputError
                      ? "border-red-300 focus:ring-red-200"
                      : "border-slate-300 focus:ring-indigo-200 focus:border-indigo-400"
                  }`}
                />
                <input
                  type="range"
                  min={1}
                  max={20}
                  value={n}
                  onChange={(e) => { const v = Number(e.target.value); setInputN(String(v)); setN(v); setInputError(""); }}
                  className="flex-1 accent-indigo-600"
                />
                <span className="text-2xl font-bold text-indigo-600 w-8">{n}</span>
              </div>
              {inputError && <p className="text-xs text-red-500 font-medium">{inputError}</p>}
            </div>

            <button
              onClick={handleSolve}
              disabled={!!inputError || loading}
              className="px-8 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 text-white font-semibold rounded-xl shadow-md shadow-indigo-200 transition-all duration-200 flex items-center gap-2 whitespace-nowrap"
            >
              {loading ? (
                <>
                  <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                  </svg>
                  Solving…
                </>
              ) : (
                <>♛ Solve</>
              )}
            </button>
          </div>
        </div>

        {/* ── Edge case banners ── */}
        {stats && !stats.hasSolution && stats.n > 1 && (
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex items-start gap-3">
            <span className="text-xl">⚠️</span>
            <div>
              <p className="font-semibold text-amber-800">No Solution for N={stats.n}</p>
              <p className="text-sm text-amber-700 mt-0.5">
                It is mathematically impossible to place {stats.n} queens on a {stats.n}×{stats.n} board without conflicts.
                This is a known result — try N ≥ 4.
              </p>
            </div>
          </div>
        )}
        {stats?.n === 1 && (
          <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex items-start gap-3">
            <span className="text-xl">♟️</span>
            <div>
              <p className="font-semibold text-green-800">N=1: Trivial Case</p>
              <p className="text-sm text-green-700 mt-0.5">A single queen on a 1×1 board is always safe. One solution exists.</p>
            </div>
          </div>
        )}

        {/* ── Stats ── */}
        {stats && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <StatCard
              icon="📐"
              label="Board Size"
              value={`${stats.n}×${stats.n}`}
            />
            <StatCard
              icon="♛"
              label="Total Solutions"
              value={
                stats.totalCount < 0
                  ? "N/A"
                  : stats.totalCount.toLocaleString()
              }
              sub={!stats.countIsExact && stats.totalCount >= 0 ? "OEIS A000170" : undefined}
            />
            <StatCard
              icon={stats.hasSolution ? "✅" : "❌"}
              label="Status"
              value={stats.hasSolution ? "Solvable" : "No Solution"}
            />
            <StatCard
              icon="⚡"
              label="Solve Time"
              value={
                stats.solveTimeMs < 1
                  ? "< 1 ms"
                  : stats.solveTimeMs < 1000
                  ? `${stats.solveTimeMs.toFixed(1)} ms`
                  : `${(stats.solveTimeMs / 1000).toFixed(2)} s`
              }
            />
          </div>
        )}

        {/* ── Tabs ── */}
        {stats?.hasSolution && (
          <>
            <div className="flex gap-1 bg-slate-100 p-1 rounded-xl w-fit">
              {(
                [
                  { key: "solution", label: "♛ Solution Board", emoji: "" },
                  { key: "all", label: `🗂 All Solutions`, emoji: "" },
                  { key: "stepwise", label: "🎬 Step-by-Step", emoji: "" },
                ] as const
              ).map(({ key, label }) => (
                <button
                  key={key}
                  onClick={() => setActiveTab(key)}
                  className={`px-4 py-2 text-sm font-semibold rounded-lg transition-all ${
                    activeTab === key
                      ? "bg-white text-indigo-700 shadow-sm"
                      : "text-slate-500 hover:text-slate-700"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>

            {/* ── Tab: Solution Board ── */}
            {activeTab === "solution" && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-slate-800">
                      {stats.allSolutions.length > 1
                        ? `Solution ${selectedSolution + 1} of ${stats.allSolutions.length}`
                        : "First Valid Solution"}
                    </h3>
                    {stats.allSolutions.length > 1 && (
                      <div className="flex gap-2">
                        <button
                          onClick={() => setSelectedSolution(Math.max(0, selectedSolution - 1))}
                          disabled={selectedSolution === 0}
                          className="px-2 py-1 text-xs bg-slate-100 hover:bg-slate-200 disabled:opacity-40 rounded-lg transition-colors"
                        >◀</button>
                        <button
                          onClick={() => setSelectedSolution(Math.min(stats.allSolutions.length - 1, selectedSolution + 1))}
                          disabled={selectedSolution === stats.allSolutions.length - 1}
                          className="px-2 py-1 text-xs bg-slate-100 hover:bg-slate-200 disabled:opacity-40 rounded-lg transition-colors"
                        >▶</button>
                      </div>
                    )}
                  </div>
                  <ChessBoard n={stats.n} placement={displayPlacement} showCoords />
                </div>

                <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 space-y-5">
                  <h3 className="font-semibold text-slate-800">♛ Queen Placement</h3>
                  <p className="text-sm text-slate-500">Column of queen in each row (0-indexed):</p>
                  <div className="space-y-1.5">
                    {displayPlacement.map((col, row) => (
                      col >= 0 && (
                        <div key={row} className="flex items-center gap-3">
                          <span className="w-16 text-xs font-medium text-slate-500">Row {row + 1}</span>
                          <div className="flex-1 bg-slate-50 rounded-lg px-3 py-1.5 flex items-center justify-between">
                            <span className="text-sm font-mono text-slate-700">
                              Col {col} ({String.fromCharCode(65 + col)}{stats.n - row})
                            </span>
                            <span className="text-yellow-500">♛</span>
                          </div>
                        </div>
                      )
                    ))}
                  </div>

                  <div className="border-t border-slate-100 pt-4">
                    <p className="text-xs font-semibold text-slate-500 mb-2">Text Representation</p>
                    <pre className="bg-slate-900 text-green-400 text-xs p-3 rounded-lg font-mono leading-5 overflow-x-auto">
                      {displayPlacement.map((col) =>
                        Array.from({ length: stats.n }, (_, c) =>
                          c === col ? "Q" : "."
                        ).join(" ")
                      ).join("\n")}
                    </pre>
                  </div>
                </div>
              </div>
            )}

            {/* ── Tab: All Solutions ── */}
            {activeTab === "all" && (
              <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-slate-800">
                    All {stats.allSolutions.length.toLocaleString()} Solutions
                    {stats.n > 10 && " (showing first solution only)"}
                  </h3>
                  {stats.n > 10 && (
                    <span className="text-xs bg-amber-100 text-amber-700 px-2 py-1 rounded-full font-medium">
                      N&gt;10: Full enumeration skipped for performance
                    </span>
                  )}
                </div>
                {stats.n <= 10 ? (
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
                    {stats.allSolutions.map((placement, i) => (
                      <MiniBoard key={i} n={stats.n} placement={placement} index={i} />
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 space-y-3">
                    <div className="text-5xl">📊</div>
                    <p className="text-slate-600 font-medium">
                      N={stats.n} has {(KNOWN_COUNTS[stats.n] ?? "many").toLocaleString()} known solutions
                    </p>
                    <p className="text-sm text-slate-400">
                      Full enumeration for N&gt;10 is computationally intensive. Use the Solution Board tab to view the first solution.
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* ── Tab: Step-by-step ── */}
            {activeTab === "stepwise" && (
              <StepVisualiser n={stats.n} />
            )}
          </>
        )}

        {/* ── Algorithm Panel ── */}
        <AlgorithmPanel />

        {/* ── Python Code Preview ── */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
          <button
            onClick={() => {}}
            className="w-full px-6 py-4 flex items-center gap-3 bg-slate-900 text-left"
          >
            <span className="text-xl">🐍</span>
            <span className="font-semibold text-white">Python Source — Core Backtracking Algorithm</span>
            <span className="ml-auto text-xs text-slate-400 bg-slate-700 px-2 py-0.5 rounded">solver.py</span>
          </button>
          <pre className="bg-slate-900 text-sm overflow-x-auto p-6 text-slate-300 leading-6">
            <span className="text-slate-500">{`# src/solver.py — excerpt (full file in repo)\n\n`}</span>
            <span className="text-purple-400">def </span>
            <span className="text-yellow-300">_backtrack</span>
            <span className="text-white">{`(board: Board, row: int, placement: list[int]) -> bool:\n`}</span>
            <span className="text-slate-500">{"    # Base case: all N queens placed — solution complete\n"}</span>
            <span className="text-purple-400">{"    if "}</span>
            <span className="text-white">{"row == board.size:\n"}</span>
            <span className="text-purple-400">{"        return "}</span>
            <span className="text-green-400">{"True\n\n"}</span>
            <span className="text-purple-400">{"    for "}</span>
            <span className="text-white">{"col "}</span>
            <span className="text-purple-400">{"in "}</span>
            <span className="text-white">{"range(board.size):\n"}</span>
            <span className="text-purple-400">{"        if "}</span>
            <span className="text-white">{"board.is_safe(row, col):\n"}</span>
            <span className="text-slate-500">{"            # ── Place queen ──────────────────────────────────────\n"}</span>
            <span className="text-white">{"            board.place_queen(row, col)\n"}</span>
            <span className="text-white">{"            placement.append(col)\n\n"}</span>
            <span className="text-slate-500">{"            # ── Recurse to next row ─────────────────────────────\n"}</span>
            <span className="text-purple-400">{"            if "}</span>
            <span className="text-white">{"_backtrack(board, row + 1, placement):\n"}</span>
            <span className="text-purple-400">{"                return "}</span>
            <span className="text-green-400">{"True  "}</span>
            <span className="text-slate-500">{"# Propagate success upward\n\n"}</span>
            <span className="text-slate-500">{"            # ── Backtrack: undo placement ──────────────────────\n"}</span>
            <span className="text-white">{"            board.remove_queen(row, col)\n"}</span>
            <span className="text-white">{"            placement.pop()\n\n"}</span>
            <span className="text-purple-400">{"    return "}</span>
            <span className="text-red-400">{"False  "}</span>
            <span className="text-slate-500">{"# No valid column found → backtrack\n"}</span>
          </pre>
        </div>

        {/* ── Project Files ── */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
          <h3 className="font-semibold text-slate-800 mb-4">📁 Project Structure</h3>
          <div className="font-mono text-sm text-slate-600 space-y-0.5 bg-slate-50 rounded-lg p-4 border border-slate-100">
            {[
              { indent: 0, name: "n-queens/", type: "dir" },
              { indent: 1, name: "app.py", type: "file", desc: "Streamlit UI entry point" },
              { indent: 1, name: "src/", type: "dir" },
              { indent: 2, name: "__init__.py", type: "file" },
              { indent: 2, name: "solver.py", type: "file", desc: "Backtracking algorithm" },
              { indent: 2, name: "board.py", type: "file", desc: "2D board + O(1) constraints" },
              { indent: 2, name: "utils.py", type: "file", desc: "Helpers & display" },
              { indent: 1, name: "tests/", type: "dir" },
              { indent: 2, name: "__init__.py", type: "file" },
              { indent: 2, name: "test_solver.py", type: "file", desc: "~40 pytest tests" },
              { indent: 1, name: "requirements.txt", type: "file" },
              { indent: 1, name: "Dockerfile", type: "file" },
              { indent: 1, name: ".gitignore", type: "file" },
              { indent: 1, name: "README.md", type: "file" },
            ].map(({ indent, name, type, desc }, i) => (
              <div key={i} className="flex items-center gap-2" style={{ paddingLeft: indent * 20 }}>
                <span>{type === "dir" ? "📂" : "📄"}</span>
                <span className={type === "dir" ? "text-indigo-700 font-semibold" : "text-slate-700"}>{name}</span>
                {desc && <span className="text-slate-400 text-xs">— {desc}</span>}
              </div>
            ))}
          </div>
        </div>

        {/* ── Footer ── */}
        <footer className="text-center py-6 text-sm text-slate-400 space-y-1">
          <p>♛ N-Queens Solver · Codveda Technologies Internship · Level 3 · Task 3</p>
          <p>Built with Python 3.11 · Streamlit · Backtracking · pytest</p>
        </footer>

      </div>
    </div>
  );
}
