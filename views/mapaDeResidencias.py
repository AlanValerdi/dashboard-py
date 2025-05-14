# views/mapResidences.py
import streamlit as st
import plotly.express as px


def show(data):
    # Datos de España, México y Grecia
    df_spain = data['df']
    df_mexico = data['dfMx']
    df_greece = data['dfGr']
    
    st.sidebar.title("Mapa de residencias")
    st.sidebar.markdown("Busca anfitriones según país, tipo de habitación y rango de precio")

    # Selección de país
    country = st.sidebar.selectbox(
        "País",
        options=["España", "México", "Grecia"],
        format_func=lambda x: x
    )

    # Seleccionar el dataframe correspondiente
    if country == "España":
        df = df_spain
    elif country == "México":
        df = df_mexico
    else:
        df = df_greece

    # Selección de tipo de habitación
    room_types = df['room_type'].unique().tolist()
    seleccion = st.sidebar.selectbox("Tipo de habitación", options=room_types)

    # Slider de precio
    min_price = float(df['price'].min())
    max_price = float(df['price'].max())
    precio = st.sidebar.slider(
        "Rango de precio", 
        min_value=min_price, 
        max_value=max_price, 
        value=(min_price, max_price), 
        step=1.0
    )

    # Filtrar dataframe
    df_filtrado = df[
        (df['room_type'] == seleccion) & 
        (df['price'] >= precio[0]) & 
        (df['price'] <= precio[1])
    ]

    st.title(f"Mapa de Alojamientos - {country}")
    st.markdown(f"Mostrando **{len(df_filtrado)}** registros de tipo **{seleccion}** en el rango de precio {precio[0]}–{precio[1]}")

    if df_filtrado.empty:
        st.warning("No se encontraron registros para los filtros seleccionados.")
        return

    # Crear el mapa
    fig = px.scatter_mapbox(
        df_filtrado,
        lat="latitude", lon="longitude",
        color="price", size="price",
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
        zoom=11,
        mapbox_style="carto-positron",
        hover_data={"price": True, "room_type": True, "name": True}
    )
    st.plotly_chart(fig, use_container_width=True)
