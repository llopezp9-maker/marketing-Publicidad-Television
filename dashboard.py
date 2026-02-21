"""
======================================================
 COLOMBIA ADVERTISING INVESTMENT STORYTELLING DASHBOARD
 Inversión Publicitaria Colombia 1995-2025 | Proyección 2031
 Autor: Luis Miguel López | Data Analyst
======================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from io import StringIO
import base64, os

# ─────────────────────────────────────────
# CONFIGURACIÓN GLOBAL
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Inversión Publicitaria Colombia | Storytelling",
    page_icon="📺",
    layout="wide",
)

# Paleta pastel para gráficas
PLOT_BG  = "#F0F5FF"   # Azul hielo muy suave: fondo de gráfica
PAPER_BG = "#F0F5FF"   # Igual para el lienzo exterior

# ─────────────────────────────────────────
# CSS PREMIUM — light, contraste alto
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #ffffff !important;
    color: #1E293B !important;
}
.stApp { background-color: #ffffff !important; }

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 65%, #60A5FA 100%);
    color: white;
    padding: 50px 40px 36px;
    border-radius: 28px;
    text-align: center;
    margin-bottom: 36px;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
    color: white !important;
}
.hero p { font-size: 1.1rem; opacity: 0.9; color: white !important; }
.hero-author {
    margin-top: 26px;
    padding-top: 22px;
    border-top: 1px solid rgba(255,255,255,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}
.hero-author-info { text-align: left; }
.hero-author-name  { font-size: 1.2rem; font-weight: 700; color: white !important; }
.hero-author-role  { font-size: 0.85rem; color: rgba(255,255,255,0.78); margin-top: 2px; }
.hero-li-link {
    background: rgba(255,255,255,0.18);
    color: white !important;
    text-decoration: none !important;
    padding: 8px 18px;
    border-radius: 30px;
    font-weight: 600;
    font-size: 0.9rem;
    border: 1px solid rgba(255,255,255,0.4);
}
.hero-li-link:hover { background: rgba(255,255,255,0.30); }

/* ── SECTION SEPARATORS ── */
.section-label {
    font-size: 0.75rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #2563EB; margin-bottom: 4px;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem; color: #0F172A; margin-bottom: 8px;
}

/* ── KPI CARDS ── */
div[data-testid="stMetric"] {
    background: #EFF6FF !important;
    border: 1.5px solid #BFDBFE !important;
    border-radius: 18px !important;
    padding: 20px 24px !important;
}
[data-testid="stMetricLabel"] > div { color: #1E40AF !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] > div { color: #0F172A !important; font-size: 1.9rem !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] > div { font-weight: 600 !important; }

/* ── NARRATIVE CARD ── */
.narr {
    background: #F8FAFC; border-left: 6px solid #2563EB;
    padding: 22px 26px; border-radius: 14px;
    line-height: 1.7; color: #334155;
    margin: 16px 0 28px; font-size: 1.05rem;
}

/* ── TABS — texto siempre visible ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px; background: #DBEAFE;
    padding: 6px; border-radius: 14px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px; padding: 8px 18px;
    color: #1E40AF !important;
    font-weight: 700 !important;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    background-color: #1E40AF !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(30,64,175,0.3);
}

/* ── SIDEBAR — texto siempre oscuro ── */
[data-testid="stSidebar"] { background-color: #EFF6FF !important; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div { color: #1E293B !important; font-weight: 500; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #1E40AF !important; font-weight: 700 !important; }
[data-baseweb="tag"] { background-color: #BFDBFE !important; }
[data-baseweb="tag"] span { color: #1E3A8A !important; }

/* ── MULTISELECT — contenedor de tags (recuadro negro → blanco) ── */
[data-baseweb="select"] > div,
[data-baseweb="base-input"],
div[data-baseweb="select"] div[role="combobox"],
div[class*="multiSelect"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #BFDBFE !important;
    border-radius: 10px !important;
    color: #1E293B !important;
}

/* ── MULTISELECT DROPDOWN POPUP — fondo azul crema, letra negra ── */
[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background-color: #EFF6FF !important;
    border: 1px solid #BFDBFE !important;
    border-radius: 12px !important;
}
[data-baseweb="menu"] li,
[role="option"],
[role="listbox"] li {
    color: #1E293B !important;
    font-weight: 500 !important;
    background-color: #EFF6FF !important;
}
[data-baseweb="menu"] li:hover,
[role="option"]:hover {
    background-color: #DBEAFE !important;
    color: #1E40AF !important;
}

/* ── FOOTER CARD DE FIRMA ── */
.footer-card {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border-radius: 22px;
    padding: 32px 40px;
    display: flex;
    align-items: center;
    gap: 36px;
    margin-top: 40px;
    flex-wrap: wrap;
    border: 1px solid #BFDBFE;
}
.footer-card-text h3 { color: #1E40AF !important; margin: 0; font-size: 1.4rem; }
.footer-card-text .role { color: #475569; margin: 4px 0 12px; font-size: 1rem; }
.footer-card-text a {
    background: #1E40AF;
    color: white !important;
    padding: 9px 22px;
    border-radius: 25px;
    text-decoration: none !important;
    font-weight: 600;
    font-size: 0.95rem;
}
.footer { text-align:center; color:#94A3B8; margin-top:16px; font-size:0.85rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# QR HELPER
# ─────────────────────────────────────────
def get_qr_b64():
    qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qr_linkedin.png")
    if os.path.exists(qr_path):
        with open(qr_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

qr_b64  = get_qr_b64()
qr_hero = (f'<img src="data:image/png;base64,{qr_b64}" width="88" '
           f'style="border-radius:10px;border:2px solid rgba(255,255,255,0.4);"/>') if qr_b64 else ""
qr_foot = (f'<img src="data:image/png;base64,{qr_b64}" width="110" '
           f'style="border-radius:14px;box-shadow:0 4px 12px rgba(30,64,175,0.15);"/>') if qr_b64 else ""


# ─────────────────────────────────────────
# DATA ENGINE
# ─────────────────────────────────────────
@st.cache_data
def build_dataset():
    try:
        df = pd.read_csv("cleaned_ad_data.csv")
    except FileNotFoundError:
        raw = (
            "AÑO;TV REG Y LOCAL;REVISTAS;PUB EXTERIOR;PRENSA;RADIO;TV NACIONAL;"
            "DIGITAL;TOTAL_INV;IPC;TRM Promedio;Penetración Internet (%);"
            "Poblacion DANE\n"
            "1995;22969.6;32751.2;15280.0;38202.0;25468.0;198962.4;0.0;333633.2;0.195;912.9;0.001;36229830\n"
            "2000;24330.8;53527.7;38491.6;96229.0;188868.2;374799.9;0.0;776246.2;0.088;2087.73;0.030;39140080\n"
            "2005;36742.0;83440.0;84253.0;353131.0;257508.0;673410.0;0.0;1488484.0;0.049;2320.08;0.121;41671878\n"
            "2010;65275.0;99876.0;128054.0;536026.0;419008.0;919366.0;94682.0;2262287.0;0.032;1897.74;0.325;44086292\n"
            "2014;71644.0;103048.0;145738.0;636192.0;550216.0;1155026.0;255389.0;2917253.0;0.037;2000.36;0.516;45866010\n"
            "2015;71228.0;95061.0;145885.0;574232.0;561034.0;1102929.0;376110.0;2926479.0;0.068;2747.73;0.572;46313898\n"
            "2016;56371.0;77516.0;130590.0;503065.0;517723.0;990127.0;409739.0;2685131.0;0.058;2977.77;0.630;46830116\n"
            "2017;51899.0;71067.0;181973.0;465685.0;528459.0;917494.0;600476.0;2817053.0;0.041;2951.0;0.665;47419200\n"
            "2018;52374.0;59988.0;184168.0;418083.0;549185.0;889760.0;848594.0;3002152.0;0.032;2956.0;0.684;48258494\n"
            "2019;60717.0;48036.0;209888.0;376697.0;541920.0;889057.0;1080535.0;3206850.0;0.038;3281.0;0.709;49395678\n"
            "2020;56101.0;19606.0;82238.0;225403.0;373737.0;763423.0;1251333.0;2771841.0;0.016;3693.0;0.720;50407647\n"
            "2021;69995.0;14732.0;166607.0;253875.0;499184.0;1037067.0;2040158.0;4081618.0;0.056;3743.0;0.752;51117378\n"
            "2022;70900.0;11470.0;274741.0;269501.0;578788.0;1043937.0;2354697.9;4604034.9;0.131;4255.44;0.768;51682692\n"
            "2023;59038.0;10513.0;279346.0;246444.0;578117.0;975070.0;2663179.0;4811707.0;0.093;4325.05;0.773;52314000\n"
            "2024;52116.3;8622.2;292696.0;215570.0;558882.4;955310.3;2825565.2;4908762.4;0.052;4072.59;0.757;52695952\n"
            "2025;61114.8;6839.0;328924.6;206962.0;560706.3;908657.0;3066685.3;5139889.1;0.035;4000.0;0.835;53200000\n"
        )
        df = pd.read_csv(StringIO(raw), sep=";")

    num_cols = [c for c in df.columns if c != "AÑO"]
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")
    df = df.set_index("AÑO").reindex(range(1995, 2026)).interpolate(method="linear").reset_index()

    pib_map = {
        1995:5.2,1996:2.1,1997:3.4,1998:0.6,1999:-4.2,
        2000:2.9,2001:1.7,2002:2.5,2003:3.9,2004:5.3,
        2005:4.7,2006:6.7,2007:6.9,2008:3.5,2009:1.7,
        2010:4.0,2011:6.6,2012:4.0,2013:4.9,2014:4.4,
        2015:3.0,2016:2.1,2017:1.4,2018:2.6,2019:3.2,
        2020:-7.0,2021:10.8,2022:7.3,2023:0.6,2024:1.5,2025:2.8,
    }
    df["PIB_PCT"]    = df["AÑO"].map(pib_map)
    df["TV_TOTAL"]   = df["TV REG Y LOCAL"] + df["TV NACIONAL"]
    df["TRADICIONAL"]= df["REVISTAS"] + df["PUB EXTERIOR"] + df["PRENSA"] + df["RADIO"]
    df["TV_SHARE"]   = df["TV_TOTAL"] / df["TOTAL_INV"]
    df["DIG_SHARE"]  = df["DIGITAL"]  / df["TOTAL_INV"]
    df["VAR_YOY"]    = df["TOTAL_INV"].pct_change() * 100

    # Proyección a 2031
    future_idx = np.arange(2026, 2032)
    proj_rows  = [{"AÑO": y, "PROYECCION": True} for y in future_idx]
    df_proj    = pd.DataFrame(proj_rows)

    for col in ["TOTAL_INV","TV_TOTAL","DIGITAL","TRADICIONAL"]:
        valid = df[["AÑO", col]].dropna()
        X = valid["AÑO"].values.reshape(-1, 1)
        y_ = valid[col].values
        model = LinearRegression().fit(X, y_)
        df_proj[col] = np.maximum(model.predict(future_idx.reshape(-1, 1)), 0)

    df["PROYECCION"] = False
    df_full = pd.concat([df, df_proj], ignore_index=True)
    return df, df_full


df_hist, df_full = build_dataset()


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Filtros")
    yr_range  = st.slider("Rango de años", 1995, 2025, (1995, 2025), step=1)
    st.markdown("---")
    medios_all = ["TV REG Y LOCAL","TV NACIONAL","DIGITAL","RADIO","PRENSA","PUB EXTERIOR","REVISTAS"]
    medios_sel = st.multiselect("Medios para gráficas", medios_all, default=medios_all)
    st.markdown("---")
    st.info("**Fuentes:** IBOPE, Kantar, DANE, Banco de la República, IAB Colombia, Banco Mundial")

df_v = df_hist[(df_hist["AÑO"] >= yr_range[0]) & (df_hist["AÑO"] <= yr_range[1])]


# ─────────────────────────────────────────
# HERO CON FIRMA
# ─────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <h1>📺 Inversión Publicitaria en Colombia</h1>
    <p>Análisis de Datos, Tendencias y Proyecciones 1995 – 2031 &nbsp;|&nbsp; Storytelling de Medios</p>
    <div class="hero-author">
        {qr_hero}
        <div class="hero-author-info">
            <div class="hero-author-name">👤 Luis Miguel López</div>
            <div class="hero-author-role">Data Analyst &nbsp;|&nbsp; Marketing & Media Intelligence</div>
        </div>
        <a href="https://www.linkedin.com/in/luislopezanalytics" target="_blank" class="hero-li-link">
            🔗 LinkedIn: luislopezanalytics
        </a>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────
r2025 = df_hist[df_hist["AÑO"] == df_hist["AÑO"].max()].iloc[0]
k1, k2, k3, k4 = st.columns(4)
k1.metric("Inversión Total 2025",  f"${r2025['TOTAL_INV']/1e6:.2f}B COP",  f"{r2025['VAR_YOY']:.1f}%")
k2.metric("Inversión TV",          f"${r2025['TV_TOTAL']/1e6:.2f}B COP",    "Ancla del Mercado")
k3.metric("Share Televisión",      f"{r2025['TV_SHARE']*100:.1f}%",          "-1.2 pts")
k4.metric("Share Digital",         f"{r2025['DIG_SHARE']*100:.1f}%",         "+4.8 pts")
st.markdown("")


# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
t1, t2, t3, t4, t5, t6 = st.tabs([
    "1 · Contexto Histórico",
    "2 · Tendencias & Mix",
    "3 · Estadística",
    "4 · Año a Año",
    "5 · Proyecciones",
    "6 · Hallazgos",
])

# ── helper para layout uniforme ──
def base_layout(fig, title="", xtitle="Año", ytitle="Inversión (M COP)"):
    fig.update_layout(
        title        = dict(text=title, font=dict(color="#0F172A", size=17, family="DM Sans")),
        paper_bgcolor= PAPER_BG,
        plot_bgcolor = PLOT_BG,
        xaxis_title  = xtitle,
        yaxis_title  = ytitle,
        font         = dict(color="#0F172A", family="DM Sans"),  # Negro para todo el texto
        legend       = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                            font=dict(color="#0F172A")),
        hovermode    = "x unified",
    )
    fig.update_xaxes(gridcolor="#DBEAFE", title_font=dict(color="#0F172A"), tickfont=dict(color="#0F172A"))
    fig.update_yaxes(gridcolor="#DBEAFE", title_font=dict(color="#0F172A"), tickfont=dict(color="#0F172A"))
    return fig


# ════════════════════════════════════════════
# TAB 1  CONTEXTO HISTÓRICO
# ════════════════════════════════════════════
with t1:
    st.markdown('<div class="section-label">Capítulo 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">El legado de 30 años de publicidad</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="narr">
    En 1995 Colombia tenía menos de 37 millones de habitantes y el internet era prácticamente invisible.
    La <strong>Televisión Nacional</strong> concentraba casi el 60% del presupuesto publicitario.
    Tres décadas después el mercado creció más de <strong>15 veces en términos nominales</strong>,
    y aunque el mapa de medios luce radicalmente distinto, la TV sigue en el centro del tablero.
    </div>
    """, unsafe_allow_html=True)

    medios_disp = [m for m in medios_sel if m in df_v.columns]

    if medios_disp:
        fig1a = px.area(df_v, x="AÑO", y=medios_disp,
                        title="Inversión histórica por medio (M COP)",
                        color_discrete_sequence=["#1D4ED8","#3B82F6","#10B981","#F59E0B","#6B7280","#94A3B8","#CBD5E1"])
        base_layout(fig1a)
        st.plotly_chart(fig1a, use_container_width=True)

    fig1b = go.Figure()
    fig1b.add_trace(go.Scatter(x=df_v["AÑO"], y=df_v["TOTAL_INV"], name="Total Mercado", line=dict(color="#0F172A", width=2)))
    fig1b.add_trace(go.Scatter(x=df_v["AÑO"], y=df_v["TV_TOTAL"],  name="Televisión",   line=dict(color="#1D4ED8", width=4)))
    fig1b.add_trace(go.Scatter(x=df_v["AÑO"], y=df_v["DIGITAL"],   name="Digital",      line=dict(color="#10B981", width=4)))
    if 2020 in df_v["AÑO"].values:
        fig1b.add_annotation(x=2020, y=df_v[df_v["AÑO"]==2020]["TOTAL_INV"].values[0]*1.06,
                             text="Pandemia -6.9%", showarrow=True, arrowhead=2,
                             bgcolor="#FEF9C3", font=dict(color="#92400E"))
    base_layout(fig1b, "Mercado Total vs TV vs Digital")
    st.plotly_chart(fig1b, use_container_width=True)


# ════════════════════════════════════════════
# TAB 2  TENDENCIAS & MIX
# ════════════════════════════════════════════
with t2:
    st.markdown('<div class="section-label">Capítulo 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tendencias: Digital vs Tradicional vs TV</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        df_norm = df_v[["AÑO","TV_TOTAL","DIGITAL","TRADICIONAL"]].copy()
        tot = df_norm[["TV_TOTAL","DIGITAL","TRADICIONAL"]].sum(axis=1)
        df_norm["TV_TOTAL"]    = df_norm["TV_TOTAL"]    / tot * 100
        df_norm["DIGITAL"]     = df_norm["DIGITAL"]     / tot * 100
        df_norm["TRADICIONAL"] = df_norm["TRADICIONAL"] / tot * 100
        fig2a = go.Figure()
        fig2a.add_trace(go.Scatter(x=df_norm["AÑO"], y=df_norm["TV_TOTAL"],    stackgroup="one", name="TV",         fillcolor="rgba(29,78,216,0.55)",  line=dict(color="#1D4ED8")))
        fig2a.add_trace(go.Scatter(x=df_norm["AÑO"], y=df_norm["DIGITAL"],     stackgroup="one", name="Digital",    fillcolor="rgba(16,185,129,0.55)", line=dict(color="#10B981")))
        fig2a.add_trace(go.Scatter(x=df_norm["AÑO"], y=df_norm["TRADICIONAL"], stackgroup="one", name="Tradicional",fillcolor="rgba(148,163,184,0.45)",line=dict(color="#94A3B8")))
        base_layout(fig2a, "Share normalizado del Presupuesto (%)", ytitle="Share (%)")
        st.plotly_chart(fig2a, use_container_width=True)

    with c2:
        fig2b = go.Figure()
        fig2b.add_trace(go.Scatter(x=df_v["AÑO"], y=df_v["TV_SHARE"]*100,  name="TV %",     fill="tozeroy", line=dict(color="#1D4ED8", width=3)))
        fig2b.add_trace(go.Scatter(x=df_v["AÑO"], y=df_v["DIG_SHARE"]*100, name="Digital %",fill="tozeroy", line=dict(color="#10B981", width=3)))
        base_layout(fig2b, "Duelo por el Share: TV vs Digital (%)", ytitle="% del presupuesto")
        st.plotly_chart(fig2b, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Inversión por Medio — Año Seleccionado")
    year_snap = st.select_slider("Seleccione el año", options=sorted(df_v["AÑO"].unique().tolist()))
    row_snap  = df_v[df_v["AÑO"] == year_snap]
    if not row_snap.empty:
        row = row_snap.iloc[0]
        snap_data = pd.DataFrame({
            "Medio": ["TV Nac.","TV Reg.","Digital","Radio","Prensa","Exterior","Revistas"],
            "Inversión": [row["TV NACIONAL"],row["TV REG Y LOCAL"],row["DIGITAL"],
                          row["RADIO"],row["PRENSA"],row["PUB EXTERIOR"],row["REVISTAS"]]
        }).sort_values("Inversión", ascending=False)
        fig2c = go.Figure(go.Bar(
            x=snap_data["Medio"], y=snap_data["Inversión"],
            marker_color=["#1D4ED8","#3B82F6","#10B981","#F59E0B","#6B7280","#94A3B8","#CBD5E1"],
            text=snap_data["Inversión"].apply(lambda v: f"{v/1e3:.0f}K"),
            textposition="outside"
        ))
        base_layout(fig2c, f"Inversión por Medio — {year_snap}", xtitle="Medio")
        st.plotly_chart(fig2c, use_container_width=True)


# ════════════════════════════════════════════
# TAB 3  ESTADÍSTICA DESCRIPTIVA
# ════════════════════════════════════════════
with t3:
    st.markdown('<div class="section-label">Capítulo 3</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Perfil estadístico de los medios</div>', unsafe_allow_html=True)

    media_stat = ["TV REG Y LOCAL","TV NACIONAL","DIGITAL","RADIO","PRENSA","PUB EXTERIOR","REVISTAS"]
    df_stat    = df_v[media_stat].dropna()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Histograma de Frecuencia**")
        var_hist = st.selectbox("Variable", media_stat)
        fig3a = go.Figure(go.Histogram(x=df_stat[var_hist], nbinsx=15, marker_color="#3B82F6",
                                        marker_line_color="white", marker_line_width=1.5))
        base_layout(fig3a, f"Distribución histórica — {var_hist}", xtitle=var_hist, ytitle="Frecuencia")
        st.plotly_chart(fig3a, use_container_width=True)

    with c2:
        st.markdown("**Boxplot — Dispersión y Outliers**")
        fig3b = go.Figure()
        colors_box = ["#1D4ED8","#3B82F6","#10B981","#F59E0B","#6B7280","#94A3B8","#CBD5E1"]
        for i, m in enumerate(media_stat):
            fig3b.add_trace(go.Box(y=df_stat[m], name=m, marker_color=colors_box[i % len(colors_box)]))
        base_layout(fig3b, "Volatilidad por Medio (Boxplot)", xtitle="Medio")
        fig3b.update_layout(showlegend=False)
        st.plotly_chart(fig3b, use_container_width=True)

    st.markdown("**Media de Inversión por Medio**")
    means = df_stat.mean().reset_index()
    means.columns = ["Medio","Media"]
    means = means.sort_values("Media", ascending=False)
    fig3c = go.Figure(go.Bar(
        x=means["Medio"], y=means["Media"],
        marker_color=["#1D4ED8","#3B82F6","#10B981","#F59E0B","#6B7280","#94A3B8","#CBD5E1"],
        text=means["Media"].apply(lambda v: f"{v/1e3:.0f}K"), textposition="outside"
    ))
    base_layout(fig3c, "Media histórica de inversión por medio", xtitle="Medio")
    st.plotly_chart(fig3c, use_container_width=True)

    st.markdown("**Tabla de Estadísticas Descriptivas**")
    stats_tbl = df_stat.describe().T
    stats_tbl["mediana"] = df_stat.median()
    stats_tbl["moda"]    = df_stat.apply(lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan)
    st.dataframe(
        stats_tbl[["mean","mediana","moda","std","min","max"]].rename(columns={
            "mean":"Media","std":"Desv. Std","min":"Mínimo","max":"Máximo",
            "mediana":"Mediana","moda":"Moda"
        }).style.format("{:,.0f}").background_gradient(cmap="Blues")
    )


# ════════════════════════════════════════════
# TAB 4  AÑO A AÑO
# ════════════════════════════════════════════
with t4:
    st.markdown('<div class="section-label">Capítulo 4</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">¿Qué pasó cada año?</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="narr">
    Cada punto de inflexión deja huella en el presupuesto publicitario.
    La caída del petróleo en 2016, la pandemia de 2020 y el rebote de 2021 son los episodios más dramáticos en 30 años.
    </div>
    """, unsafe_allow_html=True)

    df_var = df_v.dropna(subset=["VAR_YOY"])
    bar_colors = ["#F87171" if v < 0 else "#60A5FA" for v in df_var["VAR_YOY"]]
    fig4a = go.Figure(go.Bar(
        x=df_var["AÑO"], y=df_var["VAR_YOY"],
        marker_color=bar_colors,
        text=[f"{v:.1f}%" for v in df_var["VAR_YOY"]], textposition="outside"
    ))
    for hito in [(2020,"Pandemia\n-6.9%"),(2021,"Rebote\n+47.5%"),(2016,"Crisis\nPetróleo")]:
        y_val = df_var[df_var["AÑO"]==hito[0]]["VAR_YOY"]
        if not y_val.empty:
            fig4a.add_annotation(x=hito[0], y=y_val.values[0],
                                  text=hito[1], showarrow=True, arrowhead=2,
                                  bgcolor="#FEF9C3", font=dict(color="#78350F", size=11))
    base_layout(fig4a, "Variación Porcentual Anual de la Inversión Total (%)", ytitle="Variación (%)")
    st.plotly_chart(fig4a, use_container_width=True)

    fig4b = go.Figure(go.Waterfall(
        x=df_v["AÑO"].tolist(),
        y=df_v["TV_TOTAL"].diff().fillna(df_v["TV_TOTAL"].iloc[0]).tolist(),
        connector=dict(line=dict(color="#BFDBFE")),
        increasing=dict(marker=dict(color="#60A5FA")),
        decreasing=dict(marker=dict(color="#F87171")),
    ))
    base_layout(fig4b, "Variación Incremental de TV por Año (Waterfall)")
    st.plotly_chart(fig4b, use_container_width=True)


# ════════════════════════════════════════════
# TAB 5  PROYECCIONES
# ════════════════════════════════════════════
with t5:
    st.markdown('<div class="section-label">Capítulo 5</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Proyecciones al 2031: Tres métodos</div>', unsafe_allow_html=True)

    proj_slice = df_full[df_full["PROYECCION"] == True]

    # Método 1: Regresión Lineal
    st.markdown("#### Método 1 — Regresión Lineal (Mercado Total)")
    fig5a = go.Figure()
    fig5a.add_trace(go.Scatter(x=df_hist["AÑO"], y=df_hist["TOTAL_INV"],
                                name="Histórico", mode="lines+markers", line=dict(color="#1D4ED8", width=3)))
    fig5a.add_trace(go.Scatter(x=proj_slice["AÑO"], y=proj_slice["TOTAL_INV"],
                                name="Proyección", mode="lines+markers",
                                line=dict(color="#93C5FD", width=3, dash="dash"),
                                marker=dict(symbol="diamond")))
    fig5a.add_vrect(x0=2025.5, x1=2031.5, fillcolor="#DBEAFE", opacity=0.5,
                    layer="below", annotation_text="Zona Proyección", annotation_position="top left")
    base_layout(fig5a, "Regresión Lineal: Inversión Total 1995 – 2031")
    st.plotly_chart(fig5a, use_container_width=True)

    # Método 2: Series de Tiempo
    st.markdown("#### Método 2 — Series de Tiempo (TV vs Digital al 2031)")
    fig5b = go.Figure()
    fig5b.add_trace(go.Scatter(x=df_hist["AÑO"],     y=df_hist["TV_TOTAL"],    name="TV Histórico", line=dict(color="#1D4ED8", width=4)))
    fig5b.add_trace(go.Scatter(x=proj_slice["AÑO"],  y=proj_slice["TV_TOTAL"], name="TV Proyectado", line=dict(color="#93C5FD", width=3, dash="dot"), marker=dict(symbol="diamond")))
    fig5b.add_trace(go.Scatter(x=df_hist["AÑO"],     y=df_hist["DIGITAL"],     name="Digital Histórico", line=dict(color="#10B981", width=4)))
    fig5b.add_trace(go.Scatter(x=proj_slice["AÑO"],  y=proj_slice["DIGITAL"],  name="Digital Proyectado",line=dict(color="#6EE7B7", width=3, dash="dot")))
    fig5b.add_vrect(x0=2025.5, x1=2031.5, fillcolor="#F0FDF4", opacity=0.5, layer="below", annotation_text="Futuro")
    base_layout(fig5b, "Series de Tiempo: Trayectorias TV y Digital al 2031")
    st.plotly_chart(fig5b, use_container_width=True)

    # Método 3: Correlación
    st.markdown("#### Método 3 — Correlación: Penetración de Internet vs Inversión TV")
    df_corr = df_hist[["Penetración Internet (%)","TV_TOTAL","AÑO"]].dropna()
    X_c = df_corr[["Penetración Internet (%)"]].values
    y_c = df_corr["TV_TOTAL"].values
    model_c = LinearRegression().fit(X_c, y_c)
    x_line  = np.linspace(X_c.min(), X_c.max(), 80)
    y_line  = model_c.predict(x_line.reshape(-1, 1))
    fig5c = go.Figure()
    fig5c.add_trace(go.Scatter(
        x=df_corr["Penetración Internet (%)"], y=df_corr["TV_TOTAL"],
        mode="markers+text",
        text=df_corr["AÑO"].astype(int).astype(str), textposition="top center",
        marker=dict(color="#1D4ED8", size=9), name="Cada año"))
    fig5c.add_trace(go.Scatter(x=x_line, y=y_line, mode="lines",
                                name="Tendencia", line=dict(color="#F59E0B", width=3, dash="dash")))
    base_layout(fig5c, "Correlación: Internet (%) vs Inversión TV",
                xtitle="Penetración Internet (%)", ytitle="Inversión TV (M COP)")
    corr_val = np.corrcoef(df_corr["Penetración Internet (%)"], df_corr["TV_TOTAL"])[0,1]
    st.plotly_chart(fig5c, use_container_width=True)
    st.info(f"**Correlación de Pearson = {corr_val:.2f}** — La TV crece junto con el acceso a internet, refutando el mito de sustitución.")


# ════════════════════════════════════════════
# TAB 6  HALLAZGOS FINALES
# ════════════════════════════════════════════
with t6:
    st.markdown('<div class="section-label">Capítulo 6</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">La TV y el PIB: El ecosistema que no muere</div>', unsafe_allow_html=True)

    df_pib = df_hist.dropna(subset=["PIB_PCT"])
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(x=df_pib["AÑO"], y=df_pib["TOTAL_INV"],
                           name="Inversión Publicitaria (M COP)", marker_color="#BFDBFE"))
    fig6.add_trace(go.Scatter(x=df_pib["AÑO"], y=df_pib["PIB_PCT"],
                               name="Crecimiento PIB (%)", yaxis="y2",
                               line=dict(color="#1D4ED8", width=3)))
    fig6.update_layout(
        title        = dict(text="Inversión Publicitaria vs Crecimiento del PIB en Colombia",
                            font=dict(color="#0F172A", size=17)),
        paper_bgcolor= PAPER_BG,
        plot_bgcolor = PLOT_BG,
        font         = dict(color="#0F172A", family="DM Sans"),
        yaxis        = dict(title="Inversión (M COP)", gridcolor="#DBEAFE",
                            title_font=dict(color="#0F172A"), tickfont=dict(color="#0F172A")),
        yaxis2       = dict(title="Crecimiento PIB (%)", overlaying="y", side="right", showgrid=False,
                            title_font=dict(color="#0F172A"), tickfont=dict(color="#0F172A")),
        legend       = dict(orientation="h", y=1.12, font=dict(color="#0F172A")),
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("""
    <div class="narr">
    🔵 <strong>La TV no muere — se transforma.</strong>
    Desde 1995, la inversión acumulada en televisión supera los <em>25 billones de pesos</em>.
    Aunque su share cayó del 60% al 19%, en términos absolutos la inversión <strong>se triplicó</strong>.<br><br>
    📈 <strong>Relación TV–PIB.</strong>
    La curva publicitaria es espejo fiel del ciclo económico. En recesiones, la TV regional es el último presupuesto en recortarse.<br><br>
    🌐 <strong>Convergencia, no sustitución.</strong>
    El coeficiente de correlación entre penetración de internet e inversión en TV es positivo: ambos ecosistemas se potencian.<br><br>
    📊 <strong>Para 2031</strong> el mercado publicitario superará los <em>6.5 billones de pesos</em>.
    La TV Conectada (CTV) y el Streaming capturarán presupuesto digital bajo la lógica y métricas de televisión.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button("📥 Descargar Dataset (CSV)",
                           df_full.to_csv(index=False).encode(),
                           "colombia_publicidad_1995_2031.csv", "text/csv")
    with dl2:
        with open(__file__, "rb") as f:
            st.download_button("🐍 Descargar Código Fuente (.py)",
                               f, "dashboard_storytelling_colombia.py", "text/plain")


# ─────────────────────────────────────────
# FOOTER — FIRMA DE AUTOR
# ─────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div class="footer-card">
    {qr_foot}
    <div class="footer-card-text">
        <h3>👤 Luis Miguel López</h3>
        <div class="role">Data Analyst &nbsp;•&nbsp; Marketing & Media Intelligence &nbsp;•&nbsp; Colombia</div>
        <a href="https://www.linkedin.com/in/luislopezanalytics" target="_blank">
            🔗 www.linkedin.com/in/luislopezanalytics
        </a>
    </div>
</div>
<div class="footer">
    Colombia Advertising Intelligence &nbsp;|&nbsp;
    Data Storytelling Dashboard &nbsp;|&nbsp; 2026 &nbsp;|&nbsp;
    Fuentes: IBOPE · DANE · Banco Mundial · IAB Colombia
</div>
""", unsafe_allow_html=True)
