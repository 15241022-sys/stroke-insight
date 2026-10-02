import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit.components.v1 import html

# ════════════════════════════════════════════════════════════════════ CONFIG
st.set_page_config(
    page_title="Stroke Insight Dashboard",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY  = "#0E1B48"
MAUVE = "#C18DB4"
BLUSH = "#E2CAD8"
SKY   = "#87A7D0"
SLATE = "#27425D"
INK   = "#0E1F2F"
COLOR_MAP = {"Tidak Stroke": SKY, "Stroke": MAUVE}

# ════════════════════════════════════════════════════════════════════ CSS
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {{ font-family: 'Inter', sans-serif !important; }}

/* ──────────── APP SHELL ──────────── */
.stApp {{
    background: {INK};
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(14,27,72,.6) 0%, transparent 70%),
        radial-gradient(ellipse 60% 50% at 90% 80%, rgba(193,141,180,.07) 0%, transparent 60%),
        linear-gradient(180deg, {INK} 0%, #060d1f 100%);
}}

/* ──────────── SIDEBAR ──────────── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #080e22 0%, #0b1530 50%, #0d1a3a 100%) !important;
    border-right: none !important;
    box-shadow: 6px 0 40px rgba(0,0,0,.5);
}}
[data-testid="stSidebar"] > div:first-child {{
    background: none !important;
}}
section[data-testid="stSidebarSidebar"] > div > div {{
    background: none !important;
}}

/* ──────────── TEXT HIERARCHY ──────────── */
h1 {{ color: #fff !important; font-weight: 900 !important; font-size: 2.6rem !important;
      letter-spacing: -.04em !important; line-height: 1.1 !important; }}
h2 {{ color: #fff !important; font-weight: 700 !important; }}
h3 {{ color: {BLUSH} !important; font-weight: 600 !important; }}
.stCaption {{ color: rgba(135,167,208,.6) !important; font-size: .82rem !important; }}
p, span, label {{ color: rgba(226,202,216,.8) !important; }}

/* ──────────── SIDEBAR BRAND ──────────── */
.sb-brand {{
    text-align: center; padding: 28px 16px 20px;
}}
.sb-brand-icon {{
    width: 56px; height: 56px; margin: 0 auto 12px;
    background: linear-gradient(135deg, {MAUVE}, {SKY});
    border-radius: 16px; display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem; box-shadow: 0 4px 20px rgba(193,141,180,.3);
}}
.sb-brand-title {{
    font-size: 1.15rem; font-weight: 800; color: #fff;
    letter-spacing: -.02em; margin-bottom: 2px;
}}
.sb-brand-sub {{
    font-size: .7rem; color: {SKY}; opacity: .55;
    text-transform: uppercase; letter-spacing: .1em;
}}
.sb-divider {{
    height: 1px; margin: 16px 8px;
    background: linear-gradient(90deg, transparent, rgba(135,167,208,.15), transparent);
}}
.sb-section {{
    font-size: .68rem; font-weight: 700; color: {MAUVE};
    text-transform: uppercase; letter-spacing: .12em;
    margin: 18px 0 8px 4px; opacity: .8;
}}

/* ──────────── HERO HEADER ──────────── */
.hero {{
    position: relative; padding: 32px 0 20px; margin-bottom: 4px;
}}
.hero-glow {{
    position: absolute; top: -40px; left: 50%; transform: translateX(-50%);
    width: 500px; height: 180px;
    background: radial-gradient(ellipse, rgba(193,141,180,.08) 0%, transparent 70%);
    pointer-events: none;
}}
.hero-line {{
    height: 3px; border-radius: 3px;
    background: linear-gradient(90deg, transparent, {SKY}, {MAUVE}, {BLUSH}, transparent);
    margin-bottom: 20px;
    animation: heroPulse 4s ease-in-out infinite;
}}
@keyframes heroPulse {{
    0%,100% {{ opacity: .5; transform: scaleX(.95); }}
    50% {{ opacity: 1; transform: scaleX(1); }}
}}
.hero-title {{
    font-size: 2.5rem; font-weight: 900; color: #fff;
    letter-spacing: -.04em; line-height: 1.1; margin-bottom: 6px;
}}
.hero-title em {{
    font-style: normal;
    background: linear-gradient(135deg, {MAUVE}, {BLUSH});
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.hero-sub {{
    font-size: .88rem; color: rgba(135,167,208,.55); font-weight: 400;
}}

/* ──────────── KPI ──────────── */
.kpi-row {{
    display: grid; grid-template-columns: repeat(4,1fr); gap: 16px;
    margin: 8px 0 20px;
}}
.kpi {{
    position: relative; padding: 24px 20px 20px; text-align: center;
    background: rgba(14,27,72,.3);
    border: 1px solid rgba(135,167,208,.08);
    border-radius: 20px;
    overflow: hidden;
    transition: all .3s cubic-bezier(.4,0,.2,1);
}}
.kpi:hover {{
    transform: translateY(-6px);
    border-color: rgba(193,141,180,.2);
    box-shadow: 0 20px 50px rgba(0,0,0,.4), 0 0 30px rgba(193,141,180,.08);
}}
.kpi::before {{
    content:''; position:absolute; inset:0;
    background: linear-gradient(160deg, rgba(135,167,208,.06) 0%, transparent 50%);
    pointer-events: none;
}}
.kpi-glow {{
    position: absolute; top: -20px; left: 50%; transform: translateX(-50%);
    width: 80px; height: 60px; border-radius: 50%;
    filter: blur(30px); opacity: .35; pointer-events: none;
}}
.kpi-icon {{
    font-size: 1.5rem; margin-bottom: 10px;
    display: inline-block;
    filter: drop-shadow(0 2px 6px rgba(0,0,0,.3));
}}
.kpi-label {{
    font-size: .7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: .1em; color: {SKY}; opacity: .7; margin-bottom: 6px;
}}
.kpi-val {{
    font-size: 2.3rem; font-weight: 900; color: #fff;
    letter-spacing: -.03em; line-height: 1;
}}

/* ──────────── TABS ──────────── */
[data-baseweb="tab-list"] {{
    gap: 6px !important;
    background: rgba(14,27,72,.25) !important;
    border: 1px solid rgba(135,167,208,.06) !important;
    border-radius: 16px !important;
    padding: 5px !important;
    backdrop-filter: blur(12px) !important;
}}
button[data-baseweb="tab"] {{
    border-radius: 12px !important;
    padding: 9px 20px !important;
    font-weight: 600 !important; font-size: .85rem !important;
    color: rgba(135,167,208,.5) !important;
    transition: all .25s ease !important;
    border: none !important; background: transparent !important;
}}
button[data-baseweb="tab"]:hover {{
    color: {BLUSH} !important;
    background: rgba(135,167,208,.06) !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    background: linear-gradient(135deg, rgba(135,167,208,.12), rgba(193,141,180,.08)) !important;
    color: #fff !important;
    box-shadow: 0 2px 16px rgba(193,141,180,.12) !important;
    border: 1px solid rgba(193,141,180,.12) !important;
}}

/* ──────────── CHART FRAME ──────────── */
.frame {{
    background: rgba(10,18,42,.5);
    border: 1px solid rgba(135,167,208,.06);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,.2), inset 0 1px 0 rgba(255,255,255,.02);
    backdrop-filter: blur(8px);
}}
.frame-title {{
    font-size: .72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .1em; color: {MAUVE}; opacity: .6; margin-bottom: 12px;
}}

/* ──────────── CTRL PANEL ──────────── */
.ctrl {{
    background: rgba(10,18,42,.55);
    border: 1px solid rgba(135,167,208,.08);
    border-radius: 16px;
    padding: 22px 18px;
    backdrop-filter: blur(10px);
}}
.ctrl-label {{
    font-size: .72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .08em; color: {SKY}; opacity: .7; margin-bottom: 6px;
}}

/* ──────────── BUTTONS ──────────── */
.stDownloadButton > button {{
    background: linear-gradient(135deg, {SLATE}, rgba(14,27,72,.8)) !important;
    color: {BLUSH} !important;
    border: 1px solid rgba(193,141,180,.2) !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(0,0,0,.4) !important;
    transition: all .3s ease !important;
}}
.stDownloadButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(193,141,180,.15) !important;
    border-color: rgba(193,141,180,.35) !important;
}}

/* ──────────── MISC ──────────── */
.stAlert {{ border-radius: 14px !important; }}
.stDataFrame {{ border-radius: 16px !important; overflow: hidden !important; }}
hr {{ border: none !important; height: 1px !important;
      background: linear-gradient(90deg, transparent, rgba(135,167,208,.1), transparent) !important; }}
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {SLATE}; border-radius: 10px; }}

/* ──────────── FOOTER ──────────── */
.foot {{
    text-align: center; padding: 24px 0 8px; margin-top: 16px;
    font-size: .72rem; color: rgba(135,167,208,.3);
    border-top: 1px solid rgba(135,167,208,.05);
}}
.foot span {{ color: {MAUVE}; opacity: .6; }}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════ DATA
@st.cache_data
def load_data():
    df = pd.read_csv("healthcare-dataset-stroke-data.csv")
    df = df.drop(columns="id")
    df["status_stroke"] = df["stroke"].map({0: "Tidak Stroke", 1: "Stroke"})
    return df

df = load_data()

def style(fig, height=440):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=BLUSH, size=12),
        legend=dict(
            title="", orientation="h", y=1.1,
            font=dict(size=12, color=BLUSH),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=6, r=6, t=48, b=6),
    )
    for ax in (fig.update_xaxes, fig.update_yaxes):
        ax(
            gridcolor="rgba(135,167,208,.06)",
            zerolinecolor="rgba(135,167,208,.1)",
            tickfont=dict(color=SKY, size=10),
            title_font=dict(color=BLUSH, size=12, family="Inter"),
        )
    return fig

# ════════════════════════════════════════════════════════════════════ SIDEBAR
with st.sidebar:
    st.markdown(f"""
    <div class="sb-brand">
        <div class="sb-brand-icon">🫀</div>
        <div class="sb-brand-title">Stroke Insight</div>
        <div class="sb-brand-sub">Interactive Dashboard</div>
    </div>
    <div class="sb-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="sb-section">Demografi</div>', unsafe_allow_html=True)
    gender = st.multiselect("Gender", df["gender"].unique(),
                            default=list(df["gender"].unique()), label_visibility="collapsed")
    age_min, age_max = int(df["age"].min()), int(df["age"].max())
    age_rng = st.slider("Rentang Usia", age_min, age_max, (age_min, age_max), label_visibility="collapsed")

    st.markdown(f'<div class="sb-section">Lifestyle</div>', unsafe_allow_html=True)
    smoke = st.multiselect("Status Merokok", df["smoking_status"].unique(),
                           default=list(df["smoking_status"].unique()), label_visibility="collapsed")

    st.markdown(f'<div class="sb-section">Lokasi</div>', unsafe_allow_html=True)
    resid = st.multiselect("Tipe Tempat Tinggal", df["Residence_type"].unique(),
                           default=list(df["Residence_type"].unique()), label_visibility="collapsed")

    st.markdown(f"""
    <div class="sb-divider"></div>
    <div style="text-align:center; padding:8px 0;">
        <div style="display:inline-flex; gap:6px; align-items:center;">
            <span style="width:10px;height:10px;border-radius:50%;background:{NAVY};display:inline-block;"></span>
            <span style="width:10px;height:10px;border-radius:50%;background:{MAUVE};display:inline-block;"></span>
            <span style="width:10px;height:10px;border-radius:50%;background:{BLUSH};display:inline-block;"></span>
            <span style="width:10px;height:10px;border-radius:50%;background:{SKY};display:inline-block;"></span>
            <span style="width:10px;height:10px;border-radius:50%;background:{SLATE};display:inline-block;"></span>
            <span style="width:10px;height:10px;border-radius:50%;background:{INK};display:inline-block;border:1px solid rgba(135,167,208,.2);"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

f = df[
    df["gender"].isin(gender)
    & df["Residence_type"].isin(resid)
    & df["smoking_status"].isin(smoke)
    & df["age"].between(*age_rng)
]

# ════════════════════════════════════════════════════════════════════ HERO
st.markdown(f"""
<div class="hero">
    <div class="hero-glow"></div>
    <div class="hero-line"></div>
    <div class="hero-title">Stroke <em>Insight</em></div>
    <div class="hero-sub">Eksplorasi faktor risiko stroke · Healthcare Stroke Dataset</div>
</div>
""", unsafe_allow_html=True)

if f.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
    st.stop()

# ════════════════════════════════════════════════════════════════════ KPI
total   = len(f)
stroke  = int(f["stroke"].sum())
pct     = f["stroke"].mean() * 100
avg_age = f["age"].mean()

kpi_data = [
    ("👥", "Total Pasien",      f"{total:,}",        SKY),
    ("⚠️", "Kasus Stroke",      f"{stroke:,}",       MAUVE),
    ("📈", "Persentase Stroke", f"{pct:.2f}%",       BLUSH),
    ("🎂", "Rata-rata Usia",    f"{avg_age:.1f} th", SKY),
]

kpi_html = '<div class="kpi-row">'
for icon, label, value, glow_color in kpi_data:
    kpi_html += f"""
    <div class="kpi">
        <div class="kpi-glow" style="background:{glow_color};"></div>
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-val">{value}</div>
    </div>"""
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════ TABS
NUM = ["age", "avg_glucose_level", "bmi"]
CAT = ["status_stroke", "gender", "smoking_status", "work_type",
       "Residence_type", "hypertension", "heart_disease", "ever_married"]

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Histogram", "📦  Boxplot", "🔵  Scatter", "🔥  Heatmap", "📋  Data"
])

# ────────────────────── HISTOGRAM
with tab1:
    c1, c2 = st.columns([1, 4])
    with c1:
        st.markdown('<div class="ctrl">', unsafe_allow_html=True)
        st.markdown('<div class="ctrl-label">Variabel</div>', unsafe_allow_html=True)
        var = st.selectbox("Variabel", NUM, key="h_var", label_visibility="collapsed")
        st.markdown('<div class="ctrl-label">Bins</div>', unsafe_allow_html=True)
        bins = st.slider("Bins", 10, 80, 30, label_visibility="collapsed")
        norm = st.checkbox("Normalisasi (%)", value=True,
                           help="Penting karena kasus stroke jauh lebih sedikit.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        fig = px.histogram(
            f, x=var, color="status_stroke", nbins=bins,
            barmode="overlay", opacity=0.7,
            histnorm="percent" if norm else None,
            color_discrete_map=COLOR_MAP,
        )
        fig.update_traces(
            marker_line_width=0, marker_opacity=0.75,
        )
        st.markdown('<div class="frame"><div class="frame-title">Distribusi Histogram</div>', unsafe_allow_html=True)
        st.plotly_chart(style(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ────────────────────── BOXPLOT
with tab2:
    c1, c2 = st.columns([1, 4])
    with c1:
        st.markdown('<div class="ctrl">', unsafe_allow_html=True)
        st.markdown('<div class="ctrl-label">Numerik (Y)</div>', unsafe_allow_html=True)
        y = st.selectbox("Y", NUM, key="b_y", label_visibility="collapsed")
        st.markdown('<div class="ctrl-label">Kategori (X)</div>', unsafe_allow_html=True)
        x = st.selectbox("X", CAT, key="b_x", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        fig = px.box(
            f, x=x, y=y, color="status_stroke",
            color_discrete_map=COLOR_MAP, points="outliers",
        )
        fig.update_traces(
            marker_size=3, marker_opacity=0.4,
            boxmean="sd", line_width=1.2,
            fillcolor=None,
        )
        st.markdown('<div class="frame"><div class="frame-title">Distribusi Boxplot</div>', unsafe_allow_html=True)
        st.plotly_chart(style(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ────────────────────── SCATTERPLOT
with tab3:
    c1, c2 = st.columns([1, 4])
    with c1:
        st.markdown('<div class="ctrl">', unsafe_allow_html=True)
        st.markdown('<div class="ctrl-label">Sumbu X</div>', unsafe_allow_html=True)
        sx = st.selectbox("X", NUM, index=0, key="s_x", label_visibility="collapsed")
        st.markdown('<div class="ctrl-label">Sumbu Y</div>', unsafe_allow_html=True)
        sy = st.selectbox("Y", NUM, index=1, key="s_y", label_visibility="collapsed")
        trend = st.checkbox("Tren OLS", value=False)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        fig = px.scatter(
            f, x=sx, y=sy, color="status_stroke",
            opacity=0.55, color_discrete_map=COLOR_MAP,
            hover_data=["gender", "smoking_status", "age"],
            trendline="ols" if trend else None,
            trendline_color_override=BLUSH,
        )
        fig.update_traces(marker_size=4.5, marker_line_width=0)
        st.markdown('<div class="frame"><div class="frame-title">Scatter Plot</div>', unsafe_allow_html=True)
        st.plotly_chart(style(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    if trend:
        st.caption("Membutuhkan `statsmodels` · tambahkan ke requirements.txt")

# ────────────────────── HEATMAP
with tab4:
    corr = f[["age","hypertension","heart_disease",
              "avg_glucose_level","bmi","stroke"]].corr()
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        zmin=-1, zmax=1, zmid=0,
        colorscale=[
            [0.00, SKY], [0.20, SLATE], [0.45, NAVY],
            [0.55, NAVY], [0.80, MAUVE], [1.00, BLUSH],
        ],
        text=corr.round(2).values,
        texttemplate="%{text}",
        textfont=dict(size=13, color="#fff", family="Inter"),
        hoverongaps=False, xgap=4, ygap=4,
    ))
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(tickangle=35)
    st.markdown('<div class="frame"><div class="frame-title">Korelasi Antar Variabel</div>', unsafe_allow_html=True)
    st.plotly_chart(style(fig, 520), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ────────────────────── DATA
with tab5:
    st.markdown('<div class="frame">', unsafe_allow_html=True)
    st.dataframe(f.drop(columns="status_stroke"), use_container_width=True, height=460)
    st.markdown('</div>', unsafe_allow_html=True)
    _, dc, _ = st.columns([3, 1, 3])
    with dc:
        st.download_button(
            "⬇️  Unduh CSV",
            f.to_csv(index=False),
            "stroke_filtered.csv",
            use_container_width=True,
        )

# ════════════════════════════════════════════════════════════════════ FOOTER
st.markdown(f"""
<div class="foot">
    Stroke Insight Dashboard &nbsp;·&nbsp;
    <span>{NAVY}</span> &nbsp;
    <span>{MAUVE}</span> &nbsp;
    <span>{BLUSH}</span> &nbsp;
    <span>{SKY}</span> &nbsp;
    <span>{SLATE}</span> &nbsp;
    <span>{INK}</span>
</div>
""", unsafe_allow_html=True)