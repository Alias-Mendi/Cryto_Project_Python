import streamlit as st
import pandas as pd
import krakenex
from Clase import Dataset, Grafico  # Asegúrate de tener las clases actualizadas
import plotly.express as px
import plotly.graph_objects as go
import dotenv
import os

# Configuración de la página al inicio
st.set_page_config(page_title="Kraken Visualizer", layout="wide", initial_sidebar_state="expanded")

# Aplicar estilo minimalista y modo oscuro utilizando CSS
st.markdown("""
    <style>
    body {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        background-color: #121212;  /* Fondo oscuro */
        color: #E0E0E0;  /* Texto claro */
    }
    .css-18e3th9 {
        padding: 20px;
    }
    .css-1lcbmhc {
        background-color: #1E1E1E !important;  /* Fondo de los cuadros */
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .css-1d391kg {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .stButton button {
        background-color: #BB86FC;  /* Color pastel púrpura para el botón */
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #9B70D0;  /* Color pastel más oscuro al hacer hover */
    }
    .css-1aumxhk {  /* Sidebar */
        background-color: #1E1E1E;  /* Fondo oscuro */
        color: #E0E0E0;  /* Texto claro */
    }
    .st-expander {
        background-color: #1E1E1E !important;  /* Fondo oscuro del expander */
    }
    .st-expander .stButton button {
        background-color: #BB86FC;
        color: white;
    }
    h1, h3, h4, h5 {
        color: #BB86FC;  /* Títulos en púrpura pastel */
    }

    /* Spinner personalizado */
    .stSpinner > div > div {
        border-top-color: #BB86FC !important;  /* Cambia el color de la rueda de carga */
        border-right-color: #BB86FC !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación con estilo minimalista
st.markdown("<h1 style='text-align: center; color: #BB86FC;'>Visualización de Precios de Activos en Kraken</h1>", unsafe_allow_html=True)

# Conectar a la API de Kraken
dotenv.load_dotenv()
k = krakenex.API(os.getenv('KRAKEN_KEY'))

# Inicializar el estado de la sesión
if 'data' not in st.session_state:
    st.session_state['data'] = None

# Función para obtener datos
@st.cache_data
def fetch_data(pair):
    pair_mapping = {
        "BTC/USD": 'XXBTZUSD',
        "ETH/USD": 'XETHZUSD',
        "ETH/BTC": 'XETHXXBT',
        "ADA/USD": 'ADAUSD',
        "DOT/USD": 'DOTUSD',
        "SOL/USD": 'SOLUSD',
        "XRP/USD": 'XXRPZUSD',
        "LTC/USD": 'XLTCZUSD'
    }
    # Realizar la consulta a la API de Kraken
    data = k.query_public('OHLC', {'pair': pair_mapping[pair], 'interval': 60})
    datos = data['result'][pair_mapping[pair]]
    # Procesar los datos con la clase Dataset
    df = Dataset(datos)
    df.get_metrics()
    return df.data

# Barra lateral con diseño estético minimalista
st.sidebar.markdown("<h3 style='color: #BB86FC;'>Controles</h3>", unsafe_allow_html=True)

# Selector de par de monedas
pair = st.sidebar.selectbox(
    "Selecciona la moneda que quieres representar",
    ["BTC/USD", "ETH/USD", "ETH/BTC", "ADA/USD", "DOT/USD", "SOL/USD", "XRP/USD", "LTC/USD"]
)

# Botón para obtener datos y graficar
if st.sidebar.button('Obtener datos'):
    try:
        # Mostrar mensaje de carga mientras se obtiene el gráfico
        with st.spinner("Obteniendo datos..."):
            st.session_state['data'] = fetch_data(pair)
            st.session_state['pair'] = pair
        st.success('Datos obtenidos exitosamente.')
    except Exception as e:
        st.error(f"Ocurrió un error al obtener los datos: {e}")

# Mostrar datos y gráficos si los datos están disponibles
if st.session_state['data'] is not None:
    # Mostrar datos en un expansor
    with st.expander("Mostrar datos en bruto", expanded=False):  # Mantenemos este menú colapsado por defecto
        st.write(st.session_state['data'].head(200))

    # Crear instancia de la clase Grafico
    grafico = Grafico(st.session_state['data'], st.session_state['pair'])

    st.subheader('Gráficos')

    # Opciones de gráficos en la barra lateral
    st.sidebar.markdown("<h4 style='color: #BB86FC;'>Opciones de gráficos</h4>", unsafe_allow_html=True)
    show_lineplot = st.sidebar.checkbox('Gráfico de líneas')
    show_lineplot_volume = st.sidebar.checkbox('Gráfico de líneas con volumen')
    show_candlestick = st.sidebar.checkbox('Gráfico de velas')
    show_candlestick_volume = st.sidebar.checkbox('Gráfico de velas con volumen')

    # Botón para generar los gráficos
    if st.sidebar.button('Generar gráficos'):
        if show_lineplot:
            with st.spinner("Generando gráfico de líneas..."):  # Mostrar spinner mientras se carga el gráfico
                fig = grafico.lineplot()  # Obtener la figura de la clase Grafico
                st.pyplot(fig)  # Mostrar la figura directamente en Streamlit

        if show_lineplot_volume:
            with st.spinner("Generando gráfico de líneas con volumen..."):  # Mostrar spinner mientras se carga el gráfico
                fig = grafico.lineplot_with_volume()  # Obtener la figura de la clase Grafico
                st.pyplot(fig)  # Mostrar la figura directamente en Streamlit

        if show_candlestick:
            with st.spinner("Generando gráfico de velas..."):  # Mostrar spinner mientras se carga el gráfico
                fig = grafico.candlestick()  # Obtener la figura de la clase Grafico
                st.pyplot(fig)  # Mostrar la figura directamente en Streamlit

        if show_candlestick_volume:
            with st.spinner("Generando gráfico de velas con volumen..."):  # Mostrar spinner mientras se carga el gráfico
                fig = grafico.candlestick_with_volume()  # Obtener la figura de la clase Grafico
                st.pyplot(fig)  # Mostrar la figura directamente en Streamlit
else:
    st.info('Selecciona un par de monedas y presiona "Obtener datos" en la barra lateral.')
