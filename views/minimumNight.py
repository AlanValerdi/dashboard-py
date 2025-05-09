import streamlit as st
import pandas as pd

def renderMinimumNightsAnalysis(data):
    df_spain = data["df"]
    df_mexico = data["dfMx"]

    st.title("Análisis de Noches Mínimas por Tipo de Habitación 🌑")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🇪🇸España - Promedio de Noches Mínimas por Tipo de Cuarto")
        spain_table = df_spain.groupby("room_type")["minimum_nights"].mean().reset_index().sort_values(by="minimum_nights", ascending=False)
        spain_table.columns = ["Tipo de cuarto", "Promedio de noches mínimas"]
        st.table(spain_table)

    with col2:
        st.subheader("🇲🇽México - Promedio de Noches Mínimas por Tipo de Cuarto")
        mexico_table = df_mexico.groupby("room_type")["minimum_nights"].mean().reset_index().sort_values(by="minimum_nights", ascending=False)
        mexico_table.columns = ["Tipo de cuarto", "Promedio de noches mínimas"]
        st.table(mexico_table)

    st.markdown("---")

    # Insight adicional (opcional)
    st.subheader("Comparación de Noches Mínimas entre México y España por Tipo de Cuarto")

    # Merge de ambas tablas para comparación
    merged = pd.merge(
        spain_table,
        mexico_table,
        on="Tipo de cuarto",
        suffixes=("_España", "_México")
    )
    merged["Diferencia (Esp - Mx)"] = merged["Promedio de noches mínimas_España"] - merged["Promedio de noches mínimas_México"]
    st.table(merged)
