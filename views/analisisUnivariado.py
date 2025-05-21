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
        country_emoji = "🇪🇸"
    elif country == "México":
        df = data['dfMx']
        text_cols = list(data['textColsMx'])
        country_emoji = "🇲🇽"
    else:  # Grecia
        df = data['dfGr']
        text_cols = list(data['textColsGr'])
        country_emoji = "🇬🇷"

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

    # Reemplazar radio buttons con checkboxes
    st.sidebar.subheader("Selecciona tipos de visualización:")
    show_freq_table = st.sidebar.checkbox("Tablas de Frecuencia", value=True)
    show_bar_chart = st.sidebar.checkbox("Gráficos de Barra")
    show_scatter_chart = st.sidebar.checkbox("Gráficos de Dispersión")
    show_area_chart = st.sidebar.checkbox("Gráficos de Área")
    show_pie_chart = st.sidebar.checkbox("Gráficos de Pastel")

    # Análisis de la variable seleccionada
    st.header(f"Variable: {selected_col} - {country_emoji} {country}")
    tbl = freq_tbl(df[selected_col])
    top_n = 10
    top_tbl = tbl.head(top_n)

    # Mostrar todas las visualizaciones seleccionadas
    if show_freq_table:
        st.subheader(f"Tabla de Frecuencia - {country_emoji} {country}")
        st.dataframe(top_tbl)

    if show_bar_chart:
        st.subheader(f"Gráfico de Barra - {country_emoji} {country}")
        fig, ax = plt.subplots()
        sns.barplot(x=top_tbl['frequency'], y=top_tbl[selected_col], palette='viridis', ax=ax)
        ax.set_xlabel("Frecuencia")
        ax.set_ylabel(selected_col)
        st.pyplot(fig)

    if show_scatter_chart:
        st.subheader(f"Gráfico de Dispersión - {country_emoji} {country}")
        fig = px.scatter(
            top_tbl,
            x='frequency', y='cumulative_perc',
            labels={'frequency':'Frecuencia', 'cumulative_perc':'% Acumulado'},
            title=f"Frecuencia vs % Acumulado ({selected_col}) - {country_emoji} {country}"
        )
        st.plotly_chart(fig, use_container_width=True)

    if show_area_chart:
        st.subheader(f"Gráfico de Área - {country_emoji} {country}")
        fig, ax = plt.subplots()
        ax.fill_between(top_tbl.index, top_tbl['frequency'], alpha=0.5)
        ax.plot(top_tbl.index, top_tbl['frequency'])
        ax.set_xticks(top_tbl.index)
        ax.set_xticklabels(top_tbl[selected_col], rotation=45)
        ax.set_ylabel('Frecuencia')
        ax.set_title(f"Distribución de {selected_col} - {country_emoji} {country}")
        st.pyplot(fig)

    if show_pie_chart:
        st.subheader(f"Gráfico de Pastel - {country_emoji} {country}")
        fig, ax = plt.subplots()
        ax.pie(top_tbl['frequency'], labels=top_tbl[selected_col], autopct="%.1f%%")
        ax.set_title(f"Distribución de {selected_col} - {country_emoji} {country}")
        st.pyplot(fig)

    # Mostrar datos de otros países
    other_countries = {
        "España": ("🇪🇸", data['df'], data['textCols']),
        "México": ("🇲🇽", data['dfMx'], data['textColsMx']),
        "Grecia": ("🇬🇷", data['dfGr'], data['textColsGr'])
    }

    for other_country, (emoji, other_df, other_cols) in other_countries.items():
        if other_country != country:
            st.markdown("---")
            st.subheader(f"Comparación con {emoji} {other_country}")
            
            if selected_col in other_cols:
                other_tbl = freq_tbl(other_df[selected_col])
                other_top_tbl = other_tbl.head(top_n)

                if show_freq_table:
                    st.write(f"Tabla de Frecuencia - {emoji} {other_country}")
                    st.dataframe(other_top_tbl)

                if show_bar_chart:
                    st.write(f"Gráfico de Barra - {emoji} {other_country}")
                    fig, ax = plt.subplots()
                    sns.barplot(x=other_top_tbl['frequency'], y=other_top_tbl[selected_col], palette='viridis', ax=ax)
                    ax.set_xlabel("Frecuencia")
                    ax.set_ylabel(selected_col)
                    st.pyplot(fig)

                if show_scatter_chart:
                    st.write(f"Gráfico de Dispersión - {emoji} {other_country}")
                    fig = px.scatter(
                        other_top_tbl,
                        x='frequency', y='cumulative_perc',
                        labels={'frequency':'Frecuencia', 'cumulative_perc':'% Acumulado'},
                        title=f"Frecuencia vs % Acumulado ({selected_col}) - {emoji} {other_country}"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                if show_area_chart:
                    st.write(f"Gráfico de Área - {emoji} {other_country}")
                    fig, ax = plt.subplots()
                    ax.fill_between(other_top_tbl.index, other_top_tbl['frequency'], alpha=0.5)
                    ax.plot(other_top_tbl.index, other_top_tbl['frequency'])
                    ax.set_xticks(other_top_tbl.index)
                    ax.set_xticklabels(other_top_tbl[selected_col], rotation=45)
                    ax.set_ylabel('Frecuencia')
                    ax.set_title(f"Distribución de {selected_col} - {emoji} {other_country}")
                    st.pyplot(fig)

                if show_pie_chart:
                    st.write(f"Gráfico de Pastel - {emoji} {other_country}")
                    fig, ax = plt.subplots()
                    ax.pie(other_top_tbl['frequency'], labels=other_top_tbl[selected_col], autopct="%.1f%%")
                    ax.set_title(f"Distribución de {selected_col} - {emoji} {other_country}")
                    st.pyplot(fig)
            else:
                st.warning(f"La variable {selected_col} no está disponible en los datos de {other_country}")

