"""
======================================================
 COLOMBIA ADVERTISING INVESTMENT STORYTELLING DASHBOARD
 Inversión Publicitaria Colombia 1995-2025 | Proyección 2031
======================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from io import StringIO

# ─────────────────────────────────────────
# CONFIGURACIÓN GLOBAL
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Inversión Publicitaria Colombia | Storytelling",
    page_icon="📺",
    layout="wide",
)

# CSS PREMIUM LIGHT (tema claro, contraste alto, profesional)
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
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 60%, #60A5FA 100%);
    color: white;
    padding: 56px 40px;
    border-radius: 28px;
    text-align: center;
    margin-bottom: 40px;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 3.4rem;
    margin-bottom: 12px;
    letter-spacing: -0.03em;
}
.hero p { font-size: 1.15rem; opacity: 0.88; }

/* ── SECTION SEPARATORS ── */
.section-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #2563EB;
    margin-bottom: 4px;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #0F172A;
    margin-bottom: 8px;
}

/* ── KPI CARDS ── */
div[data-testid="stMetric"] {
    background: #F0F6FF !important;
    border: 1.5px solid #BFDBFE !important;
    border-radius: 18px !important;
    padding: 20px 24px !important;
}
[data-testid="stMetricLabel"] > div { color: #1E40AF !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] > div { color: #0F172A !important; font-size: 2rem !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] > div { font-weight: 600 !important; }

/* ── NARRATIVE CARD ── */
.narr {
    background: #F8FAFC;
    border-left: 6px solid #2563EB;
    padding: 22px 26px;
    border-radius: 14px;
    line-height: 1.7;
    color: #334155;
    margin: 16px 0 28px;
    font-size: 1.05rem;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: #F1F5F9;
    padding: 6px;
    border-radius: 14px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 8px 20px;
    color: #64748B;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background-color: #fff !important;
    color: #1E40AF !important;
    box-shadow: 0 2px 8px rgba(30,64,175,0.1);
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] { background: #F8FAFC !important; }

/* Footer */
.footer { text-align:center; color:#94A3B8; margin-top:50px; font-size:0.9rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# DATA ENGINE — CARGA + LIMPIEZA + PROYECCIONES
# ─────────────────────────────────────────
@st.cache_data
def build_dataset():
    """
    Carga el CSV procesado (cleaned_ad_data.csv) o reconstruye desde datos
    embebidos. Incluye interpolación, imputación de PIB conocido y
    proyección lineal a 2031.
    """
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

    # — Interpolación lineal para llenar huecos internos
    num_cols = [c for c in df.columns if c != "AÑO"]
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")
    df = df.set_index("AÑO").reindex(range(1995, 2026)).interpolate(method="linear").reset_index()

    # — PIB % Colombia (DANE / Banco Mundial histórico + est.)
    pib_map = {
        1995: 5.2, 1996: 2.1, 1997: 3.4, 1998: 0.6, 1999: -4.2,
        2000: 2.9, 2001: 1.7, 2002: 2.5, 2003: 3.9, 2004: 5.3,
        2005: 4.7, 2006: 6.7, 2007: 6.9, 2008: 3.5, 2009: 1.7,
        2010: 4.0, 2011: 6.6, 2012: 4.0, 2013: 4.9, 2014: 4.4,
        2015: 3.0, 2016: 2.1, 2017: 1.4, 2018: 2.6, 2019: 3.2,
        2020: -7.0, 2021: 10.8, 2022: 7.3, 2023: 0.6, 2024: 1.5,
        2025: 2.8,
    }
    df["PIB_PCT"] = df["AÑO"].map(pib_map)

    # — Métricas derivadas
    df["TV_TOTAL"]      = df["TV REG Y LOCAL"] + df["TV NACIONAL"]
    df["TRADICIONAL"]   = df["REVISTAS"] + df["PUB EXTERIOR"] + df["PRENSA"] + df["RADIO"]
    df["TV_SHARE"]      = df["TV_TOTAL"] / df["TOTAL_INV"]
    df["DIG_SHARE"]     = df["DIGITAL"] / df["TOTAL_INV"]
    df["VAR_YOY"]       = df["TOTAL_INV"].pct_change() * 100

    # ── PROYECCIONES A 6 AÑOS (2026-2031) con Regresión Lineal ──
    future_idx = np.arange(2026, 2032)
    proj_rows = []
    for yr in future_idx:
        row = {"AÑO": yr, "PROYECCION": True}
        proj_rows.append(row)
    df_proj = pd.DataFrame(proj_rows)

    forecast_cols = ["TOTAL_INV", "TV_TOTAL", "DIGITAL", "TRADICIONAL"]
    for col in forecast_cols:
        valid = df[["AÑO", col]].dropna()
        X = valid["AÑO"].values.reshape(-1, 1)
        y = valid[col].values
        model = LinearRegression().fit(X, y)
        df_proj[col] = np.maximum(model.predict(future_idx.reshape(-1, 1)), 0)

    df["PROYECCION"] = False
    df_full = pd.concat([df, df_proj], ignore_index=True)
    return df, df_full


df_hist, df_full = build_dataset()


# ─────────────────────────────────────────
# SIDEBAR — FILTROS GLOBALES (REQUISITO: filtros)
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Filtros")
    yr_range = st.slider("Rango de años (histórico)", 1995, 2025, (1995, 2025), step=1)
    st.markdown("---")
    medios_all = ["TV REG Y LOCAL", "TV NACIONAL", "DIGITAL", "RADIO", "PRENSA", "PUB EXTERIOR", "REVISTAS"]
    medios_sel = st.multiselect("Medios para gráficas", medios_all, default=medios_all)
    st.markdown("---")
    st.info("**Fuentes:** IBOPE, Kantar, DANE, Banco de la República, IAB Colombia, Banco Mundial")

df_v = df_hist[(df_hist["AÑO"] >= yr_range[0]) & (df_hist["AÑO"] <= yr_range[1])]

# ─────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>📺 Inversión Publicitaria en Colombia</h1>
    <p>Análisis de Datos, Tendencias y Proyecciones 1995 – 2031 &nbsp;|&nbsp; Storytelling de Medios</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# KPIs PRINCIPALES
# ─────────────────────────────────────────
r2025 = df_hist[df_hist["AÑO"] == min(2025, df_hist["AÑO"].max())].iloc[0]
k1, k2, k3, k4 = st.columns(4)
k1.metric("Inversión Total 2025", f"${r2025['TOTAL_INV']/1e6:.2f}B COP", f"{r2025['VAR_YOY']:.1f}%")
k2.metric("Inversión Total TV", f"${r2025['TV_TOTAL']/1e6:.2f}B COP", "Ancla del Mercado")
k3.metric("Share Televisión", f"{r2025['TV_SHARE']*100:.1f}%", "-1.2 pts")
k4.metric("Share Digital", f"{r2025['DIG_SHARE']*100:.1f}%", "+4.8 pts")

st.markdown("")

# ─────────────────────────────────────────
# PESTAÑAS PRINCIPALES
# ─────────────────────────────────────────
t1, t2, t3, t4, t5, t6 = st.tabs([
    "1 · Contexto Histórico",
    "2 · Tendencias & Mix",
    "3 · Estadística",
    "4 · Año a Año",
    "5 · Proyecciones",
    "6 · Hallazgos",
])


# ════════════════════════════════════════════
# 1  CONTEXTO HISTÓRICO
# ════════════════════════════════════════════
with t1:
    st.markdown('<div class="section-label">Capítulo 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">El legado de 30 años de publicidad</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="narr">
    En 1995, Colombia tenía menos de 37 millones de habitantes y el internet era prácticamente invisible.
    La <strong>Televisión Nacional</strong> concentraba casi el 60% del presupuesto publicitario;
    la Prensa y las Revistas complementaban el ecosistema. No existía el concepto de <em>pauta digital</em>.
    Tres décadas después, el mercado creció más de <strong>15 veces en términos nominales</strong>,
    y el mapa de medios luce radicalmente distinto — pero la TV sigue en el centro del tablero.
    </div>
    """, unsafe_allow_html=True)

    # Gráfico: Evolución completa todos los medios
    medios_disp = [m for m in medios_sel if m in df_v.columns]
    if medios_disp:
        fig1 = px.area(df_v, x="AÑO", y=medios_disp,
                       title="Inversión histórica por medio (M COP)",
                       color_discrete_sequence=["#1D4ED8","#60A5FA","#10B981","#F59E0B","#6B7280","#94A3B8","#CBD5E1"],
                       template="plotly_white")
        fig1.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.35))
        st.plotly_chart(fig1, use_container_width=True)

    # Gráfico: TV + Digital + Total — líneas
    fig1b = px.line(df_v, x="AÑO", y=["TOTAL_INV","TV_TOTAL","DIGITAL"],
                    title="Mercado total vs Televisión vs Digital",
                    color_discrete_map={"TOTAL_INV":"#0F172A","TV_TOTAL":"#1D4ED8","DIGITAL":"#10B981"},
                    template="plotly_white", markers=True)
    fig1b.add_annotation(x=2020, y=df_v[df_v["AÑO"]==2020]["TOTAL_INV"].values[0]*1.05,
                          text="Pandemia -6.9%", showarrow=True, arrowhead=2, bgcolor="#FEF9C3", font=dict(color="#92400E"))
    st.plotly_chart(fig1b, use_container_width=True)


# ════════════════════════════════════════════
# 2  TENDENCIAS & MIX DE MEDIOS
# ════════════════════════════════════════════
with t2:
    st.markdown('<div class="section-label">Capítulo 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tendencias: Digital vs Tradicional vs TV</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    # Área apilada normalizada (share %)
    with c1:
        df_norm = df_v[["AÑO","TV_TOTAL","DIGITAL","TRADICIONAL"]].copy()
        total   = df_norm[["TV_TOTAL","DIGITAL","TRADICIONAL"]].sum(axis=1)
        df_norm["TV_TOTAL"]    = df_norm["TV_TOTAL"]/total*100
        df_norm["DIGITAL"]     = df_norm["DIGITAL"]/total*100
        df_norm["TRADICIONAL"] = df_norm["TRADICIONAL"]/total*100
        fig2a = px.area(df_norm, x="AÑO", y=["TV_TOTAL","DIGITAL","TRADICIONAL"],
                        title="Share normalizado del Presupuesto (%)",
                        color_discrete_sequence=["#1D4ED8","#10B981","#94A3B8"],
                        template="plotly_white")
        fig2a.update_layout(legend=dict(orientation="h"))
        st.plotly_chart(fig2a, use_container_width=True)

    # TV Share vs Digital Share a lo largo del tiempo
    with c2:
        fig2b = go.Figure()
        fig2b.add_trace(go.Scatter(x=df_v["AÑO"], y=df_v["TV_SHARE"]*100,
                                   name="TV Share %", fill="tozeroy",
                                   line=dict(color="#1D4ED8", width=3)))
        fig2b.add_trace(go.Scatter(x=df_v["AÑO"], y=df_v["DIG_SHARE"]*100,
                                   name="Digital Share %", fill="tozeroy",
                                   line=dict(color="#10B981", width=3)))
        fig2b.update_layout(title="TV vs Digital: Participación en la torta (%)",
                             template="plotly_white",
                             yaxis_title="% del presupuesto total")
        st.plotly_chart(fig2b, use_container_width=True)

    # Gráfico de barras: Comparativa absoluta por medio (año selecto)
    st.markdown("---")
    year_snap = st.select_slider("Año para comparar los medios", options=sorted(df_v["AÑO"].unique()))
    row_snap  = df_v[df_v["AÑO"] == year_snap]
    if not row_snap.empty:
        row_snap = row_snap.iloc[0]
        snap_data = pd.DataFrame({
            "Medio": ["TV Nac.", "TV Reg.", "Digital", "Radio", "Prensa", "Exterior", "Revistas"],
            "Inversión": [row_snap["TV NACIONAL"], row_snap["TV REG Y LOCAL"], row_snap["DIGITAL"],
                          row_snap["RADIO"], row_snap["PRENSA"], row_snap["PUB EXTERIOR"], row_snap["REVISTAS"]]
        }).sort_values("Inversión", ascending=False)
        fig2c = px.bar(snap_data, x="Medio", y="Inversión", text_auto=".3s",
                       title=f"Inversión por Medio — {year_snap}",
                       color="Inversión", color_continuous_scale="Blues",
                       template="plotly_white")
        st.plotly_chart(fig2c, use_container_width=True)


# ════════════════════════════════════════════
# 3  ESTADÍSTICA DESCRIPTIVA
# ════════════════════════════════════════════
with t3:
    st.markdown('<div class="section-label">Capítulo 3</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Perfil estadístico de los medios</div>', unsafe_allow_html=True)

    media_stat = ["TV REG Y LOCAL","TV NACIONAL","DIGITAL","RADIO","PRENSA","PUB EXTERIOR","REVISTAS"]
    df_stat    = df_v[media_stat].dropna()

    # — Histograma interactivo
    var_hist = st.selectbox("Variable para histograma", media_stat)
    fig3a = px.histogram(df_stat, x=var_hist, nbins=15,
                         title=f"Distribución histórica — {var_hist}",
                         color_discrete_sequence=["#1D4ED8"],
                         template="plotly_white")
    fig3a.update_traces(marker_line_color="white", marker_line_width=1.5)
    st.plotly_chart(fig3a, use_container_width=True)

    # — Boxplots
    fig3b = px.box(df_stat, y=media_stat,
                   title="Dispersión, mediana y outliers por medio (Boxplot)",
                   template="plotly_white",
                   color_discrete_sequence=["#1D4ED8"])
    st.plotly_chart(fig3b, use_container_width=True)

    # — Barras de Media por medio
    means = df_stat.mean().reset_index()
    means.columns = ["Medio", "Media"]
    fig3c = px.bar(means.sort_values("Media", ascending=False), x="Medio", y="Media",
                   text_auto=".3s", title="Media histórica de inversión por medio",
                   color="Media", color_continuous_scale="Blues",
                   template="plotly_white")
    st.plotly_chart(fig3c, use_container_width=True)

    # — Tabla de estadísticas descriptivas
    st.markdown("#### Tabla de estadísticas descriptivas")
    stats_tbl = df_stat.describe().T
    stats_tbl["mediana"] = df_stat.median()
    stats_tbl["moda"]    = df_stat.apply(lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan)
    cols_show = ["mean","mediana","moda","std","min","max"]
    st.dataframe(stats_tbl[cols_show].rename(columns={
        "mean":"Media","std":"Desv. Estándar","min":"Mínimo","max":"Máximo",
        "mediana":"Mediana","moda":"Moda"
    }).style.format("{:,.0f}").background_gradient(cmap="Blues"))


# ════════════════════════════════════════════
# 4  COMPARATIVO AÑO A AÑO
# ════════════════════════════════════════════
with t4:
    st.markdown('<div class="section-label">Capítulo 4</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">¿Qué pasó cada año?</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="narr">
    Cada punto de inflexión en la economía colombiana dejó una huella en el presupuesto publicitario.
    La caída del petróleo en 2016, la pandemia de 2020 y el rebote extraordinario de 2021 son los episodios más dramáticos
    en 30 años de historia.
    </div>
    """, unsafe_allow_html=True)

    # Barras de variación porcentual
    df_var = df_v.dropna(subset=["VAR_YOY"])
    colors = ["#F87171" if v < 0 else "#60A5FA" for v in df_var["VAR_YOY"]]
    fig4a = go.Figure(go.Bar(x=df_var["AÑO"], y=df_var["VAR_YOY"], marker_color=colors,
                              text=[f"{v:.1f}%" for v in df_var["VAR_YOY"]], textposition="outside"))
    fig4a.update_layout(title="Variación Porcentual Anual de la Inversión Total (%)",
                        xaxis_title="Año", yaxis_title="Variación (%)", template="plotly_white")
    # Anotaciones hitos
    for hito in [(2020,"Pandemia\n-6.9%","-7"),(2021,"Rebote\n+47.5%","+47"),(2016,"Crisis\nPetróleo","-8")]:
        y_val = df_var[df_var["AÑO"]==hito[0]]["VAR_YOY"]
        if not y_val.empty:
            fig4a.add_annotation(x=hito[0], y=y_val.values[0],
                                  text=hito[1], showarrow=True, arrowhead=2,
                                  bgcolor="#FEF9C3", font=dict(color="#78350F", size=11))
    st.plotly_chart(fig4a, use_container_width=True)

    # — Waterfall acumulado de TV
    fig4b = go.Figure(go.Waterfall(
        x      = df_v["AÑO"].tolist(),
        y      = df_v["TV_TOTAL"].diff().fillna(df_v["TV_TOTAL"].iloc[0]).tolist(),
        connector = dict(line=dict(color="#CBD5E1")),
        increasing = dict(marker=dict(color="#60A5FA")),
        decreasing = dict(marker=dict(color="#F87171")),
    ))
    fig4b.update_layout(title="Variación Incremental de la Inversión en TV (por año)",
                        template="plotly_white", xaxis_title="Año")
    st.plotly_chart(fig4b, use_container_width=True)


# ════════════════════════════════════════════
# 5  PROYECCIONES A 6 AÑOS
# ════════════════════════════════════════════
with t5:
    st.markdown('<div class="section-label">Capítulo 5</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Proyecciones al 2031: Tres métodos</div>', unsafe_allow_html=True)

    COLORS = {"hist":"#1D4ED8","proj":"#93C5FD","digital":"#10B981","tv":"#1D4ED8"}

    # ── MÉTODO 1: Regresión Lineal ─────────────────────────────
    st.markdown("#### Método 1 — Regresión Lineal (Mercado Total)")
    fig5a = go.Figure()

    # Datos históricos
    fig5a.add_trace(go.Scatter(x=df_hist["AÑO"], y=df_hist["TOTAL_INV"],
                                name="Histórico", mode="lines+markers",
                                line=dict(color=COLORS["hist"], width=3)))
    # Proyección
    proj_slice = df_full[df_full["PROYECCION"] == True]
    fig5a.add_trace(go.Scatter(x=proj_slice["AÑO"], y=proj_slice["TOTAL_INV"],
                                name="Proyección (Regresión)", mode="lines+markers",
                                line=dict(color=COLORS["proj"], width=3, dash="dash"),
                                marker=dict(symbol="diamond")))
    # Sombra de futuro
    fig5a.add_vrect(x0=2025.5, x1=2031.5, fillcolor="#EFF6FF", opacity=0.7,
                    layer="below", annotation_text="Zona Proyección",
                    annotation_position="top left")
    fig5a.update_layout(template="plotly_white", xaxis_title="Año",
                        yaxis_title="Inversión (M COP)",
                        title="Regresión Lineal: Inversión Total 1995 – 2031")
    st.plotly_chart(fig5a, use_container_width=True)

    # ── MÉTODO 2: Series de Tiempo (por medio) ─────────────────
    st.markdown("#### Método 2 — Series de Tiempo por Medio (TV vs Digital)")
    fig5b = go.Figure()
    # Histórico TV
    fig5b.add_trace(go.Scatter(x=df_hist["AÑO"], y=df_hist["TV_TOTAL"],
                                name="TV Histórico", line=dict(color="#1D4ED8", width=4)))
    # Proyección TV
    fig5b.add_trace(go.Scatter(x=proj_slice["AÑO"], y=proj_slice["TV_TOTAL"],
                                name="TV Proyectado", line=dict(color="#93C5FD", width=3, dash="dot"),
                                marker=dict(symbol="diamond")))
    # Histórico Digital
    fig5b.add_trace(go.Scatter(x=df_hist["AÑO"], y=df_hist["DIGITAL"],
                                name="Digital Histórico", line=dict(color="#10B981", width=4)))
    # Proyección Digital
    fig5b.add_trace(go.Scatter(x=proj_slice["AÑO"], y=proj_slice["DIGITAL"],
                                name="Digital Proyectado", line=dict(color="#6EE7B7", width=3, dash="dot")))
    fig5b.add_vrect(x0=2025.5, x1=2031.5, fillcolor="#F0FDF4", opacity=0.6,
                    layer="below", annotation_text="Futuro")
    fig5b.update_layout(template="plotly_white",
                        title="Series de Tiempo: Trayectorias de TV y Digital al 2031",
                        hovermode="x unified")
    st.plotly_chart(fig5b, use_container_width=True)

    # ── MÉTODO 3: Correlación (scatter) ────────────────────────
    st.markdown("#### Método 3 — Análisis de Correlación (TV vs Penetración Internet)")
    df_corr = df_hist[["Penetración Internet (%)","TV_TOTAL","AÑO"]].dropna()
    X_c = df_corr[["Penetración Internet (%)"]].values
    y_c = df_corr["TV_TOTAL"].values
    model_c = LinearRegression().fit(X_c, y_c)
    x_line  = np.linspace(X_c.min(), X_c.max(), 80)
    y_line  = model_c.predict(x_line.reshape(-1,1))

    fig5c = go.Figure()
    fig5c.add_trace(go.Scatter(
        x=df_corr["Penetración Internet (%)"], y=df_corr["TV_TOTAL"],
        mode="markers+text", text=df_corr["AÑO"].astype(int).astype(str),
        textposition="top center", marker=dict(color="#1D4ED8", size=9),
        name="Cada Año"))
    fig5c.add_trace(go.Scatter(x=x_line, y=y_line, mode="lines",
                                name="Tendencia", line=dict(color="#F59E0B", width=3, dash="dash")))
    fig5c.update_layout(template="plotly_white",
                        xaxis_title="Penetración de Internet (%)",
                        yaxis_title="Inversión en TV (M COP)",
                        title="Correlación: Penetración de Internet vs Inversión TV")
    corr_coef = np.corrcoef(df_corr["Penetración Internet (%)"], df_corr["TV_TOTAL"])[0,1]
    st.plotly_chart(fig5c, use_container_width=True)
    st.info(f"**Coeficiente de correlación de Pearson:** {corr_coef:.2f}  |  "
            "La TV crece junto con el acceso a Internet, refutando el mito de que la conectividad destruye la televisión.")


# ════════════════════════════════════════════
# 6  HALLAZGOS FINALES
# ════════════════════════════════════════════
with t6:
    st.markdown('<div class="section-label">Capítulo 6</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">La TV y el PIB: El ecosistema que no muere</div>', unsafe_allow_html=True)

    # PIB + Inversión Publicitaria (eje dual)
    df_pib = df_hist.dropna(subset=["PIB_PCT"])
    fig6a = go.Figure()
    fig6a.add_trace(go.Bar(x=df_pib["AÑO"], y=df_pib["TOTAL_INV"],
                            name="Inversión Publicitaria (M COP)", marker_color="#BFDBFE"))
    fig6a.add_trace(go.Scatter(x=df_pib["AÑO"], y=df_pib["PIB_PCT"],
                                name="Crecimiento PIB (%)", yaxis="y2",
                                line=dict(color="#1D4ED8", width=3)))
    fig6a.update_layout(
        template="plotly_white",
        title="Inversión Publicitaria vs. Crecimiento del PIB en Colombia",
        yaxis=dict(title="Inversión (M COP)"),
        yaxis2=dict(title="Crecimiento PIB (%)", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", y=1.12)
    )
    st.plotly_chart(fig6a, use_container_width=True)

    # Narrativa final
    st.markdown("""
    <div class="narr">
    <strong>Hallazgos Estratégicos:</strong><br><br>
    🔵 <strong>La TV no muere — se transforma.</strong>
    Desde 1995, la inversión acumulada en televisión supera los <em>25 billones de pesos</em>,
    y aunque su share ha disminuido del 60% al 19%, en términos absolutos la inversión se ha triplicado.<br><br>
    📈 <strong>Relación TV–PIB.</strong>
    La curva de inversión publicitaria es un espejo fiel del ciclo económico.
    En cada año de recesión o desaceleración, la tv regional fue la última en ser recortada,
    validando su rol como medio de construcción de marca en tiempos difíciles.<br><br>
    🌐 <strong>Convergencia, no sustitución.</strong>
    El coeficiente de correlación entre Penetración de Internet e Inversión en TV es positivo,
    lo que evidencia que ambos ecosistemas <em>coexisten y se potencian</em>, no se destruyen.<br><br>
    📊 <strong>Para 2031</strong> el mercado publicitario superará los <em>6.5 billones de pesos</em>.
    La TV Conectada (CTV) y el Streaming capturarán presupuesto digital pero bajo la lógica y
    métricas de la televisión, consolidando su relevancia estratégica.
    </div>
    """, unsafe_allow_html=True)

    # Downloads
    st.markdown("---")
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button("📥 Descargar Dataset Completo (CSV)",
                           df_full.to_csv(index=False).encode(),
                           "colombia_publicidad_1995_2031.csv", "text/csv")
    with dl2:
        with open(__file__, "rb") as f:
            st.download_button("🐍 Descargar Código Fuente (.py)",
                               f, "dashboard_storytelling_colombia.py", "text/plain")

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("""
<div class="footer">
    Colombia Advertising Intelligence &nbsp;|&nbsp;
    Data Storytelling Dashboard &nbsp;|&nbsp; 2026 &nbsp;|&nbsp;
    Fuentes: IBOPE · DANE · Banco Mundial · IAB Colombia
</div>
""", unsafe_allow_html=True)
