import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


def show(data):
    st.title("Regresión Lineal Múltiple")
    
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
    check_all = st.sidebar.checkbox("Mapa de calor de todo el DataFrame")
    selected_vars = []
    num_vars = None
    if not check_all:
        st.sidebar.subheader("Variables a seleccionar para el heatmap")
        selected_vars = st.sidebar.multiselect(
            "Variables graficadas", options=numeric_cols
        )
        if selected_vars:
            max_opts = len(numeric_cols)
            min_opts = 2
            num_vars = st.sidebar.selectbox(
                "Número de variables a mostrar", options=list(range(min_opts, max_opts+1))
            )
    plot_heat = st.sidebar.button("Mostrar Mapa de calor")

    if plot_heat:
        if check_all:
            df_plot = numeric_df
        elif selected_vars and num_vars and len(selected_vars) <= num_vars:
            # completar con variables más correlacionadas
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
            st.warning("Selecciona variables válidas antes de generar el heatmap.")
            return

        st.subheader(f"Mapa de calor - {country}")
        n = df_plot.shape[1]
        tick_fs = int(np.interp(n, [5, 30], [14, 6]))
        annot_fs = int(np.interp(n, [5, 30], [14, 6]))
        corr_mat = df_plot.corr()
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            corr_mat,
            cmap="coolwarm",
            annot=True,
            fmt=".2f",
            annot_kws={"size": annot_fs},
            linewidths=0.5,
            square=True,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        plt.xticks(rotation=90, fontsize=tick_fs)
        plt.yticks(rotation=0, fontsize=tick_fs)
        st.pyplot(fig)

        # Mostrar mapa de calor de México si se seleccionó comparación
        if compare_with_mexico == "Sí":
            st.subheader("Mapa de calor - México (Comparación)")
            df_mexico = data['numericDfMx']
            df_plot_mx = df_mexico[df_plot.columns]
            corr_mat_mx = df_plot_mx.corr()
            fig_mx, ax_mx = plt.subplots(figsize=(12, 10))
            sns.heatmap(
                corr_mat_mx,
                cmap="coolwarm",
                annot=True,
                fmt=".2f",
                annot_kws={"size": annot_fs},
                linewidths=0.5,
                square=True,
                cbar_kws={"shrink": 0.8},
                ax=ax_mx
            )
            plt.xticks(rotation=90, fontsize=tick_fs)
            plt.yticks(rotation=0, fontsize=tick_fs)
            st.pyplot(fig_mx)

    # --- Múltiple Regresión ---
    st.sidebar.subheader("Selección de variables para Regresión")
    dep_var = st.sidebar.selectbox("Variable dependiente", options=numeric_cols)
    indep_opts = [c for c in numeric_cols if c != dep_var]
    indep_vars = st.sidebar.multiselect(
        "Variables independientes", options=indep_opts, default=indep_opts[:1]
    )
    if not indep_vars:
        st.warning("Selecciona al menos una variable independiente.")
        return
    if len(indep_vars) > 5:
        st.sidebar.warning("Máximo 5 variables independientes.")
        return
    
    comparative_table = st.sidebar.checkbox("Mostrar tabla comparativa")
    run_model = st.sidebar.button("Mostrar Regresión")

    # Si no ejecuta regresión, mostrar scatter con trendline
    if not run_model:
        df_melt = pd.melt(
            numeric_df,
            id_vars=[dep_var],
            value_vars=indep_vars,
            var_name="Variable independiente",
            value_name="Valor"
        )
        st.subheader(f"Dispersión vs {dep_var} - {country}")
        fig_scatter = px.scatter(
            df_melt,
            x="Valor",
            y=dep_var,
            color="Variable independiente",
            trendline="ols",
            labels={"Valor": "Valor variable independiente"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Mostrar scatter de México si se seleccionó comparación
        if compare_with_mexico == "Sí":
            st.subheader(f"Dispersión vs {dep_var} - México (Comparación)")
            df_mexico = data['numericDfMx']
            df_melt_mx = pd.melt(
                df_mexico,
                id_vars=[dep_var],
                value_vars=indep_vars,
                var_name="Variable independiente",
                value_name="Valor"
            )
            fig_scatter_mx = px.scatter(
                df_melt_mx,
                x="Valor",
                y=dep_var,
                color="Variable independiente",
                trendline="ols",
                labels={"Valor": "Valor variable independiente"}
            )
            st.plotly_chart(fig_scatter_mx, use_container_width=True)
        return

    # Ejecutar regresión múltiple para el país seleccionado
    X = numeric_df[indep_vars]
    y = numeric_df[[dep_var]]
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = model.score(X, y)
    r = np.sqrt(r2)

    st.subheader(f"Resultados del Modelo - {country}")
    #st.write(f"**Variable dependiente:** {dep_var}")
    #st.write(f"**Variables independientes:** {indep_vars}")
    #st.write(f"Coeficiente de determinación (R²): {r2:.3f}")
    #st.write(f"Coeficiente de correlación (R): {r:.3f}")

    # Comparación real vs predicho
    numeric_df[f"pred_{dep_var}"] = y_pred
    if comparative_table:
        st.subheader("Tabla comparativa Real vs Predicho")
        st.dataframe(numeric_df[[dep_var, f"pred_{dep_var}"]].head(10))

    st.subheader("Gráfico comparativo")
    fig_comp = go.Figure()
    var0 = indep_vars[0]
    fig_comp.add_trace(go.Scatter(
        x=numeric_df[var0],
        y=numeric_df[dep_var],
        mode='markers',
        name='Real',
        marker=dict(color='blue')
    ))
    fig_comp.add_trace(go.Scatter(
        x=numeric_df[var0],
        y=numeric_df[f"pred_{dep_var}"],
        mode='markers',
        name='Predicho',
        marker=dict(color='red')
    ))
    fig_comp.update_layout(
        title=f"Real vs Predicho de {dep_var} - {country}",
        xaxis_title=var0,
        yaxis_title=dep_var
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    
    st.write(f"Coeficiente de determinación (R²): {r2:.3f}")
    st.write(f"Coeficiente de correlación (R): {r:.3f}")
    
    # Cleanup
    numeric_df.drop(columns=[f"pred_{dep_var}"], inplace=True)

    # Mostrar comparación con México si se seleccionó
    if compare_with_mexico == "Sí":
        # Ejecutar regresión múltiple para México
        df_mexico = data['numericDfMx']
        X_mx = df_mexico[indep_vars]
        y_mx = df_mexico[[dep_var]]
        model_mx = LinearRegression()
        model_mx.fit(X_mx, y_mx)
        y_pred_mx = model_mx.predict(X_mx)
        r2_mx = model_mx.score(X_mx, y_mx)
        r_mx = np.sqrt(r2_mx)

        st.subheader("Resultados del Modelo - México (Comparación)")
        #st.write(f"**Variable dependiente:** {dep_var}")
        #st.write(f"**Variables independientes:** {indep_vars}")
        #st.write(f"Coeficiente de determinación (R²): {r2_mx:.3f}")
        #st.write(f"Coeficiente de correlación (R): {r_mx:.3f}")

        # Comparación real vs predicho México
        df_mexico[f"pred_{dep_var}"] = y_pred_mx
        if comparative_table:
            st.subheader("Tabla comparativa Real vs Predicho - México")
            st.dataframe(df_mexico[[dep_var, f"pred_{dep_var}"]].head(10))

        st.subheader("Gráfico comparativo - México")
        fig_comp_mx = go.Figure()
        fig_comp_mx.add_trace(go.Scatter(
            x=df_mexico[var0],
            y=df_mexico[dep_var],
            mode='markers',
            name='Real',
            marker=dict(color='blue')
        ))
        fig_comp_mx.add_trace(go.Scatter(
            x=df_mexico[var0],
            y=df_mexico[f"pred_{dep_var}"],
            mode='markers',
            name='Predicho',
            marker=dict(color='red')
        ))
        fig_comp_mx.update_layout(
            title=f"Real vs Predicho de {dep_var} - México",
            xaxis_title=var0,
            yaxis_title=dep_var
        )
        st.plotly_chart(fig_comp_mx, use_container_width=True)
        
        st.write(f"Coeficiente de determinación (R²): {r2_mx:.3f}")
        st.write(f"Coeficiente de correlación (R): {r_mx:.3f}")
        
        # Cleanup
        df_mexico.drop(columns=[f"pred_{dep_var}"], inplace=True)
