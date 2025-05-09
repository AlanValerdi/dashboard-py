# views/roomTypeAnalysis.py
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit_shadcn_ui as ui
import pandas as pd
import numpy as np
import altair as alt

def show(data):
    df_spain = data["df"]
    df_mex = data["dfMx"]

    

    col1, col2, col3 = st.columns([1.5, 3, 2], gap="large")

    with col1:
        st.subheader("📌 Datos clave por tipo de cuarto")
        top_room_spain = df_spain["room_type"].value_counts().idxmax()
        top_room_mex = df_mex["room_type"].value_counts().idxmax()

        avg_price_spain = df_spain.groupby("room_type")["price"].mean().sort_values(ascending=False)
        avg_price_mex = df_mex.groupby("room_type")["price"].mean().sort_values(ascending=False)

        ui.metric_card("Tipo de cuarto más común (España)", top_room_spain)
        ui.metric_card("Tipo de cuarto más común (México)", top_room_mex)
        ui.metric_card("Tipo de cuarto más caro (España)", avg_price_spain.index[0] + f" - {avg_price_spain.iloc[0]:.2f}€")
        ui.metric_card("Tipo de cuarto más caro (México)", avg_price_mex.index[0] + f" - {avg_price_mex.iloc[0]:.2f}€")

        st.divider()

        st.markdown("💡 *Los tipos de cuarto más caros no siempre son los más comunes. Esto puede influir en la percepción de valor.*")

    # En col2: Predicción lineal
    with col2:
        # Asumiendo que ya tienes cargado df_spain y df_mex
        df_spain["pais"] = "España"
        df_mex["pais"] = "México"

        # Usamos head(1000) para rendimiento
        df_spain_sample = df_spain.head(1000)
        df_mex_sample = df_mex.head(1000)

        st.subheader("📈 Predicción lineal por país (Precio vs Reviews por mes)")

        # Gráfica para España
        st.markdown("### 🇪🇸 España")
        scatter_spain = alt.Chart(df_spain_sample).mark_circle(size=60).encode(
            x=alt.X("reviews_per_month", title="Reviews por mes"),
            y=alt.Y("price", title="Precio"),
            color=alt.Color("room_type", title="Tipo de cuarto"),
            tooltip=["room_type", "price", "reviews_per_month"]
        )

        # Línea de regresión
        regression_spain = scatter_spain.transform_regression(
            "reviews_per_month", "price", method="linear"
        ).mark_line(color="red").encode()

        st.altair_chart(scatter_spain + regression_spain, use_container_width=True)

        # Gráfica para México
        st.markdown("### 🇲🇽 México")
        scatter_mex = alt.Chart(df_mex_sample).mark_circle(size=60).encode(
            x=alt.X("reviews_per_month", title="Reviews por mes"),
            y=alt.Y("price", title="Precio"),
            color=alt.Color("room_type", title="Tipo de cuarto"),
            tooltip=["room_type", "price", "reviews_per_month"]
        )

        regression_mex = scatter_mex.transform_regression(
            "reviews_per_month", "price", method="linear"
        ).mark_line(color="red").encode()

        st.altair_chart(scatter_mex + regression_mex, use_container_width=True)


    # En col3: Distribución
    with col3:
        st.subheader("📊 Distribución por tipo de cuarto")
        tab = st.radio("Selecciona país", ["España", "México"], horizontal=True)

        df_selected = df_spain if tab == "España" else df_mex
        df_selected = df_selected.head(100)  # Limitar los datos cargados

        fig, axs = plt.subplots(2, 1, figsize=(8, 6))
        sns.histplot(data=df_selected, x="price", hue="room_type", multiple="stack", ax=axs[0])
        axs[0].set_title("Distribución de precios por tipo de cuarto")
        sns.histplot(data=df_selected, x="number_of_reviews", hue="room_type", multiple="stack", ax=axs[1])
        axs[1].set_title("Distribución de reviews por tipo de cuarto")
        plt.tight_layout()
        st.pyplot(fig)
