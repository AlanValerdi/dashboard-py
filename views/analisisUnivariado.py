import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def show(data):
    st.title("📊 Análisis Univariado de Variables Categóricas")
    st.markdown("Esta vista permite explorar tablas y gráficos de frecuencia para variables categóricas.")

    # Selección de país
    country = st.sidebar.selectbox(
        "País",
        options=["España", "México", "Grecia"],
        format_func=lambda x: x
    )

    # Seleccionar el dataframe correspondiente
    if country == "España":
        df = data['df']
        text_cols = list(data['textCols'])
    elif country == "México":
        df = data['dfMx']
        text_cols = list(data['textColsMx'])
    else:  # Grecia
        df = data['dfGr']
        text_cols = list(data['textColsGr'])

    # Opción de comparación con México
    if country != "México":
        compare_with_mexico = st.sidebar.radio(
            "¿Comparar con México?",
            options=["No", "Sí"],
            horizontal=True
        )
    else:
        compare_with_mexico = "No"

    # Función auxiliar para tabla de frecuencia
    def freq_tbl(series: pd.Series) -> pd.DataFrame:
        tbl = series.value_counts(dropna=False).reset_index()
        tbl.columns = [series.name, 'frequency']
        tbl['percentage'] = tbl['frequency'] / tbl['frequency'].sum()
        tbl['cumulative_perc'] = tbl['percentage'].cumsum()
        return tbl

    # Opciones en sidebar
    st.sidebar.subheader("Selección de Variable")
    selected_col = st.sidebar.selectbox(
        "Variable a analizar",
        options=text_cols,
        format_func=lambda x: x
    )

    opcion = st.sidebar.radio(
        "Selecciona vista:",
        [
            "Tablas de Frecuencia", 
            "Gráficos de Barra", 
            "Gráficos de Dispersión", 
            "Gráficos de Área", 
            "Gráficos de Pastel"
        ]
    )

    # Análisis de la variable seleccionada
    st.header(f"Variable: {selected_col} - {country}")
    tbl = freq_tbl(df[selected_col])
    top_n = 10
    top_tbl = tbl.head(top_n)

    if opcion == "Tablas de Frecuencia":
        st.subheader("Tabla de Frecuencia")
        st.dataframe(top_tbl)

    if compare_with_mexico == "Sí":
        st.subheader("Tabla de Frecuencia - México (Comparación)")
        df_mexico = data['dfMx']
        tbl_mx = freq_tbl(df_mexico[selected_col])
        top_tbl_mx = tbl_mx.head(top_n)
        st.dataframe(top_tbl_mx)

    elif opcion == "Gráficos de Barra":
        st.subheader("Gráfico de Barra")
        fig, ax = plt.subplots()
        sns.barplot(x=top_tbl['frequency'], y=top_tbl[selected_col], palette='viridis', ax=ax)
        ax.set_xlabel("Frecuencia")
        ax.set_ylabel(selected_col)
        st.pyplot(fig)

    if compare_with_mexico == "Sí":
        st.subheader("Gráfico de Barra - México (Comparación)")
        df_mexico = data['dfMx']
        tbl_mx = freq_tbl(df_mexico[selected_col])
        top_tbl_mx = tbl_mx.head(top_n)
        fig_mx, ax_mx = plt.subplots()
        sns.barplot(x=top_tbl_mx['frequency'], y=top_tbl_mx[selected_col], palette='viridis', ax=ax_mx)
        ax_mx.set_xlabel("Frecuencia")
        ax_mx.set_ylabel(selected_col)
        st.pyplot(fig_mx)

    elif opcion == "Gráficos de Dispersión":
        st.subheader("Gráfico de Dispersión")
        fig = px.scatter(
            top_tbl,
            x='frequency', y='cumulative_perc',
            labels={'frequency':'Frecuencia', 'cumulative_perc':'% Acumulado'},
        title=f"Frecuencia vs % Acumulado ({selected_col}) - {country}"
        )
        st.plotly_chart(fig, use_container_width=True)

    if compare_with_mexico == "Sí":
        st.subheader("Gráfico de Dispersión - México (Comparación)")
        df_mexico = data['dfMx']
        tbl_mx = freq_tbl(df_mexico[selected_col])
        top_tbl_mx = tbl_mx.head(top_n)
        fig_mx = px.scatter(
            top_tbl_mx,
            x='frequency', y='cumulative_perc',
            labels={'frequency':'Frecuencia', 'cumulative_perc':'% Acumulado'},
            title=f"Frecuencia vs % Acumulado ({selected_col}) - México"
        )
        st.plotly_chart(fig_mx, use_container_width=True)

    elif opcion == "Gráficos de Área":
        st.subheader("Gráfico de Área")
        fig, ax = plt.subplots()
        ax.fill_between(top_tbl.index, top_tbl['frequency'], alpha=0.5)
        ax.plot(top_tbl.index, top_tbl['frequency'])
        ax.set_xticks(top_tbl.index)
        ax.set_xticklabels(top_tbl[selected_col], rotation=45)
        ax.set_ylabel('Frecuencia')
        ax.set_title(f"Distribución de {selected_col} - {country}")
        st.pyplot(fig)

    if compare_with_mexico == "Sí":
        st.subheader("Gráfico de Área - México (Comparación)")
        df_mexico = data['dfMx']
        tbl_mx = freq_tbl(df_mexico[selected_col])
        top_tbl_mx = tbl_mx.head(top_n)
        fig_mx, ax_mx = plt.subplots()
        ax_mx.fill_between(top_tbl_mx.index, top_tbl_mx['frequency'], alpha=0.5)
        ax_mx.plot(top_tbl_mx.index, top_tbl_mx['frequency'])
        ax_mx.set_xticks(top_tbl_mx.index)
        ax_mx.set_xticklabels(top_tbl_mx[selected_col], rotation=45)
        ax_mx.set_ylabel('Frecuencia')
        ax_mx.set_title(f"Distribución de {selected_col} - México")
        st.pyplot(fig_mx)

    elif opcion == "Gráficos de Pastel":
        st.subheader("Gráfico de Pastel")
        fig, ax = plt.subplots()
        ax.pie(top_tbl['frequency'], labels=top_tbl[selected_col], autopct="%.1f%%")
        ax.set_title(f"Distribución de {selected_col} - {country}")
        st.pyplot(fig)

    if compare_with_mexico == "Sí":
        st.subheader("Gráfico de Pastel - México (Comparación)")
        df_mexico = data['dfMx']
        tbl_mx = freq_tbl(df_mexico[selected_col])
        top_tbl_mx = tbl_mx.head(top_n)
        fig_mx, ax_mx = plt.subplots()
        ax_mx.pie(top_tbl_mx['frequency'], labels=top_tbl_mx[selected_col], autopct="%.1f%%")
        ax_mx.set_title(f"Distribución de {selected_col} - México")
        st.pyplot(fig_mx)

