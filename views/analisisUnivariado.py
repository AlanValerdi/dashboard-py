# import streamlit as st
# import seaborn as sns
# import matplotlib.pyplot as plt

# def renderUnivariateFullAnalysis(data):
#     df_sp = data["df"]
#     df_mx = data["dfMx"]

#     st.title("Análisis Univariado Completo")

#     st.markdown("""
#     Este análisis muestra cómo se distribuyen las variables principales de forma individual para cada país.
#     Incluye tanto variables categóricas como numéricas discretizadas o suavizadas.
#     """)

#     # ---------- Variables categóricas ----------
#     cat_vars = {
#         "Tipo de habitación": "room_type",
#         "Tipo de propiedad": "property_type",
#         "Es superhost": "host_is_superhost",
#         "Identidad verificada": "host_identity_verified"
#     }

#     for title, col in cat_vars.items():
#         st.subheader(f"Distribución de: {title}")
#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown("**España**")
#             fig_sp, ax_sp = plt.subplots()
#             sns.countplot(x=df_sp[col], palette="Greens_r", ax=ax_sp)
#             ax_sp.set_xticklabels(ax_sp.get_xticklabels(), rotation=45)
#             st.pyplot(fig_sp)

#         with col2:
#             st.markdown("**México**")
#             fig_mx, ax_mx = plt.subplots()
#             sns.countplot(x=df_mx[col], palette="Oranges_r", ax=ax_mx)
#             ax_mx.set_xticklabels(ax_mx.get_xticklabels(), rotation=45)
#             st.pyplot(fig_mx)

#     st.divider()

#     # ---------- Variables numéricas ----------
#     num_vars = {
#         "Noches mínimas": "minimum_nights",
#         "Disponibilidad (365)": "availability_365",
#         "Precio": "price",
#         "Calificación (rating)": "review_scores_rating"
#     }

#     for title, col in num_vars.items():
#         if col not in df_sp.columns or col not in df_mx.columns:
#             continue  # Salta si no existe en uno de los dataframes

#         st.subheader(f"Distribución de: {title}")
#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown("**España**")
#             fig_sp, ax_sp = plt.subplots()
#             sns.histplot(df_sp[col][df_sp[col] < df_sp[col].quantile(0.95)], kde=True, color="seagreen", ax=ax_sp)
#             st.pyplot(fig_sp)

#         with col2:
#             st.markdown("**México**")
#             fig_mx, ax_mx = plt.subplots()
#             sns.histplot(df_mx[col][df_mx[col] < df_mx[col].quantile(0.95)], kde=True, color="coral", ax=ax_mx)
#             st.pyplot(fig_mx)

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def show(data):
    # Datos
    df = data['df']
    text_cols = list(data['textCols'])

    st.title("📊 Análisis Univariado de Variables Categóricas")
    st.markdown("Esta vista permite explorar tablas y gráficos de frecuencia para variables categóricas.")

    # Función auxiliar para tabla de frecuencia
    def freq_tbl(series: pd.Series) -> pd.DataFrame:
        tbl = series.value_counts(dropna=False).reset_index()
        tbl.columns = [series.name, 'frequency']
        tbl['percentage'] = tbl['frequency'] / tbl['frequency'].sum()
        tbl['cumulative_perc'] = tbl['percentage'].cumsum()
        return tbl

    # Opciones en sidebar
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

    # Recorrer cada variable categórica
    for col in text_cols:
        st.header(f"Variable: {col}")
        tbl = freq_tbl(df[col])
        top_n = 10
        top_tbl = tbl.head(top_n)

        if opcion == "Tablas de Frecuencia":
            st.subheader("Tabla de Frecuencia")
            st.dataframe(top_tbl)

        elif opcion == "Gráficos de Barra":
            st.subheader("Gráfico de Barra")
            fig, ax = plt.subplots()
            sns.barplot(x=top_tbl['frequency'], y=top_tbl[col], palette='viridis', ax=ax)
            ax.set_xlabel("Frecuencia")
            ax.set_ylabel(col)
            st.pyplot(fig)

        elif opcion == "Gráficos de Dispersión":
            st.subheader("Gráfico de Dispersión")
            fig = px.scatter(
                top_tbl,
                x='frequency', y='cumulative_perc',
                labels={'frequency':'Frecuencia', 'cumulative_perc':'% Acumulado'},
                title=f"Frecuencia vs % Acumulado ({col})"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif opcion == "Gráficos de Área":
            st.subheader("Gráfico de Área")
            fig, ax = plt.subplots()
            ax.fill_between(top_tbl.index, top_tbl['frequency'], alpha=0.5)
            ax.plot(top_tbl.index, top_tbl['frequency'])
            ax.set_xticks(top_tbl.index)
            ax.set_xticklabels(top_tbl[col], rotation=45)
            ax.set_ylabel('Frecuencia')
            st.pyplot(fig)

        elif opcion == "Gráficos de Pastel":
            st.subheader("Gráfico de Pastel")
            fig, ax = plt.subplots()
            ax.pie(top_tbl['frequency'], labels=top_tbl[col], autopct="%.1f%%")
            ax.set_title(f"Distribución de {col}")
            st.pyplot(fig)

