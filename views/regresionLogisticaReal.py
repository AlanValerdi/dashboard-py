import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score
import streamlit_shadcn_ui as ui

def show(data):
    st.title("Regresión Logística")
    
    # Sidebar controls for country visibility
    st.sidebar.subheader("Mostrar países")
    show_spain = st.sidebar.checkbox("🇪🇸 España", value=True)
    show_mexico = st.sidebar.checkbox("🇲🇽 México", value=True)
    show_greece = st.sidebar.checkbox("🇬🇷 Grecia", value=True)

    # Universal controls in sidebar
    st.sidebar.subheader("Configuración del Modelo")
    
    # Get all possible binary columns from any country
    binary_cols = ['host_is_superhost', 'host_identity_verified']
    dependent_variable = st.sidebar.selectbox(
        "Variable dependiente",
        options=binary_cols
    )
    
    # Get all possible numeric columns from visible countries
    all_numeric_cols = set()
    if show_spain:
        all_numeric_cols.update(data['numericCols'])
    if show_mexico:
        all_numeric_cols.update(data['numericColsMx'])
    if show_greece:
        all_numeric_cols.update(data['numericColsGr'])
    
    independent_option = [var for var in all_numeric_cols if var != dependent_variable]
    independent_variables = st.sidebar.multiselect(
        "Variables independientes",
        options=independent_option,
        default=independent_option[:1] if independent_option else None
    )
    
    # Validate independent variables selection
    if not independent_variables:
        st.warning("Por favor selecciona al menos una variable independiente.")
        return
    
    # Replace radio buttons with checkboxes
    st.sidebar.subheader("Selecciona opciones a mostrar:")
    show_prediction = st.sidebar.checkbox("📊 Predicción", value=True)
    show_confusion = st.sidebar.checkbox("🎯 Matriz de Confusión")
    show_metrics = st.sidebar.checkbox("📈 Métricas del modelo")

    # Function to run logistic regression for a country
    def run_logistic_regression(numeric_df, binary_df, country_name, country_emoji):
        st.subheader(f"Regresión Logística - {country_emoji} {country_name}")
        
        # Filter numeric columns to only include selected ones that exist in this country
        available_vars = [var for var in independent_variables if var in numeric_df.columns]
        if not available_vars:
            st.warning(f"No hay variables independientes disponibles para {country_name}")
            return
            
        varsIndep = numeric_df[available_vars]
        varDep = binary_df[[dependent_variable]]
        
        X = varsIndep 
        y = varDep
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=None)
        
        escalar = StandardScaler()
        X_train = escalar.fit_transform(X_train)
        X_test = escalar.transform(X_test)
        
        modelo = LogisticRegression()
        modelo.fit(X_train, y_train)
        
        # Predecir
        y_pred = modelo.predict(X_test)
        y_proba = modelo.predict_proba(X_test)
        
        if show_prediction:
            st.write("### 📊 Predicciones del modelo")
            pred_df = X_test.copy()
            pred_df = pd.DataFrame(pred_df, columns=available_vars)
            pred_df["Probabilidad False"] = y_proba[:, 0]
            pred_df["Probabilidad True"] = y_proba[:, 1]
            pred_df["Predicción"] = y_pred
            st.dataframe(pred_df.head(10))  # Mostrar primeras 10 filas
            
        if show_confusion:
            st.write("### 🎯 Matriz de confusión")
            matriz = confusion_matrix(y_test, y_pred)
            st.write(pd.DataFrame(matriz, index=["Positivo", "Negativo"], columns=["Predicho 0", "Predicho 1"]))
            
        if show_metrics:
            st.write("### 📈 Métricas del Modelo")
            
            # Precisión
            precision_true = precision_score(y_test, y_pred, average="binary", pos_label="t")
            precision_false = precision_score(y_test, y_pred, average="binary", pos_label="f")
            
            # Exactitud
            exactitud = accuracy_score(y_test, y_pred)
            
            # Sensibilidad
            sensibilidad_true = recall_score(y_test, y_pred, average="binary", pos_label="t")
            sensibilidad_false = recall_score(y_test, y_pred, average="binary", pos_label="f")

            # Create metrics cards
            col1, col2 = st.columns(2)
            
            with col1:
                ui.metric_card(
                    title="Precisión (True)",
                    content=f"{precision_true:.4f}",
                    description="Precisión para la clase True"
                )
                ui.metric_card(
                    title="Precisión (False)",
                    content=f"{precision_false:.4f}",
                    description="Precisión para la clase False"
                )
                ui.metric_card(
                    title="Exactitud",
                    content=f"{exactitud:.4f}",
                    description="Exactitud general del modelo"
                )
            
            with col2:
                ui.metric_card(
                    title="Sensibilidad (True)",
                    content=f"{sensibilidad_true:.4f}",
                    description="Sensibilidad para la clase True"
                )
                ui.metric_card(
                    title="Sensibilidad (False)",
                    content=f"{sensibilidad_false:.4f}",
                    description="Sensibilidad para la clase False"
                )

    # Create three columns for the countries
    col1, col2, col3 = st.columns(3)

    # Spain
    if show_spain:
        with col1:
            run_logistic_regression(
                data['numericDf'],
                data['df'][['host_is_superhost', 'host_identity_verified']],
                "España",
                "🇪🇸"
            )

    # Mexico
    if show_mexico:
        with col2:
            run_logistic_regression(
                data['numericDfMx'],
                data['dfMx'][['host_is_superhost', 'host_identity_verified']],
                "México",
                "🇲🇽"
            )

    # Greece
    if show_greece:
        with col3:
            run_logistic_regression(
                data['numericDfGr'],
                data['dfGr'][['host_is_superhost', 'host_identity_verified']],
                "Grecia",
                "🇬🇷"
            )