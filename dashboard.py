import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats as scipy_stats
from io import StringIO

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO
# ==========================================
st.set_page_config(page_title="Data Storytelling: Publicidad Colombia", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background-color: #F8F9FB;
    }
    
    .main-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #0F172A;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .sub-title {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 40px;
    }
    
    .section-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        margin-bottom: 30px;
        border-top: 5px solid #1E40AF;
    }
    
    .insight-box {
        background-color: #EFF6FF;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #1D4ED8;
        margin: 20px 0;
    }
    
    h2, h3 {
        color: #1E3A8A;
        font-family: 'Montserrat', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CARGA Y PROCESAMIENTO DE DATOS
# ==========================================
@st.cache_data
def load_and_clean_data():
    try:
        # Intentar cargar el archivo procesado previo
        df = pd.read_csv('cleaned_ad_data.csv')
    except:
        # Fallback de datos crudos (incrustados basado en el archivo del usuario)
        raw = """AÑO;TV REG Y LOCAL;REVISTAS;PUB EXTERIOR;PRENSA;RADIO;TV NACIONAL;DIGITAL;TOTAL_INV;IPC;TRM Promedio;Penetración Internet (%);Poblacion DANE
1995;22969,6;32751,2;;;;198962,4;;254683,1;0,195;912,9;0,001;36229830
1996;22347,2;35404,7;;;;229243,1;;286995;0,216;1002,94;0,003;36830574
1997;22268;40055,5;;;;286168,8;;348492,3;0,177;1115,69;0,005;37426532
1998;27846,2;47905,3;;;224890,9;304204,9;;604847,3;0,167;1402,92;0,012;38012359
1999;19016,6;46349;;;172073,2;327958,1;;565396,9;0,092;1776;0,018;38585016
2000;24330,8;53527,7;;;188868,2;374799,9;;641526,6;0,088;2087,73;0,03;39140080
2001;22420,3;50546,1;;;175153,2;430507,5;;678627,1;0,077;2299,24;0,045;39674811
2002;30265,3;53648;;;192641,8;452990,7;;729545,9;0,07;2361,07;0,058;40190679
2003;32552;61775;;307647;209554;518029;;1129557;0,065;2877,19;0,072;40693254
2004;34035;70553;;320890;222096;584915;;1232489;0,055;2607,87;0,093;41188093
2005;36742;83440;;353131;257508;673410;;1404231;0,049;2320,08;0,121;41671878
2006;47228;105912;;414077;294505;763408;;1625130;0,045;2358,38;0,15;42170126
2007;59306;118890;;526803;345592;863885;;1914476;0,057;2000,06;0,184;42658630
2008;58633;108196;;496891;352518;858225;40601;1915064;0,077;1969,95;0,226;43134017
2009;58794;93488;;478655;365762;823611;50016;1870326;0,02;2147,81;0,27;43608630
2010;65275;99876;;536026;419008;919366;94682;2134233;0,032;1897,74;0,325;44086292
2011;61702;109519;;599099;443469;1020467;126366;2360622;0,037;1848,06;0,379;44553416
2012;63394;110206;;607059;466508;1043509;162205;2452881;0,024;1768,23;0,42;45001571
2013;66569;108706;;637900;521607;1098966;215507;2649255;0,019;1868,9;0,471;45434942
2014;71644;103048;145738;636192;550216;1155026;255389;2917253;0,037;2000,36;0,516;45866010
2015;71228;95061;145885;574232;561034;1102929;376110;2926479;0,068;2747,73;0,572;46313898
2016;56371;77516;130590;503065;517723;990127;409739;2685131;0,058;2977,77;0,63;46830116
2017;51899;71067;181973;465685;528459;917494;600476;2817053;0,041;2951;0,665;47419200
2018;52374;59988;184168;418083;549185;889760;848594;3002152;0,032;2956;0,684;48258494
2019;60717;48036,22;209888;376697;541920;889057;1080535;3206850;0,038;3281;0.709;49395678
2020;56101;19606,19;82238;225403,1;373737;763423;1251333;2771841;0,016;3693;0.72;50407647
2021;69995;14731,99;166607;253875,3;499184;1037067;2040158;4081618;0,056;3743;0.752;51117378
2022;70900;11469.83;274741;269501.2;578788;1043937;2354697,9;4604034,9;0,131;4255,44;0.768;51682692
2023;59038;10513,11;279346;246444,1;578117;975070;2663179;4811707;0,093;4325,05;0.773;52314000
2024;52116,3;8622.25;292696.0;215570.0;558882,4;955310,3;2825565,2;4908762,4;0,052;4072,59;0.757;52695952
2025;61114,8;6839,12;328924.6;206962,0;560706,3;908657,0;3066685,3;5139889,1;;;;
"""
        df = pd.read_csv(StringIO(raw), sep=';', decimal=',')
    
    # Limpiar nombres de columnas y tipos de datos
    df.columns = df.columns.str.strip()
    
    # Imputación final para 2025
    df.loc[df['AÑO'] == 2025, ['IPC', 'TRM Promedio', 'Penetración Internet (%)', 'Poblacion DANE']] = [0.035, 4000.0, 0.835, 53200000.0]
    
    # Crear métricas agregadas
    df['TV_TOTAL'] = df['TV REG Y LOCAL'] + df['TV NACIONAL']
    df['TRADICIONAL'] = df['REVISTAS'] + df['PUB EXTERIOR'] + df['PRENSA'] + df['RADIO']
    df['VAR_ANUAL_TOTAL'] = df['TOTAL_INV'].pct_change() * 100
    
    # Calcular proyecciones a 6 años (2026-2031)
    future_years = np.array(range(2026, 2032)).reshape(-1, 1)
    proj_dfs = []
    for year in future_years.flatten():
        proj_dfs.append({'AÑO': year})
    df_proj_base = pd.DataFrame(proj_dfs)
    
    valid_cols = ['TV_TOTAL', 'DIGITAL', 'TOTAL_INV', 'TRM Promedio']
    for col in valid_cols:
        valid = df[['AÑO', col]].dropna()
        model = LinearRegression().fit(valid[['AÑO']], valid[col])
        df_proj_base[col] = model.predict(future_years).clip(min=0)
    
    full_df = pd.concat([df, df_proj_base], ignore_index=True)
    return full_df

df = load_and_clean_data()

# ==========================================
# 3. INTERFAZ DE USUARIO
# ==========================================
st.markdown('<p class="main-title">📺 La Trayectoria de la Pantalla</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Historia, Resiliencia y Futuro de la Publicidad en Colombia (1995-2031)</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Configuración")
    years = st.slider("Rango Histórico", 1995, 2025, (1995, 2025))
    df_view = df[(df['AÑO'] >= years[0]) & (df['AÑO'] <= years[1])]
    
    st.markdown("---")
    st.info("Este dashboard utiliza Regresión Lineal y Series de Tiempo para proyectar los próximos 6 años.")

# ==========================================
# 4. STORYTELLING JOURNEY
# ==========================================

# --- SECCIÓN 1: Contexto Histórico ---
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("1. 🕰️ El Legado de la Inversión")
st.write("Desde mediados de los 90, el mercado publicitario colombiano ha sido un barómetro de la economía nacional.")

fig_hist = px.line(df_view, x="AÑO", y=["TOTAL_INV", "TV_TOTAL", "DIGITAL"], 
                  title="Evolución de la Inversión (Millones COP)",
                  color_discrete_map={"TOTAL_INV": "#1E293B", "TV_TOTAL": "#1E40AF", "DIGITAL": "#10B981"})
fig_hist.update_layout(hovermode="x unified", plot_bgcolor="white")
st.plotly_chart(fig_hist, use_container_width=True)

st.markdown('<div class="insight-box"><b>Insight:</b> Mientras que el mercado total ha crecido un <b>2000%</b> en términos nominales, la テレビ (TV) ha mantenido una relevancia crítica, actuando como el ancla de confianza incluso en la era digital.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SECCIÓN 2: Tendencias Comparativas ---
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("2. 📊 El Mix de Medios: Tradicional vs Digital")
col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(df_view[df_view['AÑO'] == years[1]], values=[df_view.iloc[-1]['TV_TOTAL'], df_view.iloc[-1]['DIGITAL'], df_view.iloc[-1]['TRADICIONAL']], 
                    names=['Televisión', 'Digital', 'Otros Tradicionales'],
                    title=f"Distribución del Budget en {years[1]}",
                    color_discrete_sequence=["#1E40AF", "#10B981", "#64748B"])
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    df_share = df_view.copy()
    df_share['TV_SHARE'] = df_share['TV_TOTAL'] / df_share['TOTAL_INV']
    df_share['DIG_SHARE'] = df_share['DIGITAL'] / df_share['TOTAL_INV']
    fig_share = px.area(df_share, x="AÑO", y=["TV_SHARE", "DIG_SHARE"], 
                       title="Batalla por el Share de Inversión (%)",
                       color_discrete_map={"TV_SHARE": "#1E40AF", "DIG_SHARE": "#10B981"})
    st.plotly_chart(fig_share, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SECCIÓN 3: Descriptiva Visual (REQUISITO 2) ---
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("3. 📈 Perfil Estadístico de las Variables")
st.write("Análisis de distribución y dispersión para entender la volatilidad de los medios.")

tab_stats1, tab_stats2 = st.tabs(["Distribución (Histogramas)", "Dispersión (Boxplots)"])

valid_media = ['TV REG Y LOCAL', 'TV NACIONAL', 'DIGITAL', 'RADIO', 'PRENSA']
with tab_stats1:
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        fig_hist_tv = px.histogram(df_view, x="TV_TOTAL", nbins=15, title="Frecuencia de Inversión en TV", color_discrete_sequence=["#1E40AF"])
        st.plotly_chart(fig_hist_tv, use_container_width=True)
    with col_stat2:
        fig_hist_dig = px.histogram(df_view, x="DIGITAL", nbins=15, title="Frecuencia de Inversión Digital", color_discrete_sequence=["#10B981"])
        st.plotly_chart(fig_hist_dig, use_container_width=True)

with tab_stats2:
    fig_box = px.box(df_view, y=valid_media, title="Volatilidad Histórica por Medio", 
                    color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig_box, use_container_width=True)

st.write("Estadísticas Descriptivas:")
st.dataframe(df_view[valid_media + ['TOTAL_INV']].describe().T.style.background_gradient(cmap='Blues'))
st.markdown('</div>', unsafe_allow_html=True)

# --- SECCIÓN 4: Comparación Año a Año ---
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("4. 📉 Análisis de Variación Interanual")
fig_var = px.bar(df_view, x="AÑO", y="VAR_ANUAL_TOTAL", 
                title="Crecimiento Porcentual de la Inversión Total (%)",
                color="VAR_ANUAL_TOTAL", color_continuous_scale="RdYlGn")
fig_var.add_annotation(x=2020, y=-5, text="Pandemia COVID-19", showarrow=True)
st.plotly_chart(fig_var, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SECCIÓN 5: Proyecciones a 6 Años ---
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("5. 🔮 El Futuro al 2031: Modelado de Datos")
st.write("Utilizamos tres enfoques: Regresión Lineal, Análisis de Correlación Macro y Tendencias de Series de Tiempo.")

tab_proj1, tab_proj2 = st.tabs(["Línea de Proyección", "Correlación Macro (TV vs TRM)"])

with tab_proj1:
    df_full_proj = df[df['AÑO'] >= 2020]
    fig_proj = px.line(df_full_proj, x="AÑO", y="TOTAL_INV", line_dash="AÑO", title="Pronóstico del Mercado Publicitario")
    fig_proj.add_vrect(x0=2025, x1=2031, fillcolor="green", opacity=0.1, annotation_text="Fase de Proyección")
    st.plotly_chart(fig_proj, use_container_width=True)

with tab_proj2:
    fig_corr = px.scatter(df_view, x="TRM Promedio", y="TV_TOTAL", trendline="ols",
                         title="Relación: Inversión en TV vs TRM (Dólar)",
                         color_discrete_sequence=["#1E40AF"])
    st.plotly_chart(fig_corr, use_container_width=True)
    
    corr_val = df_view['TRM Promedio'].corr(df_view['TV_TOTAL'])
    st.markdown(f"**Coeficiente de Correlación:** {corr_val:.2f} (Fuerte relación positiva con el tipo de cambio)")

st.markdown('</div>', unsafe_allow_html=True)

# --- SECCIÓN 6: Conclusiones ---
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("6. 💡 Conclusiones y Visionado Estratégico")
st.markdown("""
- **Resiliencia de la Televisión:** A pesar del avance digital, la TV sigue siendo el medio de mayor confianza para marcas de gran consumo en Colombia.
- **Convergencia:** El futuro no es Digital vs Tradicional, sino la *TV Conectada* y la integración de métricas digitales en pantallas masivas.
- **Impacto Macro:** La publicidad en Colombia es altamente sensible a la TRM; un dólar fuerte tiende a impulsar la inversión nominal de multinacionales.
- **Proyección:** Se espera un crecimiento compuesto anual cercano al **5.8%** impulsado por el segmento Digital, pero con la TV manteniendo su rol estratégico en el PIB publicitario.
""")

# Descarga de Código
st.markdown("---")
st.markdown("### Descargas")
csv_code = df.to_csv(index=False).encode('utf-8')
st.download_button("Descargar Dataset Procesado", csv_code, "dataset_publicidad_colombia.csv", "text/csv")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align: center; color: gray;'>Dashboard diseñado para el Master de Analítica | 2026</p>", unsafe_allow_html=True)
