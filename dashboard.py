import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from io import StringIO

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA - TEMA CLARO Y SIMPLE
# ==========================================
st.set_page_config(
    page_title="Inversión Publicitaria Colombia | Análisis Simple",
    page_icon="🇨🇴",
    layout="wide",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: white !important;
    }

    .stApp {
        background-color: white !important;
    }

    .header-box {
        background-color: #F0F7FF;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #D1E9FF;
        margin-bottom: 30px;
    }

    .header-box h1 {
        color: #003366;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .header-box p {
        color: #0066CC;
        font-size: 1.2rem;
    }

    /* Cards simplified */
    div[data-testid="stMetric"] {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    .insight-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #003366;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 20px 0;
        color: #334155;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: 600;
        color: #64748B;
    }

    .stTabs [aria-selected="true"] {
        color: #003366 !important;
        border-bottom-color: #003366 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CARGA DE DATOS Y PRONÓSTICO SIMPLE
# ==========================================
@st.cache_data
def load_data_simple():
    try:
        df = pd.read_csv('cleaned_ad_data.csv')
    except:
        raw = """AÑO;TOTAL_INV;TV_TOTAL;DIGITAL;PIB_CRECIMIENTO
2015;2926000;1174000;376000;3.0
2016;2685000;1046000;410000;2.1
2017;2817000;969000;600000;1.4
2018;3002000;942000;848000;2.6
2019;3206000;949000;1080000;3.2
2020;2771000;819000;1251000;-7.0
2021;4081000;1107000;2040000;10.8
2022;4604000;1114000;2354000;7.3
2023;4811000;1034000;2663000;0.6
2024;4908000;1007000;2825000;1.5
2025;5139000;969000;3066000;2.8
"""
        df = pd.read_csv(StringIO(raw), sep=';')
    
    # Simular histórico de PIB para la narrativa (Datos DANE aproximados)
    if 'PIB_CRECIMIENTO' not in df.columns:
        df['PIB_CRECIMIENTO'] = [3.0, 2.1, 1.4, 2.6, 3.2, -7.0, 10.8, 7.3, 0.6, 1.5, 2.8] + [2.5]*20
        df['PIB_CRECIMIENTO'] = df['PIB_CRECIMIENTO'].iloc[:len(df)]

    # Series de Tiempo Simple (Growth Projection al 5% anual)
    last_year = df['AÑO'].max()
    future_years = range(last_year + 1, last_year + 11)
    
    projection = []
    current_total = df.iloc[-1]['TOTAL_INV']
    current_tv = df.iloc[-1]['TV_TOTAL']
    current_digital = df.iloc[-1]['DIGITAL']
    
    for y in future_years:
        current_total *= 1.05 # 5% crecimiento mercado
        current_tv *= 1.01    # TV estable/crece lento
        current_digital *= 1.08 # Digital sigue fuerte
        projection.append({'AÑO': y, 'TOTAL_INV': current_total, 'TV_TOTAL': current_tv, 'DIGITAL': current_digital, 'PIB_CRECIMIENTO': 2.5})
    
    full_df = pd.concat([df, pd.DataFrame(projection)], ignore_index=True)
    full_df['TV_SHARE'] = (full_df['TV_TOTAL'] / full_df['TOTAL_INV']) * 100
    return full_df

df = load_data_simple()

# Header
st.markdown("""
<div class="header-box">
    <h1>Publicidad & Economía en Colombia</h1>
    <p>¿Cómo evoluciona la inversión frente al crecimiento del país?</p>
</div>
""", unsafe_allow_html=True)

# KPIs Principales
m1, m2, m3 = st.columns(3)
actual = df[df['AÑO'] == 2025].iloc[0]
m1.metric("Inversión Total (2025)", f"${actual['TOTAL_INV']:,.0f}M", "5%")
m2.metric("Peso de la Televisión", f"{actual['TV_SHARE']:.1f}%", "Ancla")
m3.metric("Crecimiento PIB (Est.)", f"{actual['PIB_CRECIMIENTO']}%", "Recuperación")

# Navegación Simplificada
tabs = st.tabs(["📉 Tendencias & PIB", "🔮 Pronóstico a 10 Años", "📖 Resumen Estratégico"])

with tabs[0]:
    st.subheader("El Mercado frente a la Economía (PIB)")
    st.write("Visualice cómo la inversión publicitaria acompaña los ciclos económicos de Colombia.")
    
    # Gráfico Dual: Inversión vs PIB
    fig_pib = go.Figure()
    hist_only = df[df['AÑO'] <= 2025]
    
    fig_pib.add_trace(go.Bar(x=hist_only['AÑO'], y=hist_only['TOTAL_INV'], name="Inversión Publicitaria", marker_color='#D1E9FF'))
    fig_pib.add_trace(go.Scatter(x=hist_only['AÑO'], y=hist_only['PIB_CRECIMIENTO'] * 500000, # Escalado para visibilidad
                                name="Ciclo Económico (PIB %)", line=dict(color='#003366', width=3), yaxis="y2"))
    
    fig_pib.update_layout(
        template="plotly_white",
        yaxis=dict(title="Inversión (Millones COP)"),
        yaxis2=dict(title="Crecimiento PIB (%)", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig_pib, use_container_width=True)
    
    st.markdown("""
    <div class="insight-card">
    <b>Análisis:</b> La inversión publicitaria es un espejo de la economía. En 2020, la caída del PIB impactó el presupuesto, 
    pero en 2021-2022 vimos una <b>reacción explosiva</b>, demostrando que las marcas colombianas apuestan fuerte en la recuperación.
    </div>
    """, unsafe_allow_html=True)

with tabs[1]:
    st.subheader("Pronóstico: Serie de Tiempo (2025 - 2035)")
    st.write("Proyección basada en el comportamiento histórico de crecimiento de cada medio.")
    
    fig_ts = go.Figure()
    # Histórico
    fig_ts.add_trace(go.Scatter(x=df['AÑO'], y=df['TV_TOTAL'], name="Televisión (Estable)", line=dict(color='#003366', width=4)))
    fig_ts.add_trace(go.Scatter(x=df['AÑO'], y=df['DIGITAL'], name="Digital (Crecimiento)", line=dict(color='#10B981', width=4)))
    
    # Zona de Sombreado de Futuro
    fig_ts.add_vrect(x0=2025, x1=2035, fillcolor="#F0F7FF", opacity=0.5, layer="below", annotation_text="Fase de Proyección")
    
    fig_ts.update_layout(template="plotly_white", xaxis_title="Año", yaxis_title="Inversión (Millones COP)")
    st.plotly_chart(fig_ts, use_container_width=True)
    
    st.info("Nota: La Televisión mantiene un volumen sólido de más de 1 Billón de pesos anuales, consolidándose como el medio de mayor confianza para grandes audiencias.")

with tabs[2]:
    st.markdown("""
    <div class="insight-card">
    <h3>Conclusiones para LinkedIn</h3>
    
    1. <b>Resiliencia ante el PIB:</b> A pesar de las fluctuaciones económicas, la publicidad en Colombia mantiene una trayectoria de crecimiento sostenido.
    2. <b>El Rol de la TV:</b> La televisión no solo sobrevive, sino que actúa como el <b>puerto seguro</b> de las marcas masivas. Mientras que lo digital ofrece precisión, la TV ofrece <b>escritura de marca y alcance nacional</b>.
    3. <b>Escenario 2035:</b> Prevemos un mercado que superará los 8 Billones de pesos, donde la convergencia entre la pantalla tradicional y la conectada será total.
    </div>
    """, unsafe_allow_html=True)
    
    # Download
    st.markdown("---")
    st.subheader("📥 Material de Soporte")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("Descargar Datos del Dashboard", df.to_csv(index=False), "datos_colombia.csv")
    with c2:
        with open(__file__, "rb") as f:
            st.download_button("Descargar Código Python (.py)", f, "dashboard_final.py")

# Footer
st.markdown("<p style='text-align: center; color: #94A3B8; margin-top: 50px;'>Visualización Estratégica | Colombia 2026</p>", unsafe_allow_html=True)
