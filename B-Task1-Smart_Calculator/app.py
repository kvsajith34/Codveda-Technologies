"""
SmartCalc Pro - Advanced Web Calculator
Internship Project | Level 1 - Task 1 | Codveda Technology
"""

import math
import streamlit as st

from calculator.basic_ops import add, subtract, multiply, divide
from calculator.scientific_ops import (
    square_root, power, percentage, log_base,
    natural_log, sine, cosine, tangent, factorial,
)
from calculator.unit_converter import convert_unit, CONVERSIONS

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartCalc Pro",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
    }

    /* App background */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }

    /* Title area */
    .app-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
    }
    .app-title {
        font-family: 'Space Mono', monospace;
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d2ff, #7b2ff7, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin: 0;
    }
    .app-subtitle {
        color: #6b7280;
        font-size: 0.85rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Result box */
    .result-box {
        background: linear-gradient(135deg, #1e1b4b, #1e293b);
        border: 1px solid #312e81;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        font-family: 'Space Mono', monospace;
        font-size: 1.8rem;
        color: #a5f3fc;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.15);
    }
    .result-label {
        font-size: 0.75rem;
        color: #6366f1;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    /* History card */
    .history-card {
        background: rgba(30, 27, 75, 0.6);
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        margin: 0.4rem 0;
        font-family: 'Space Mono', monospace;
        font-size: 0.78rem;
    }
    .history-expr {
        color: #e2e8f0;
        font-weight: 700;
    }
    .history-result {
        color: #34d399;
        font-size: 0.9rem;
    }
    .history-time {
        color: #4b5563;
        font-size: 0.68rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(15, 15, 26, 0.8);
        border-radius: 12px;
        padding: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.4rem 1rem;
        font-weight: 600;
        font-size: 0.9rem;
        color: #6b7280;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Sora', sans-serif;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #4338ca, #6d28d9);
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
    }

    /* Input fields */
    .stNumberInput input, .stTextInput input {
        background: #1e293b !important;
        border: 1px solid #312e81 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
        font-family: 'Space Mono', monospace !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #1e293b !important;
        border: 1px solid #312e81 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }

    /* Divider */
    hr { border-color: #1e293b; }

    /* Shortcut badge */
    .shortcut-badge {
        display: inline-block;
        background: #1e293b;
        border: 1px solid #374151;
        border-radius: 5px;
        padding: 2px 8px;
        font-family: 'Space Mono', monospace;
        font-size: 0.75rem;
        color: #9ca3af;
        margin: 2px;
    }

    /* Section header */
    .section-header {
        color: #8b5cf6;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 1rem 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None


def add_history(expression: str, result: float | int | str):
    """Prepend entry to history (newest first, max 50)."""
    import datetime
    st.session_state.history.insert(0, {
        "expr": expression,
        "result": result,
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
    })
    st.session_state.history = st.session_state.history[:50]
    st.session_state.last_result = result


def fmt(value) -> str:
    """Format numbers cleanly: strip trailing zeros."""
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        if value == int(value) and abs(value) < 1e15:
            return f"{int(value):,}"
        return f"{value:,.10g}"
    return str(value)


def show_result(expression: str, result):
    """Render result box and save to history."""
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Result</div>
        {expression} = <span style="color:#f0abfc">{fmt(result)}</span>
    </div>
    """, unsafe_allow_html=True)
    add_history(expression, result)


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1 class="app-title">🧮 SmartCalc Pro</h1>
    <p class="app-subtitle">Basic · Scientific · Unit Converter · Expression Mode</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────
# LAYOUT: Main (left) + History (right)
# ─────────────────────────────────────────────
main_col, hist_col = st.columns([3, 1], gap="medium")

# ══════════════════════════════════════════════
# MAIN PANEL
# ══════════════════════════════════════════════
with main_col:
    tab_basic, tab_sci, tab_unit, tab_expr = st.tabs([
        "🔢  Basic",
        "🔬  Scientific",
        "📐  Unit Converter",
        "⌨️  Expression Mode",
    ])

    # ──────────────────────────────────────────
    # TAB 1 — BASIC CALCULATOR
    # ──────────────────────────────────────────
    with tab_basic:
        st.markdown('<p class="section-header">Arithmetic Operations</p>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            num1 = st.number_input("Number 1", value=0.0, format="%.6f", key="b_n1")
        with c2:
            num2 = st.number_input("Number 2", value=0.0, format="%.6f", key="b_n2")

        operation = st.selectbox(
            "Operation",
            ["➕  Addition", "➖  Subtraction", "✖️  Multiplication", "➗  Division"],
            key="b_op",
        )

        if st.button("Calculate  →", key="b_calc"):
            try:
                op_key = operation.split()[1]
                op_dispatch = {
                    "Addition":       (add(num1, num2),      f"{fmt(num1)} + {fmt(num2)}"),
                    "Subtraction":    (subtract(num1, num2), f"{fmt(num1)} − {fmt(num2)}"),
                    "Multiplication": (multiply(num1, num2), f"{fmt(num1)} × {fmt(num2)}"),
                    "Division":       (divide(num1, num2),   f"{fmt(num1)} ÷ {fmt(num2)}"),
                }
                result, expr = op_dispatch[op_key]
                show_result(expr, result)
            except ZeroDivisionError as e:
                st.error(f"⚠️ {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    # ──────────────────────────────────────────
    # TAB 2 — SCIENTIFIC CALCULATOR
    # ──────────────────────────────────────────
    with tab_sci:
        st.markdown('<p class="section-header">Scientific Functions</p>', unsafe_allow_html=True)

        sci_op = st.selectbox(
            "Function",
            [
                "√  Square Root",
                "xⁿ  Power",
                "%  Percentage of Total",
                "log  Logarithm",
                "ln  Natural Log",
                "sin  Sine (°)",
                "cos  Cosine (°)",
                "tan  Tangent (°)",
                "n!  Factorial",
            ],
            key="sci_op",
        )

        # Determine which inputs are required
        two_inputs = sci_op in ["xⁿ  Power", "%  Percentage of Total", "log  Logarithm"]

        sa, sb = st.columns(2)
        with sa:
            label_map = {
                "xⁿ  Power": "Base",
                "%  Percentage of Total": "Part",
                "log  Logarithm": "Number",
            }
            sci_n1 = st.number_input(
                label_map.get(sci_op, "Number"),
                value=0.0, format="%.6f", key="sci_n1"
            )

        with sb:
            if two_inputs:
                label2_map = {
                    "xⁿ  Power": "Exponent",
                    "%  Percentage of Total": "Total / Base",
                    "log  Logarithm": "Log Base (e.g. 10)",
                }
                sci_n2 = st.number_input(
                    label2_map[sci_op],
                    value=2.0, format="%.6f", key="sci_n2"
                )
            else:
                sci_n2 = None
                st.empty()

        if st.button("Calculate  →", key="sci_calc"):
            try:
                dispatch = {
                    "√  Square Root":          (square_root(sci_n1),                     f"√({fmt(sci_n1)})"),
                    "xⁿ  Power":               (power(sci_n1, sci_n2),                   f"{fmt(sci_n1)}^{fmt(sci_n2)}"),
                    "%  Percentage of Total":  (percentage(sci_n1, sci_n2),               f"{fmt(sci_n1)} % of {fmt(sci_n2)}"),
                    "log  Logarithm":          (log_base(sci_n1, sci_n2),                 f"log_{fmt(sci_n2)}({fmt(sci_n1)})"),
                    "ln  Natural Log":         (natural_log(sci_n1),                      f"ln({fmt(sci_n1)})"),
                    "sin  Sine (°)":           (sine(sci_n1),                             f"sin({fmt(sci_n1)}°)"),
                    "cos  Cosine (°)":         (cosine(sci_n1),                           f"cos({fmt(sci_n1)}°)"),
                    "tan  Tangent (°)":        (tangent(sci_n1),                          f"tan({fmt(sci_n1)}°)"),
                    "n!  Factorial":           (factorial(sci_n1),                        f"{int(sci_n1)}!"),
                }
                result, expr = dispatch[sci_op]
                show_result(expr, result)
            except (ValueError, ZeroDivisionError, OverflowError) as e:
                st.error(f"⚠️ {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    # ──────────────────────────────────────────
    # TAB 3 — UNIT CONVERTER
    # ──────────────────────────────────────────
    with tab_unit:
        st.markdown('<p class="section-header">Unit Conversion</p>', unsafe_allow_html=True)

        category = st.selectbox("Category", list(CONVERSIONS.keys()), key="u_cat")
        units = CONVERSIONS[category]["units"]

        ua, ub, uc = st.columns([2, 1, 1])
        with ua:
            u_val = st.number_input("Value", value=1.0, format="%.6f", key="u_val")
        with ub:
            from_u = st.selectbox("From", units, key="u_from")
        with uc:
            default_to = 1 if len(units) > 1 else 0
            to_u = st.selectbox("To", units, index=default_to, key="u_to")

        if st.button("Convert  →", key="u_conv"):
            try:
                if from_u == to_u:
                    st.warning("⚠️ Same unit selected — result equals input.")
                    show_result(f"{fmt(u_val)} {from_u}", u_val)
                else:
                    result = convert_unit(u_val, from_u, to_u, category)
                    show_result(f"{fmt(u_val)} {from_u}", f"{fmt(result)} {to_u}")
            except (ValueError, ZeroDivisionError) as e:
                st.error(f"⚠️ {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    # ──────────────────────────────────────────
    # TAB 4 — EXPRESSION / KEYBOARD MODE
    # ──────────────────────────────────────────
    with tab_expr:
        st.markdown('<p class="section-header">⌨️ Type Expressions Directly</p>', unsafe_allow_html=True)

        # Keyboard shortcut legend
        st.markdown("""
        <div style="margin-bottom:1rem; line-height:2.2;">
            <span class="shortcut-badge">+ add</span>
            <span class="shortcut-badge">- subtract</span>
            <span class="shortcut-badge">* multiply</span>
            <span class="shortcut-badge">/ divide</span>
            <span class="shortcut-badge">** power</span>
            <span class="shortcut-badge">% modulo</span>
            <span class="shortcut-badge">sqrt(n)</span>
            <span class="shortcut-badge">log(n)</span>
            <span class="shortcut-badge">ln(n)</span>
            <span class="shortcut-badge">sin/cos/tan(n)</span>
            <span class="shortcut-badge">pi</span>
            <span class="shortcut-badge">e</span>
            <span class="shortcut-badge">abs(n)</span>
            <span class="shortcut-badge">factorial(n)</span>
        </div>
        """, unsafe_allow_html=True)

        expr_input = st.text_input(
            "Expression",
            placeholder="e.g.  5 + 3 * 2    |    sqrt(144)    |    2**8    |    sin(45) + cos(30)",
            key="expr_in",
        )

        # Safe namespace — no builtins exposed
        _safe_ns = {
            "__builtins__": {},
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "log2": math.log2,
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "asin": lambda x: math.degrees(math.asin(x)),
            "acos": lambda x: math.degrees(math.acos(x)),
            "atan": lambda x: math.degrees(math.atan(x)),
            "abs": abs,
            "round": round,
            "pow": pow,
            "factorial": math.factorial,
            "pi": math.pi,
            "e": math.e,
        }

        if st.button("Evaluate  →", key="expr_eval"):
            if not expr_input.strip():
                st.warning("Please enter an expression.")
            else:
                try:
                    result = eval(expr_input.strip(), _safe_ns)  # noqa: S307
                    show_result(expr_input.strip(), result)
                except ZeroDivisionError:
                    st.error("⚠️ Division by zero is not allowed.")
                except SyntaxError:
                    st.error("⚠️ Invalid syntax. Check your expression and try again.")
                except Exception as e:
                    st.error(f"⚠️ Could not evaluate: {e}")

# ══════════════════════════════════════════════
# HISTORY PANEL
# ══════════════════════════════════════════════
with hist_col:
    st.markdown('<p class="section-header">📜 History</p>', unsafe_allow_html=True)

    if st.session_state.history:
        if st.button("🗑️ Clear", key="clr_hist"):
            st.session_state.history = []
            st.rerun()

        for entry in st.session_state.history:
            st.markdown(f"""
            <div class="history-card">
                <div class="history-time">🕐 {entry['time']}</div>
                <div class="history-expr">{entry['expr']}</div>
                <div class="history-result">= {fmt(entry['result'])}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:2rem 0.5rem; color:#374151; font-size:0.85rem;">
            <div style="font-size:2rem;">🧮</div>
            <div>No history yet.<br>Start calculating!</div>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center; color:#374151; font-size:0.75rem; padding:0.5rem 0;">
    SmartCalc Pro · Built with Streamlit · Codveda Technology Internship · Level 1 Task 1
</div>
""", unsafe_allow_html=True)
