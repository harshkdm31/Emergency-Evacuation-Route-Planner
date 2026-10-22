"""
Presentation-only styling for the Streamlit interface.

This module contains no application logic. It only provides:
    - A CSS stylesheet injected into the Streamlit page.
    - A helper that applies a consistent dark visual theme to
      Plotly figures (colors, fonts, gridlines, hover labels).
"""

import plotly.graph_objects as go


# ---------------------------------------------------------
# Design tokens
# ---------------------------------------------------------
BG = "#070B14"
SURFACE = "#0E1626"
SURFACE_RAISED = "#121C30"
BORDER = "#1E2A42"
TEXT = "#E2E8F0"
TEXT_MUTED = "#8B9AB4"
ACCENT = "#22D3EE"
ACCENT_2 = "#2DD4BF"
AMBER = "#FBBF24"
RED = "#EF4444"
FONT_FAMILY = "Inter, 'Segoe UI', system-ui, -apple-system, sans-serif"

CHART_COLORWAY = [ACCENT, ACCENT_2, "#818CF8", AMBER, "#F472B6"]


APP_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

:root {{
    --bg: {BG};
    --surface: {SURFACE};
    --surface-raised: {SURFACE_RAISED};
    --border: {BORDER};
    --text: {TEXT};
    --muted: {TEXT_MUTED};
    --accent: {ACCENT};
    --accent-2: {ACCENT_2};
    --amber: {AMBER};
    --red: {RED};
    --radius: 14px;
}}

/* ---------- Base ---------- */
html, body, [class*="css"], .stApp, .stMarkdown, button, input, textarea, select {{
    font-family: {FONT_FAMILY};
}}

.stApp {{
    background:
        radial-gradient(1200px 500px at 85% -10%, rgba(34, 211, 238, 0.07), transparent 60%),
        radial-gradient(900px 400px at -10% 10%, rgba(45, 212, 191, 0.05), transparent 60%),
        var(--bg);
    color: var(--text);
}}

[data-testid="stHeader"] {{
    background: rgba(7, 11, 20, 0.75);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid rgba(30, 42, 66, 0.6);
}}

.block-container {{
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1320px;
}}

/* ---------- Typography ---------- */
h1 {{
    font-weight: 800 !important;
    letter-spacing: -0.025em;
    font-size: 2.15rem !important;
    background: linear-gradient(90deg, #F8FAFC 0%, #BAE6FD 55%, var(--accent) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 0.15rem !important;
}}

h2, h3 {{
    font-weight: 700 !important;
    letter-spacing: -0.01em;
    color: #F1F5F9 !important;
}}

.main h3, [data-testid="stMain"] h3 {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.2rem !important;
    margin-top: 1.4rem;
}}

.main h3::before, [data-testid="stMain"] h3::before {{
    content: "";
    width: 4px;
    height: 1.1em;
    border-radius: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
    box-shadow: 0 0 12px rgba(34, 211, 238, 0.45);
    flex-shrink: 0;
}}

[data-testid="stCaptionContainer"], .stCaption {{
    color: var(--muted) !important;
}}

/* ---------- Command-center badge ---------- */
.cc-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    border: 1px solid rgba(34, 211, 238, 0.3);
    background: rgba(34, 211, 238, 0.08);
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}}

.cc-badge .dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--accent-2);
    box-shadow: 0 0 0 0 rgba(45, 212, 191, 0.6);
    animation: cc-pulse 2.4s ease-out infinite;
}}

@keyframes cc-pulse {{
    0%   {{ box-shadow: 0 0 0 0 rgba(45, 212, 191, 0.55); }}
    70%  {{ box-shadow: 0 0 0 8px rgba(45, 212, 191, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(45, 212, 191, 0); }}
}}

@media (prefers-reduced-motion: reduce) {{
    .cc-badge .dot {{ animation: none; }}
}}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0B1220 0%, #080D18 100%);
    border-right: 1px solid var(--border);
}}

[data-testid="stSidebar"] h2 {{
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--accent) !important;
    font-weight: 700 !important;
}}

[data-testid="stSidebar"] h3 {{
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: var(--amber) !important;
    font-weight: 700 !important;
}}

[data-testid="stSidebar"] label p {{
    font-size: 0.82rem;
    font-weight: 500;
    color: #CBD5E1;
}}

[data-testid="stSidebar"] hr {{
    border-color: var(--border) !important;
    margin: 1.2rem 0;
}}

/* ---------- Inputs ---------- */
[data-baseweb="select"] > div {{
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}}

[data-baseweb="select"] > div:hover {{
    border-color: rgba(34, 211, 238, 0.45) !important;
}}

[data-baseweb="select"] > div:focus-within {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.18) !important;
}}

/* Multiselect chips: road closures */
[data-baseweb="tag"] {{
    background-color: rgba(239, 68, 68, 0.14) !important;
    border: 1px solid rgba(239, 68, 68, 0.45) !important;
    color: #FCA5A5 !important;
    border-radius: 8px !important;
}}

[data-baseweb="tag"] span {{
    color: #FECACA !important;
}}

/* ---------- Buttons ---------- */
.stButton > button {{
    min-height: 2.75rem;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--surface-raised);
    color: var(--text);
    font-weight: 600;
    letter-spacing: 0.01em;
    transition: border-color 0.15s ease, background 0.15s ease,
                transform 0.15s ease, box-shadow 0.15s ease;
}}

.stButton > button:hover:not(:disabled) {{
    border-color: rgba(34, 211, 238, 0.6);
    background: #16223A;
    color: #FFFFFF;
    transform: translateY(-1px);
    box-shadow: 0 6px 18px -8px rgba(34, 211, 238, 0.45);
}}

.stButton > button:focus-visible {{
    outline: none;
    box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.35) !important;
}}

.stButton > button:disabled {{
    opacity: 0.4;
}}

.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {{
    background: linear-gradient(135deg, #06B6D4 0%, #14B8A6 100%);
    border: 1px solid rgba(34, 211, 238, 0.7);
    color: #04121A;
    font-weight: 700;
    padding-left: 1.6rem;
    padding-right: 1.6rem;
}}

.stButton > button[kind="primary"]:hover:not(:disabled),
.stButton > button[data-testid="stBaseButton-primary"]:hover:not(:disabled) {{
    background: linear-gradient(135deg, #22D3EE 0%, #2DD4BF 100%);
    color: #04121A;
    box-shadow: 0 8px 24px -8px rgba(34, 211, 238, 0.6);
}}

/* ---------- Metrics ---------- */
[data-testid="stMetric"] {{
    background: linear-gradient(180deg, var(--surface-raised) 0%, var(--surface) 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.15rem;
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.03) inset,
                0 10px 30px -18px rgba(0, 0, 0, 0.8);
    position: relative;
    overflow: hidden;
}}

[data-testid="stMetric"]::before {{
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent 80%);
    opacity: 0.8;
}}

[data-testid="stMetricLabel"] p {{
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted) !important;
    font-weight: 600;
}}

[data-testid="stMetricValue"] {{
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 1.55rem !important;
    font-weight: 600;
    color: #F8FAFC;
    font-variant-numeric: tabular-nums;
}}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] {{
    border-radius: 12px;
}}

[data-testid="stAlert"] > div {{
    border-radius: 12px;
    border: 1px solid rgba(148, 163, 184, 0.14);
    backdrop-filter: blur(4px);
}}

/* ---------- Expander ---------- */
[data-testid="stExpander"] {{
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--surface);
    overflow: hidden;
}}

[data-testid="stExpander"] summary {{
    font-weight: 600;
    padding-top: 0.85rem;
    padding-bottom: 0.85rem;
}}

[data-testid="stExpander"] summary:hover {{
    color: var(--accent);
}}

/* ---------- Charts & tables ---------- */
[data-testid="stPlotlyChart"] {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.5rem;
    box-shadow: 0 18px 40px -28px rgba(0, 0, 0, 0.9);
}}

[data-testid="stDataFrame"] {{
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
}}

/* ---------- Slider ---------- */
[data-testid="stSlider"] [role="slider"] {{
    box-shadow: 0 0 0 4px rgba(34, 211, 238, 0.18);
}}

/* ---------- Divider ---------- */
hr {{
    border-color: var(--border) !important;
}}

/* ---------- Responsive ---------- */
@media (max-width: 768px) {{
    .block-container {{
        padding-top: 1.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }}
    h1 {{
        font-size: 1.6rem !important;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 1.25rem !important;
    }}
}}
</style>
"""


HEADER_BADGE_HTML = (
    '<div class="cc-badge"><span class="dot"></span>'
    "Emergency Response Command Center</div>"
)


def style_figure(fig: go.Figure) -> go.Figure:
    """
    Apply the dark command-center visual theme to a Plotly figure.

    Only visual layout properties are changed. Traces, data,
    titles, and axis meanings are left untouched.
    """
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, color=TEXT, size=13),
        title_font=dict(family=FONT_FAMILY, color="#F8FAFC", size=16),
        colorway=CHART_COLORWAY,
        hoverlabel=dict(
            bgcolor=SURFACE_RAISED,
            bordercolor=ACCENT,
            font=dict(family=FONT_FAMILY, color=TEXT, size=12),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_MUTED, size=12),
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(148, 163, 184, 0.08)",
        linecolor=BORDER,
        zerolinecolor=BORDER,
        tickfont=dict(color=TEXT_MUTED),
        title_font=dict(color=TEXT_MUTED),
    )
    fig.update_yaxes(
        gridcolor="rgba(148, 163, 184, 0.08)",
        linecolor=BORDER,
        zerolinecolor=BORDER,
        tickfont=dict(color=TEXT_MUTED),
        title_font=dict(color=TEXT_MUTED),
    )
    return fig
