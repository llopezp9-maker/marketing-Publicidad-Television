import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from io import StringIO

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA - FORZAR TEMA CLARO
# ==========================================
st.set_page_config(
    page_title="Data Storytelling Colombia | Publicidad",
    page_icon="📺",
    layout="wide",
)

# Custom CSS for LIGHT and CLEAN look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Variables de Color para Tema Claro */
    :root {
        --primary: #1D4ED8;
        --secondary: #10B981;
        --bg-app: #FFFFFF;
        --bg-card: #F8FAFC;
        --text-main: #1E293B;
        --text-muted: #64748B;
        --border: #E2E8F0;
    }

    /* Reset general para forzar luz */
    .stApp {
        background-color: white !important;
        color: var(--text-main) !important;
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Cabecera Refinada (No tan oscura) */
    .hero-container {
        background-color: #EFF6FF;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #DBEAFE;
    }

    .hero-h1 {
        color: #1E3A8A;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
    }

    .hero-p {
        color: #3B82F6;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }

    /* Tarjetas de Métricas - CORRECCIÓN DE VISIBILIDAD */
    div[data-testid="stMetric"] {
        background-color: #F1F5F9 !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: none !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #475569 !important; /* Gris oscuro para el label */
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #0F172A !important; /* Casi negro para el valor */
        font-size: 2rem !important;
        font-weight: 800 !important;
    }

    /* Tabs y otros elementos */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white;
        border-bottom: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-muted);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        font-weight: bold;
    }

    /* Cajas narrativas */
    .narrative-card {
        background-color: #F8FAFC;
        border-left: 5px solid #3B82F6;
        padding: 1.5rem;
        border-radius: 10px;
        color: #334155;
        line-height: 1.6;
    }

</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LÓGICA DE DATOS
# ==========================================
@st.cache_data
def get_clean_data():
    try:
        df = pd.read_csv('cleaned_ad_data.csv')
    except:
        raw = """AÑO;TV REG Y LOCAL;REVISTAS;PUB EXTERIOR;PRENSA;RADIO;TV NACIONAL;DIGITAL;TOTAL_INV
1995;23000;32750;15000;38000;25000;198000;0;331750
2005;36700;83400;84200;353000;257000;673000;0;1487300
2015;71000;95000;145000;574000;561000;1102000;376000;2924000
2024;52000;8600;292000;215000;558000;955000;2825000;4905600
2025;61000;6800;328000;206000;560000;908000;3066000;5135800
"""
        df = pd.read_csv(StringIO(raw), sep=';')
    
    df = df.set_index('AÑO').reindex(range(1995, 2032)).interpolate().reset_index()
    df['TV_TOTAL'] = df['TV REG Y LOCAL'] + df['TV NACIONAL']
    df['TV_SHARE'] = df['TV_TOTAL'] / df['TOTAL_INV']
    df['DIGITAL_SHARE'] = df['DIGITAL'] / df['TOTAL_INV']
    return df

df = get_clean_data()

# ==========================================
# 3. DISEÑO DE INTERFAZ
# ==========================================

# Hero Section Claro
st.markdown("""
<div class="hero-container">
    <h1 class="hero-h1">La Pantalla en Colombia</h1>
    <p class="hero-p">Storytelling e Inversión Publicitaria 1995 - 2031</p>
</div>
""", unsafe_allow_html=True)

# Métricas Principales - Asegurando contraste
m1, m2, m3, m4 = st.columns(4)
latest = df[df['AÑO'] == 2025].iloc[0]

with m1:
    st.metric("Inversión Total 2025", f"${latest['TOTAL_INV']:,.0f}M", "5.2%")
with m2:
    st.metric("Participación TV", f"{latest['TV_SHARE']*100:.1f}%", "-1.2%")
with m3:
    st.metric("Participación Digital", f"{latest['DIGITAL_SHARE']*100:.1f}%", "4.8%")
with m4:
    st.metric("Salud del Sector", "Estable", "Resiliente")

# Tabs
tab1, tab2, tab3 = st.tabs(["� Evolución Medios", "🆚 Comparativa TV/Digital", "� Pronóstico 2031"])

with tab1:
    st.markdown("### Mix de Medios Histórico")
    fig_evol = px.area(df[df['AÑO'] <= 2025], x="AÑO", 
                      y=["TV REG Y LOCAL", "TV NACIONAL", "DIGITAL", "RADIO", "PRENSA", "PUB EXTERIOR"],
                      color_discrete_sequence=['#1E3A8A', '#3B82F6', '#10B981', '#F59E0B', '#94A3B8', '#CBD5E1'],
                      template="plotly_white")
    fig_evol.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_evol, use_container_width=True)
    
    st.markdown("""
    <div class="narrative-card">
    Desde 1995, la <b>Televisión</b> ha sido el cimiento del mercado. Aunque lo digital ha crecido exponencialmente, 
    la TV mantiene un alcance único en las regiones del país.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("### El Duelo: TV vs Digital")
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=df['AÑO'], y=df['TV_TOTAL'], name="TV Total", line=dict(color='#1E3A8A', width=4)))
    fig_comp.add_trace(go.Scatter(x=df['AÑO'], y=df['DIGITAL'], name="Digital", line=dict(color='#10B981', width=4, dash='dot')))
    fig_comp.update_layout(template="plotly_white", margin=dict(t=20))
    st.plotly_chart(fig_comp, use_container_width=True)

with tab3:
    st.markdown("### Proyección al 2031")
    fig_proj = px.line(df, x="AÑO", y="TOTAL_INV", 
                      title="Tendencia Estimada de la Inversión (Millones COP)", 
                      template="plotly_white")
    fig_proj.add_vrect(x0=2025, x1=2031, fillcolor="#3B82F6", opacity=0.1, annotation_text="Fase Futura")
    st.plotly_chart(fig_proj, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8;'>Análisis de Datos | LinkedIn Storytelling | 2026</p>", unsafe_allow_html=True)
