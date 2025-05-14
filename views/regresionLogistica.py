# views/simpleRegression.py
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


def show(data):
    st.title("📈 Regresión Lineal Simple")
    
    # Selección de país
    country = st.sidebar.selectbox(
        "País",
        options=["España", "México", "Grecia"],
        format_func=lambda x: x
    )

    # Seleccionar el dataframe correspondiente
    if country == "España":
        numeric_df = data['numericDf']
        numeric_cols = list(data['numericCols'])
    elif country == "México":
        numeric_df = data['numericDfMx']
        numeric_cols = list(data['numericColsMx'])
    else:  # Grecia
        numeric_df = data['numericDfGr']
        numeric_cols = list(data['numericColsGr'])

    # Opción de comparación con México
    if country != "México":
        compare_with_mexico = st.sidebar.radio(
            "¿Comparar con México?",
            options=["No", "Sí"],
            horizontal=True
        )
    else:
        compare_with_mexico = "No"

    st.sidebar.header("Opciones de Mapa de Calor")

    # --- Heatmap ---
    show_all = st.sidebar.checkbox("Mapa de calor de todo el DataFrame")
    selected_vars = []
    num_vars = None
    if not show_all:
        st.sidebar.subheader("Selecciona variables para el heatmap")
        selected_vars = st.sidebar.multiselect("Variables gráficas", options=numeric_cols)
        if selected_vars:
            min_sel = 2 if len(selected_vars) == 1 else len(selected_vars)
            max_sel = len(numeric_cols)
            if min_sel > max_sel:
                st.sidebar.warning("Rango inválido de variables.")
            else:
                num_vars = st.sidebar.selectbox("Número de variables a mostrar", options=list(range(min_sel, max_sel + 1)))
    plot_heat = st.sidebar.button("Mostrar Mapa de calor")

    if plot_heat:
        if show_all:
            df_plot = numeric_df
        elif selected_vars:
            if len(selected_vars) == num_vars:
                df_plot = numeric_df[selected_vars]
            else:
                corr = numeric_df.corr().abs()
                already = set(selected_vars)
                candidates = (
                    corr[selected_vars]
                    .mean(axis=1)
                    .sort_values(ascending=False)
                    .drop(labels=already, errors='ignore')
                )
                extra = list(candidates.head(num_vars - len(selected_vars)).index)
                df_plot = numeric_df[selected_vars + extra]
        else:
            st.warning("Selecciona al menos una variable.")
            return

        st.subheader(f"Mapa de calor - {country}")
        n = df_plot.shape[1]
        tick_size = int(np.interp(n, [5, 30], [14, 6]))
        annot_size = int(np.interp(n, [5, 30], [14, 6]))
        corr_mat = df_plot.corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            corr_mat,
            cmap="coolwarm",
            annot=True,
            fmt=".2f",
            annot_kws={"size": annot_size},
            linewidths=0.5,
            square=True,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        plt.xticks(rotation=90, fontsize=tick_size)
        plt.yticks(rotation=0, fontsize=tick_size)
        st.pyplot(fig)

        # Mostrar mapa de calor de México si se seleccionó comparación
        if compare_with_mexico == "Sí":
            st.subheader("Mapa de calor - México (Comparación)")
            df_mexico = data['numericDfMx']
            df_plot_mx = df_mexico[df_plot.columns]
            corr_mat_mx = df_plot_mx.corr()
            fig_mx, ax_mx = plt.subplots(figsize=(10, 8))
            sns.heatmap(
                corr_mat_mx,
                cmap="coolwarm",
                annot=True,
                fmt=".2f",
                annot_kws={"size": annot_size},
                linewidths=0.5,
                square=True,
                cbar_kws={"shrink": 0.8},
                ax=ax_mx
            )
            plt.xticks(rotation=90, fontsize=tick_size)
            plt.yticks(rotation=0, fontsize=tick_size)
            st.pyplot(fig_mx)

    # --- Selección de variables para regresión simple ---
    st.sidebar.subheader("Selección de regresión simple")
    dep_var = st.sidebar.selectbox("Variable dependiente", options=numeric_cols)
    indep_opts = [c for c in numeric_cols if c != dep_var]
    indep_var = st.sidebar.selectbox("Variable independiente", options=indep_opts)

    run_reg = st.sidebar.button("Mostrar Regresión Lineal Simple")

    if not run_reg and not plot_heat:
        # Scatter simple
        if indep_var == dep_var:
            st.warning("Variable independiente igual a dependiente.")
        else:
            st.subheader(f"Dispersión: {indep_var} vs {dep_var} - {country}")
            fig_scatter = px.scatter(numeric_df, x=indep_var, y=dep_var)
            st.plotly_chart(fig_scatter, use_container_width=True)

            # Mostrar scatter de México si se seleccionó comparación
            if compare_with_mexico == "Sí":
                st.subheader(f"Dispersión: {indep_var} vs {dep_var} - México (Comparación)")
                df_mexico = data['numericDfMx']
                fig_scatter_mx = px.scatter(df_mexico, x=indep_var, y=dep_var)
                st.plotly_chart(fig_scatter_mx, use_container_width=True)
        return

    if run_reg:
        if indep_var == dep_var:
            st.warning("Variable independiente igual a dependiente.")
            return

        # Datos modelo para el país seleccionado
        X = numeric_df[[indep_var]]
        y = numeric_df[[dep_var]]
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        r2 = model.score(X, y)
        r = np.sqrt(r2)

        st.subheader(f"Resultados del Modelo - {country}")
        st.write(f"**Dependiente:** {dep_var}")
        st.write(f"**Independiente:** {indep_var}")
        st.write(f"R²: {r2:.3f}, R: {r:.3f}")

        # Tabla comparativa
        numeric_df[f"pred_{dep_var}"] = y_pred
        st.subheader("Real vs Predicho")
        st.dataframe(numeric_df[[dep_var, f"pred_{dep_var}" ]].head(10))

        # Gráfico comparativo
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Scatter(x=numeric_df[indep_var], y=numeric_df[dep_var], mode='markers', name='Real', marker=dict(color='blue')))
        fig_comp.add_trace(go.Scatter(x=numeric_df[indep_var], y=numeric_df[f"pred_{dep_var}"], mode='markers', name='Predicho', marker=dict(color='red')))
        fig_comp.update_layout(title=f"{dep_var} Real vs Predicho - {country}", xaxis_title=indep_var, yaxis_title=dep_var)
        st.plotly_chart(fig_comp, use_container_width=True)

        # Limpieza
        numeric_df.drop(columns=[f"pred_{dep_var}"], inplace=True)

        # Mostrar comparación con México si se seleccionó
        if compare_with_mexico == "Sí":
            # Datos modelo para México
            df_mexico = data['numericDfMx']
            X_mx = df_mexico[[indep_var]]
            y_mx = df_mexico[[dep_var]]
            model_mx = LinearRegression()
            model_mx.fit(X_mx, y_mx)
            y_pred_mx = model_mx.predict(X_mx)
            r2_mx = model_mx.score(X_mx, y_mx)
            r_mx = np.sqrt(r2_mx)

            st.subheader("Resultados del Modelo - México (Comparación)")
            st.write(f"**Dependiente:** {dep_var}")
            st.write(f"**Independiente:** {indep_var}")
            st.write(f"R²: {r2_mx:.3f}, R: {r_mx:.3f}")

            # Tabla comparativa México
            df_mexico[f"pred_{dep_var}"] = y_pred_mx
            st.subheader("Real vs Predicho - México")
            st.dataframe(df_mexico[[dep_var, f"pred_{dep_var}" ]].head(10))

            # Gráfico comparativo México
            fig_comp_mx = go.Figure()
            fig_comp_mx.add_trace(go.Scatter(x=df_mexico[indep_var], y=df_mexico[dep_var], mode='markers', name='Real', marker=dict(color='blue')))
            fig_comp_mx.add_trace(go.Scatter(x=df_mexico[indep_var], y=df_mexico[f"pred_{dep_var}"], mode='markers', name='Predicho', marker=dict(color='red')))
            fig_comp_mx.update_layout(title=f"{dep_var} Real vs Predicho - México", xaxis_title=indep_var, yaxis_title=dep_var)
            st.plotly_chart(fig_comp_mx, use_container_width=True)

            # Limpieza
            df_mexico.drop(columns=[f"pred_{dep_var}"], inplace=True)

