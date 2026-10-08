"""StockSense NSE: six NSE stocks, 2015 to 2018.  Labmentix Project 5 | Author: Vipsa
Run:  streamlit run app.py     (needs stocks_clean.csv and .streamlit/config.toml next to it)
"""
import re
import sqlite3
import time

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="StockSense NSE", page_icon="📈", layout="wide")

# ---------- palette ----------
INK, PANEL, LINE = "#0B1220", "#111B2E", "rgba(148,163,184,.18)"
TEAL, GOLD, GREEN, RED, MUTED, TEXT = "#2DD4BF", "#FBBF24", "#22C55E", "#F43F5E", "#94A3B8", "#E6EDF7"
FONT = "Source Sans Pro, Segoe UI, sans-serif"
STOCK_COLORS = {"Bajaj Auto": "#2DD4BF", "Eicher Motors": "#60A5FA", "Hero Motocorp": "#FBBF24",
                "Infosys": "#A78BFA", "TCS": "#F472B6", "TVS Motors": "#94A3B8"}
BONUS = {"TCS": "2018-05-31", "Infosys": "2015-06-15"}  # 1:1 bonus-issue ex-dates (public announcements)

st.markdown(f"""
<style>
.stApp {{ background: radial-gradient(1200px 500px at 85% -10%, rgba(45,212,191,.10), transparent 60%), {INK}; }}
.block-container {{ padding-top: 3.6rem; padding-bottom: 2rem; max-width: 1500px; }}
header[data-testid="stHeader"] {{ background: transparent; }}
section[data-testid="stSidebar"] {{ border-right: 1px solid {LINE}; }}
.topbar {{ display:flex; align-items:center; gap:12px; margin-bottom:14px; }}
.topbar svg {{ flex-shrink:0; display:block; }}
.wordmark {{ font-size:1.7rem; font-weight:800; letter-spacing:-.4px; line-height:1; }}
.wordmark b {{ color:{TEAL}; }}
.hero {{ display:grid; grid-template-columns: 1.25fr 1fr; gap:22px; align-items:center; padding:24px 28px; margin-bottom:14px;
         border:1px solid rgba(45,212,191,.35); border-radius:16px;
         background: linear-gradient(135deg, rgba(45,212,191,.14) 0%, rgba(17,27,46,.95) 55%); }}
.hero-tag {{ font-size:.75rem; letter-spacing:.14em; font-weight:800; color:{GOLD}; text-transform:uppercase; }}
.hero-title {{ font-size:clamp(1.8rem,3vw,2.7rem); font-weight:800; line-height:1.1; margin:6px 0 8px 0; }}
.hero-sub {{ color:{MUTED}; font-size:1rem; }}
.pairs {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.pair {{ background:rgba(11,18,32,.65); border:1px solid {LINE}; border-radius:12px; padding:12px 14px; text-align:center; }}
.pair-name {{ font-weight:800; letter-spacing:.06em; font-size:.8rem; color:{MUTED}; }}
.pair-old {{ color:{RED}; font-size:1.05rem; font-weight:700; text-decoration:line-through; text-decoration-thickness:2px; }}
.pair-arrow {{ color:{MUTED}; font-size:.9rem; line-height:1; }}
.pair-new {{ color:{GREEN}; font-size:1.9rem; font-weight:800; line-height:1.15; }}
.kpis {{ display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:12px; margin-bottom:18px; }}
@media (max-width:1150px) {{ .kpis {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .hero {{ grid-template-columns:1fr; }} }}
.kpi {{ background:{PANEL}; border:1px solid {LINE}; border-top:3px solid var(--accent,{TEAL}); border-radius:12px; padding:12px 14px; }}
.kpi-l {{ font-size:.72rem; letter-spacing:.08em; text-transform:uppercase; color:{MUTED}; font-weight:700; white-space:nowrap; }}
.kpi-v {{ font-size:clamp(1.4rem,2vw,1.9rem); font-weight:800; line-height:1.3; white-space:nowrap; }}
.kpi-s {{ font-size:.85rem; color:{MUTED}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.up {{ color:{GREEN}; }} .down {{ color:{RED}; }}
.panel {{ background:{PANEL}; border:1px solid {LINE}; border-radius:12px; padding:14px 16px; }}
.panel-t {{ font-weight:800; margin-bottom:8px; }}
.sigrow {{ display:grid; grid-template-columns:1.3fr 1fr 1fr; align-items:center; gap:8px; padding:7px 0; border-top:1px solid {LINE}; font-size:.95rem; }}
.sighead {{ color:{MUTED}; font-size:.72rem; letter-spacing:.08em; text-transform:uppercase; font-weight:700; border-top:none; }}
.pill {{ display:inline-block; padding:2px 12px; border-radius:999px; font-weight:800; font-size:.8rem; }}
.pill.Buy {{ background:rgba(34,197,94,.18); color:#4ADE80; }} .pill.Sell {{ background:rgba(244,63,94,.18); color:#FB7185; }}
.fixed {{ color:{GOLD}; font-size:.72rem; font-weight:800; margin-left:6px; }}
.banner {{ border:1px solid rgba(251,191,36,.45); border-radius:12px; padding:12px 18px; background:rgba(251,191,36,.07); margin:6px 0 12px 0; font-size:1.05rem; }}
.strow {{ display:grid; grid-template-columns:1.3fr 1fr 1fr 1fr .7fr .8fr; align-items:center; gap:8px; padding:7px 0; border-top:1px solid {LINE}; font-size:.95rem; }}
.chips {{ display:flex; gap:10px; flex-wrap:wrap; margin:4px 0 8px 0; }}
.chip {{ background:{PANEL}; border:1px solid {LINE}; border-radius:999px; padding:5px 14px; font-size:.9rem; }}
div[data-baseweb="tab-list"] {{ gap:10px; margin-bottom:10px; }}
button[data-baseweb="tab"] {{ background:{PANEL}; border:1px solid {LINE}; border-radius:999px; padding:8px 22px; height:auto; }}
button[data-baseweb="tab"][aria-selected="true"] {{ background:linear-gradient(135deg,{TEAL},#0EA5E9); border-color:transparent; }}
button[data-baseweb="tab"][aria-selected="true"] p {{ color:#06121F !important; font-weight:800; }}
button[data-baseweb="tab"] p {{ font-weight:700; font-size:1rem; }}
div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] {{ display:none; }}
.foot {{ margin-top:26px; padding-top:10px; border-top:1px solid {LINE}; font-size:.78rem; color:{MUTED}; }}
</style>
""", unsafe_allow_html=True)

LOGO = f"""<svg width="46" height="46" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="StockSense logo">
  <rect x="1" y="1" width="50" height="50" rx="12" fill="#12305A" stroke="{TEAL}" stroke-width="1.5"/>
  <line x1="15" y1="17" x2="15" y2="39" stroke="#F87171" stroke-width="2.4"/><rect x="11.5" y="23" width="7" height="11" rx="1" fill="#F87171"/>
  <line x1="26" y1="13" x2="26" y2="38" stroke="#34D399" stroke-width="2.4"/><rect x="22.5" y="19" width="7" height="13" rx="1" fill="#34D399"/>
  <line x1="37" y1="9" x2="37" y2="33" stroke="#34D399" stroke-width="2.4"/><rect x="33.5" y="13" width="7" height="14" rx="1" fill="#34D399"/>
  <polyline points="9,43 21,36 31,37 43,19" fill="none" stroke="{GOLD}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


# ---------- helpers ----------
def pct(x):
    return f"{x:+.1f}%"


def rs(x):
    return f"Rs. {x:,.2f}"


def pill(sig):
    return f'<span class="pill {sig}">{sig}</span>'


def color_signal(v):
    if v == "Buy":
        return "background-color: rgba(34,197,94,.20); color: #4ADE80; font-weight:700"
    if v == "Sell":
        return "background-color: rgba(244,63,94,.20); color: #FB7185; font-weight:700"
    return ""


def style_signals(frame, cols):
    sty = frame.style
    return (getattr(sty, "map", None) or sty.applymap)(color_signal, subset=list(cols))


def style_fig(fig, title, ytitle, height=460):
    """One consistent dark look for every chart."""
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text=title, x=0, xanchor="left", font=dict(size=17, color=TEXT)),
        height=height, font=dict(family=FONT, size=13, color="#CBD5E1"), hovermode="x unified",
        hoverlabel=dict(bgcolor=PANEL, bordercolor=TEAL, font=dict(color=TEXT)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title_text=""),
        margin=dict(l=10, r=10, t=85, b=10),
        xaxis=dict(title="", showgrid=False, linecolor=LINE),
        yaxis=dict(title=ytitle, gridcolor="rgba(148,163,184,0.14)", zeroline=False))
    return fig


def add_bonus_lines(fig, shown, start, end):
    """Dashed, labelled vertical line on each bonus-issue date inside the visible range."""
    for s in shown:
        if s in BONUS and start <= pd.Timestamp(BONUS[s]) <= end:
            d = pd.Timestamp(BONUS[s])
            fig.add_shape(type="line", x0=d, x1=d, y0=0, y1=1, yref="paper", line=dict(dash="dash", color=GOLD, width=1.4))
            fig.add_annotation(x=d, y=0.98, yref="paper", text=f"{s} bonus issue, {d:%d %b %Y}", textangle=-90,
                               showarrow=False, xanchor="right", yanchor="top", font=dict(size=11, color=GOLD))


# ---------- data ----------
@st.cache_data
def load_data():
    return pd.read_csv("stocks_clean.csv", parse_dates=["date"])


try:
    df = load_data()
except FileNotFoundError:
    st.error("stocks_clean.csv was not found. Put it in the same folder as app.py and rerun.")
    st.stop()

ALL_STOCKS = sorted(df.stock.unique())
D_MIN, D_MAX = df.date.min().date(), df.date.max().date()


def latest_events(frame, col="signal"):
    rows = []
    for s, g in frame.sort_values("date").groupby("stock"):
        ev = g[g[col] != "Hold"]
        rows.append({"Stock": s, "Buys": int((ev[col] == "Buy").sum()), "Sells": int((ev[col] == "Sell").sum()),
                     "Latest signal": ev.iloc[-1][col] if len(ev) else "None",
                     "Signal date": ev.iloc[-1]["date"].strftime("%Y-%m-%d") if len(ev) else "-"})
    return pd.DataFrame(rows)


@st.cache_data
def raw_signal_table(frame):
    """Same 20/50-day rule on the RAW close price (what the course deck used)."""
    t = frame.sort_values(["stock", "date"]).copy()
    g = t.groupby("stock")["close_price"]
    t["r20"], t["r50"] = g.transform(lambda s: s.rolling(20).mean()), g.transform(lambda s: s.rolling(50).mean())
    p20, p50 = t.groupby("stock")["r20"].shift(), t.groupby("stock")["r50"].shift()
    ok = t[["r20", "r50"]].notna().all(axis=1) & p20.notna() & p50.notna()
    t["raw_signal"] = "Hold"
    t.loc[ok & (t.r20 > t.r50) & (p20 <= p50), "raw_signal"] = "Buy"
    t.loc[ok & (t.r20 < t.r50) & (p20 >= p50), "raw_signal"] = "Sell"
    return latest_events(t, "raw_signal")


@st.cache_data
def run_strategy(frame, cost):
    """Buy at the close on each Buy signal, sell at the close on each Sell signal, stay in cash in between.
    `cost` is the fraction lost on every buy and every sell (0.005 = 0.5%). Bonus-adjusted prices."""
    out = {}
    for s, g in frame.sort_values(["stock", "date"]).groupby("stock"):
        g = g.reset_index(drop=True)
        price, sig = g["adj_close"].to_numpy(), g["signal"].to_numpy()
        pos = pd.Series(np.where(sig == "Buy", 1.0, np.where(sig == "Sell", 0.0, np.nan))).ffill().fillna(0.0).to_numpy()
        daily = np.r_[0.0, price[1:] / price[:-1] - 1]
        held = np.r_[0.0, pos[:-1]]                       # position carried into each day
        switched = np.abs(pos - held)                     # 1 on a buy or sell day
        strategy = 100 * np.cumprod(1 + held * daily - switched * cost)
        trades, entry = [], None
        for k in range(len(g)):
            if sig[k] == "Buy" and entry is None:
                entry = price[k]
            elif sig[k] == "Sell" and entry is not None:
                trades.append(price[k] / entry - 1)
                entry = None
        if entry is not None:                             # still holding at the end: count it at the last price
            trades.append(price[-1] / entry - 1)
        out[s] = {"dates": g["date"], "strategy": strategy, "hold": 100 * price / price[0], "trades": trades}
    return out


@st.cache_data
def full_period_summary(frame):
    rows = []
    for s, g in frame.sort_values("date").groupby("stock"):
        a, b = g.iloc[0], g.iloc[-1]
        rows.append({"Stock": s, "Raw %": 100 * (b.close_price / a.close_price - 1),
                     "Adj %": 100 * (b.adj_close / a.adj_close - 1), "Worst day %": (g["close_price"].pct_change() * 100).min()})
    return pd.DataFrame(rows).sort_values("Adj %", ascending=False).reset_index(drop=True)


@st.cache_resource
def get_db():
    con = sqlite3.connect(":memory:", check_same_thread=False)
    out = load_data().copy()
    out["date"] = out["date"].dt.strftime("%Y-%m-%d")
    out.to_sql("stocks", con, index=False)
    con.execute("PRAGMA query_only = ON")  # read-only
    return con


summ, adj_sig, raw_sig = full_period_summary(df), latest_events(df), raw_signal_table(df)

# ---------- sidebar: filters only ----------
with st.sidebar:
    st.markdown("### Filters")
    picked = st.multiselect("Stocks", ALL_STOCKS, default=ALL_STOCKS)
    rng = st.date_input("Date range", value=(D_MIN, D_MAX), min_value=D_MIN, max_value=D_MAX,
                        help="Applies to the Price Trends and Signals tabs.")
    if isinstance(rng, (tuple, list)) and len(rng) == 2:
        start, end = pd.Timestamp(rng[0]), pd.Timestamp(rng[1])
    else:
        start, end = pd.Timestamp(D_MIN), pd.Timestamp(D_MAX)

fdf = df[df.stock.isin(picked) & (df.date >= start) & (df.date <= end)]

# ---------- top bar ----------
left, right = st.columns([6, 1])
left.markdown(f'<div class="topbar">{LOGO}<div class="wordmark">Stock<b>Sense</b> NSE</div></div>', unsafe_allow_html=True)
with right.popover("ⓘ Terms explained"):
    st.markdown(
        "**NSE:** National Stock Exchange of India, where these stocks trade.\n\n"
        "**Close price:** a share's price when the market closes for the day.\n\n"
        "**Bonus issue (1:1):** shareholders get one free share per share held, so each share's price halves "
        "but the value of what you own stays the same.\n\n"
        "**Adjusted price:** earlier prices divided by 2 so history sits on one scale.\n\n"
        "**Moving average:** the average close of the last 20 (or 50) days.\n\n"
        "**Buy / Sell signal:** the 20-day average crosses above / below the 50-day average.\n\n"
        "**Rebased to 100:** every stock starts at 100 so different price levels compare fairly.")
if st.get_option("theme.backgroundColor") is None:
    st.warning("Theme file missing: copy .streamlit/config.toml next to app.py and restart the app for the dark theme.")

# ---------- computed headline numbers (full period) ----------
t, i = summ[summ.Stock == "TCS"].iloc[0], summ[summ.Stock == "Infosys"].iloc[0]
crash = round(abs(summ[summ["Worst day %"] < -30]["Worst day %"]).mean())
best, worst = summ.iloc[0], summ.iloc[-1]
avg_adj, avg_raw = summ["Adj %"].mean(), summ["Raw %"].mean()
top_buys = adj_sig[adj_sig.Buys == adj_sig.Buys.max()]["Stock"].tolist()
n_buy, n_sell = int((adj_sig["Latest signal"] == "Buy").sum()), int((adj_sig["Latest signal"] == "Sell").sum())
trap = summ[summ["Worst day %"] < -30]["Stock"].tolist()


def kpi(label, value, sub, accent, tip, tone=""):
    return (f'<div class="kpi" style="--accent:{accent}" title="{tip}"><div class="kpi-l">{label}</div>'
            f'<div class="kpi-v {tone}">{value}</div><div class="kpi-s">{sub}</div></div>')


tab1, tab2, tab3, tab5, tab4 = st.tabs(["🏠  Overview", "📈  Price Trends", "🎯  Signals", "⚖️  Strategy vs Hold", "🧮  SQL Lab"])

# ================= OVERVIEW =================
with tab1:
    st.markdown(
        f'<div class="hero"><div><div class="hero-tag">The key finding</div>'
        f'<div class="hero-title">The {crash}% crash that never happened</div>'
        f'<div class="hero-sub">TCS and Infosys halved overnight because of free bonus shares, not because investors lost money.</div></div>'
        f'<div class="pairs">'
        f'<div class="pair"><div class="pair-name">TCS</div><div class="pair-old">{pct(t["Raw %"])}</div><div class="pair-arrow">▼ on paper · ▲ in reality</div><div class="pair-new">{pct(t["Adj %"])}</div></div>'
        f'<div class="pair"><div class="pair-name">INFOSYS</div><div class="pair-old">{pct(i["Raw %"])}</div><div class="pair-arrow">▼ on paper · ▲ in reality</div><div class="pair-new">{pct(i["Adj %"])}</div></div>'
        f'</div></div>', unsafe_allow_html=True)

    cards = [
        kpi("Best performer", pct(best["Adj %"]), best["Stock"], TEAL, "Biggest gain, first to last day, bonus-adjusted", "up"),
        kpi("Weakest" if worst["Adj %"] >= 0 else "Biggest loss", pct(worst["Adj %"]), worst["Stock"], GOLD,
            "The weakest of the six over the same period", "up" if worst["Adj %"] >= 0 else "down"),
        kpi("Average return", pct(avg_adj), f"raw prices: {pct(avg_raw)}", TEAL, "Mean of the six stocks, bonus-adjusted vs raw", "up"),
        kpi("Most Buy signals", f"{int(adj_sig.Buys.max())}", " · ".join(top_buys), GOLD, "Times the 20-day average crossed above the 50-day"),
        kpi("Latest signals", f'<span class="up">{n_buy}▲</span> <span class="down">{n_sell}▼</span>', "Buy ▲ · Sell ▼", TEAL,
            "Stocks whose latest signal is Buy (up) or Sell (down)"),
        kpi("Data trap", f"{len(trap)} of {len(summ)}", " · ".join(trap), RED, "Stocks with a false one-day price cliff from a bonus issue", "down"),
    ]
    st.markdown('<div class="kpis">' + "".join(cards) + "</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2], gap="large")
    with c1:
        o = summ.sort_values("Adj %")
        fig = go.Figure()
        fig.add_trace(go.Bar(y=o.Stock, x=o["Raw %"], name="On paper (raw prices)", orientation="h", marker_color="#64748B",
                             hovertemplate="%{y}: %{x:+.1f}%<extra>On paper</extra>"))
        fig.add_trace(go.Bar(y=o.Stock, x=o["Adj %"], name="In reality (adjusted)", orientation="h", marker_color=TEAL,
                             hovertemplate="%{y}: %{x:+.1f}%<extra>Adjusted</extra>"))
        style_fig(fig, "Return 2015 to 2018: on paper vs in reality", "", height=400)
        fig.update_layout(barmode="group", hovermode="closest",
                          xaxis=dict(title="Change, first to last day", ticksuffix="%", gridcolor="rgba(148,163,184,0.14)", zeroline=True,
                                     zerolinecolor="rgba(148,163,184,.5)"))
        st.plotly_chart(fig, theme=None, width="stretch")
    with c2:
        cmp_ = raw_sig.merge(adj_sig, on="Stock", suffixes=("_raw", "_adj"))
        rows = '<div class="sigrow sighead"><div>Stock</div><div>Deck (raw)</div><div>Corrected</div></div>'
        for _, r in cmp_.iterrows():
            tag = '<span class="fixed">CORRECTED</span>' if r["Latest signal_raw"] != r["Latest signal_adj"] else ""
            rows += (f'<div class="sigrow"><div>{r["Stock"]}</div><div>{pill(r["Latest signal_raw"])}</div>'
                     f'<div>{pill(r["Latest signal_adj"])}{tag}</div></div>')
        st.markdown(f'<div class="panel"><div class="panel-t">Latest Buy / Sell signal</div>{rows}</div>', unsafe_allow_html=True)

# ================= PRICE TRENDS =================
with tab2:
    if fdf.empty:
        st.info("Choose at least one stock and a valid date range in the sidebar.")
    else:
        k1, k2 = st.columns([2, 2])
        basis = k1.segmented_control("Prices", ["Adjusted", "Raw"], default="Adjusted") or "Adjusted"
        rebase = k2.toggle("Start every stock at 100", value=True, help="Lets stocks with very different prices share one chart.")
        col = "adj_close" if basis == "Adjusted" else "close_price"
        fig, moves = go.Figure(), {}
        for s in picked:
            g = fdf[fdf.stock == s].sort_values("date")
            if g.empty:
                continue
            y = g[col] / g[col].iloc[0] * 100 if rebase else g[col]
            moves[s] = 100 * (g[col].iloc[-1] / g[col].iloc[0] - 1)
            fig.add_trace(go.Scatter(x=g["date"], y=y, mode="lines", name=s, line=dict(color=STOCK_COLORS[s], width=2.2),
                                     hovertemplate="%{y:,.1f}" if rebase else "Rs. %{y:,.2f}"))
        add_bonus_lines(fig, picked, start, end)
        style_fig(fig, f"Share price trend ({basis.lower()} prices)", "Index (start = 100)" if rebase else "Close price (Rs.)", height=500)
        if moves:
            b, w = max(moves, key=moves.get), min(moves, key=moves.get)
            st.markdown(f'<div class="chips"><span class="chip"><span class="up">▲ Best</span> {b} {pct(moves[b])}</span>'
                        f'<span class="chip"><span class="down">▼ Weakest</span> {w} {pct(moves[w])}</span></div>', unsafe_allow_html=True)
        st.plotly_chart(fig, theme=None, width="stretch")
        if basis == "Raw" and any(s in BONUS for s in picked):
            st.warning("Raw prices show a false cliff for TCS and Infosys at the dashed lines. Use Adjusted for a fair view.")

# ================= SIGNALS =================
with tab3:
    if fdf.empty:
        st.info("Choose at least one stock and a valid date range in the sidebar.")
    else:
        st.caption("Buy ▲ when the 20-day average crosses above the 50-day average · Sell ▼ when it crosses below · bonus-adjusted prices")
        sig = latest_events(fdf)
        st.dataframe(style_signals(sig.set_index("Stock"), ["Latest signal"]), width="stretch")
        s = st.selectbox("Stock", picked, index=picked.index("TCS") if "TCS" in picked else 0)
        g = fdf[fdf.stock == s].sort_values("date")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=g["date"], y=g["adj_close"], name="Price", line=dict(width=1.2, color="rgba(148,163,184,.8)"), hovertemplate="Rs. %{y:,.2f}"))
        fig.add_trace(go.Scatter(x=g["date"], y=g["ma20"], name="20-day avg", line=dict(color="#60A5FA", width=2), hovertemplate="Rs. %{y:,.2f}"))
        fig.add_trace(go.Scatter(x=g["date"], y=g["ma50"], name="50-day avg", line=dict(color=GOLD, width=2), hovertemplate="Rs. %{y:,.2f}"))
        for label, symbol, color in (("Buy", "triangle-up", GREEN), ("Sell", "triangle-down", RED)):
            e = g[g.signal == label]
            fig.add_trace(go.Scatter(x=e["date"], y=e["adj_close"], mode="markers", name=label,
                                     marker=dict(symbol=symbol, size=12, color=color, line=dict(width=1, color="white")),
                                     hovertemplate=label + " at Rs. %{y:,.2f}"))
        add_bonus_lines(fig, [s], start, end)
        style_fig(fig, f"{s}: price, averages and signals", "Price (Rs., bonus-adjusted)", height=480)
        st.plotly_chart(fig, theme=None, width="stretch")
        ev = g[g.signal != "Hold"]
        with st.expander(f"All {len(ev)} Buy / Sell days for {s}"):
            tbl = pd.DataFrame({"Date": ev["date"].dt.strftime("%Y-%m-%d"), "Adjusted close": ev["adj_close"].map(rs),
                                "Signal": ev["signal"]}).set_index("Date")
            st.dataframe(style_signals(tbl, ["Signal"]), width="stretch", height=300)

# ================= STRATEGY VS HOLD =================
with tab5:
    st.caption("Buy at the close on each Buy signal, sell at the close on each Sell signal, stay in cash in between. "
               "Bonus-adjusted prices, full period (sidebar filters don't apply).")
    cost_pct = st.slider("Cost per buy or sell (brokerage and taxes)", 0.0, 1.0, 0.0, 0.1, format="%.1f%%",
                         help="Each buy and each sell loses this share of the money invested.")
    res = run_strategy(df, cost_pct / 100)
    rows, wins = [], 0
    for s in ALL_STOCKS:
        r = res[s]
        strat, hold = r["strategy"][-1] - 100, r["hold"][-1] - 100
        wins += strat > hold
        tr = r["trades"]
        rows.append((s, hold, strat, strat - hold, len(tr), 100 * sum(x > 0 for x in tr) / len(tr) if tr else 0))
    st.markdown(f'<div class="banner">Following the signals beat simply holding for <b>{wins} of {len(ALL_STOCKS)}</b> stocks '
                f'(at {cost_pct:.1f}% cost per trade).</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2], gap="large")
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(y=[r[0] for r in rows], x=[r[1] for r in rows], name="Buy and hold", orientation="h",
                             marker_color=GOLD, hovertemplate="%{y}: %{x:+.1f}%<extra>Buy and hold</extra>"))
        fig.add_trace(go.Bar(y=[r[0] for r in rows], x=[r[2] for r in rows], name="Follow the signals", orientation="h",
                             marker_color=TEAL, hovertemplate="%{y}: %{x:+.1f}%<extra>Signals</extra>"))
        style_fig(fig, "Total return 2015 to 2018: hold vs follow the signals", "", height=400)
        fig.update_layout(barmode="group", hovermode="closest", yaxis=dict(autorange="reversed"),
                          xaxis=dict(title="Total return", ticksuffix="%", gridcolor="rgba(148,163,184,0.14)", zeroline=True,
                                     zerolinecolor="rgba(148,163,184,.5)"))
        st.plotly_chart(fig, theme=None, width="stretch")
    with c2:
        head = ('<div class="strow sighead"><div>Stock</div><div>Hold</div><div>Signals</div><div>Gap</div>'
                '<div>Trades</div><div>Won</div></div>')
        body = "".join(
            f'<div class="strow"><div>{n}</div><div>{pct(h)}</div><div>{pct(st_)}</div>'
            f'<div class="{"up" if g >= 0 else "down"}">{g:+.1f} pts</div><div>{t_}</div><div>{w:.0f}%</div></div>'
            for n, h, st_, g, t_, w in rows)
        st.markdown(f'<div class="panel"><div class="panel-t">Hold vs signals</div>{head}{body}</div>', unsafe_allow_html=True)
        st.caption("Trades = buys made. Won = share of trades that made money.")

    pick = st.selectbox("Growth of 100 for", ALL_STOCKS, index=ALL_STOCKS.index("TCS"))
    r = res[pick]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=r["dates"], y=r["hold"], name="Buy and hold", line=dict(color=GOLD, width=2), hovertemplate="%{y:,.1f}"))
    fig.add_trace(go.Scatter(x=r["dates"], y=r["strategy"], name="Follow the signals", line=dict(color=TEAL, width=2), hovertemplate="%{y:,.1f}"))
    style_fig(fig, f"{pick}: what 100 would have grown to", "Value (start = 100)", height=420)
    st.plotly_chart(fig, theme=None, width="stretch")

# ================= SQL LAB =================
EXAMPLES = {
    "Eicher: five highest closes":
        "SELECT date, close_price\nFROM stocks\nWHERE stock = 'Eicher Motors'\nORDER BY close_price DESC\nLIMIT 5",
    "TCS: average close per year (raw)":
        "SELECT strftime('%Y', date) AS year, ROUND(AVG(close_price), 2) AS avg_close\n"
        "FROM stocks\nWHERE stock = 'TCS'\nGROUP BY year\nORDER BY year",
    "Worst single day per stock (finds the trap)":
        "WITH moves AS (\n  SELECT stock, date, close_price,\n"
        "    100.0 * (close_price / LAG(close_price) OVER (PARTITION BY stock ORDER BY date) - 1) AS pct_move\n"
        "  FROM stocks\n),\nranked AS (\n  SELECT stock, date, close_price, pct_move,\n"
        "    ROW_NUMBER() OVER (PARTITION BY stock ORDER BY pct_move) AS rn\n"
        "  FROM moves WHERE pct_move IS NOT NULL\n)\n"
        "SELECT stock, date, close_price, ROUND(pct_move, 1) AS pct_move\nFROM ranked WHERE rn = 1\nORDER BY pct_move",
    "Raw vs adjusted change per stock":
        "SELECT stock,\n"
        "  ROUND(100.0 * (MAX(CASE WHEN date = '2018-07-31' THEN close_price END) /\n"
        "                 MAX(CASE WHEN date = '2015-01-01' THEN close_price END) - 1), 1) AS raw_pct,\n"
        "  ROUND(100.0 * (MAX(CASE WHEN date = '2018-07-31' THEN adj_close END) /\n"
        "                 MAX(CASE WHEN date = '2015-01-01' THEN adj_close END) - 1), 1) AS adjusted_pct\n"
        "FROM stocks\nGROUP BY stock\nORDER BY adjusted_pct DESC",
    "Buy and Sell counts per stock":
        "SELECT stock,\n  SUM(signal = 'Buy') AS buys,\n  SUM(signal = 'Sell') AS sells\n"
        "FROM stocks\nGROUP BY stock\nORDER BY stock",
    "Signal on a given day (TCS)":
        "SELECT date, adj_close, signal\nFROM stocks\nWHERE stock = 'TCS'\n  AND date = '2018-04-20'",
    "Yearly average per stock (adjusted)":
        "SELECT stock, strftime('%Y', date) AS year, ROUND(AVG(adj_close), 2) AS avg_adj_close\n"
        "FROM stocks\nGROUP BY stock, year\nORDER BY stock, year",
    "Missing delivery data":
        "SELECT stock, date\nFROM stocks\nWHERE deliverable_qty IS NULL\nORDER BY date, stock",
    "Five biggest one-day moves":
        "WITH moves AS (\n  SELECT stock, date, close_price,\n"
        "    100.0 * (close_price / LAG(close_price) OVER (PARTITION BY stock ORDER BY date) - 1) AS pct_move\n"
        "  FROM stocks\n)\n"
        "SELECT stock, date, close_price, ROUND(pct_move, 1) AS pct_move\nFROM moves\nWHERE pct_move IS NOT NULL\n"
        "ORDER BY ABS(pct_move) DESC\nLIMIT 5",
}
_deadline = {"t": 0.0}

with tab4:
    st.caption(f"Read-only SQL on one table, `stocks` ({len(df):,} rows, SQLite syntax). Sidebar filters don't apply here.")
    with st.expander("Columns"):
        schema = pd.read_sql_query("PRAGMA table_info(stocks)", get_db())[["name", "type"]].rename(columns={"name": "column"})
        st.dataframe(schema.set_index("column"), width="stretch")
    choice = st.selectbox("Example", list(EXAMPLES))
    query = st.text_area("Query", value=EXAMPLES[choice], height=230, key=f"query_{choice}", label_visibility="collapsed")
    if st.button("▶  Run query", type="primary"):
        q = query.strip().rstrip(";").strip()
        if not re.match(r"^(select|with)\b", q, re.IGNORECASE):
            st.error("Only SELECT queries (or WITH ... SELECT) are allowed here.")
        elif ";" in q:
            st.error("Please run one statement at a time (remove the extra semicolon).")
        else:
            con = get_db()
            _deadline["t"] = time.time() + 5  # stop any query that runs longer than 5 seconds
            con.set_progress_handler(lambda: 1 if time.time() > _deadline["t"] else 0, 100000)
            try:
                result = pd.read_sql_query(q, con)
                st.success(f"{len(result):,} rows" + (" (showing the first 1,000)" if len(result) > 1000 else ""))
                st.dataframe(result.head(1000), hide_index=True, width="stretch")
            except Exception as e:
                st.error("That query couldn't run. Check the column names and the SQL spelling.")
                st.caption(f"Details: {e}")
            finally:
                con.set_progress_handler(None, 0)
