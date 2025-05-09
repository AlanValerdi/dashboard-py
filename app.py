# Creamos el archivo de la APP en el intreprete principal py

# Importar las librerias
import streamlit as st 
import plotly.express as px
import pandas as pd
import streamlit_shadcn_ui as ui
from actions.dataLoadAction import loadData
import streamlit as st
from views.generalAnalysis import renderGeneralAnalysis
from views.dichotomicAnalysis import renderDichotomicAnalysis
from views import FirstAnalysis
from views import vistaProperty
from views import vistaRoom
from views import minimumNight
from views import analisisUnivariado
from views import regresionLogistica
from views import regresionLogisticaMultiple
from views import mapaDeResidencias
from views import datosGenerales
import streamlit_shadcn_ui as ui
import altair as alt

#definir la instancia

st.set_page_config(
    page_title="Airbnb Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

alt.themes.enable("dark")

data = loadData()

# Logo Airbnb desde URL
logo_url = "https://bigcleanswitch.org/wp-content/uploads/2019/08/190806-Airbnb-Logo-White.png"

# Estilo CSS para fondo y texto de la sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #FF5A5F;
        color: white;
        text-align: center;
        align-items: center;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5 {
        color: white;
    }
    .center-logo {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# Mostrar logo y título en la sidebar
with st.sidebar:
    st.markdown(f"<div class='center-logo'><img src='{logo_url}' width='120'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:white; font-size:40px'>Airbnb Dashboard</h1>", unsafe_allow_html=True)
    page = st.sidebar.selectbox("Seleccionar Pagina", ["Introduction", "Spain vs Mexico", "Analisis de noches por room_type", "Analisis Univariado", "regresionLogistica", "regresionLogisticaMultiple", "Mapa de residencias", "datosGenerales"])


# Main View
if page == "Introduction":
    FirstAnalysis.show(data)
elif page == "Spain vs Mexico":
    vistaProperty.show(data)
elif page == "Analisis de noches por room_type":
    minimumNight.renderMinimumNightsAnalysis(data)
elif page == "Analisis Univariado":
    analisisUnivariado.show(data)
elif page == "regresionLogistica":
    regresionLogistica.show(data)
elif page == "regresionLogisticaMultiple":
    regresionLogisticaMultiple.show(data)
elif page == "Mapa de residencias":
    mapaDeResidencias.show(data)
