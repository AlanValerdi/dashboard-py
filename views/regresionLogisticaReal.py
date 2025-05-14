import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score

def show(data):
    st.title("Regresión Logística")
    
    # Sidebar controls for country visibility
    st.sidebar.subheader("Mostrar países")
    show_spain = st.sidebar.checkbox("España", value=True)
    show_mexico = st.sidebar.checkbox("México", value=True)
    show_greece = st.sidebar.checkbox("Grecia", value=True)

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
    
    # Universal analysis option
    opcRegLog = st.sidebar.radio(
        "Selecciona una opción a analizar:",
        (
            "Predicción",
            "Matriz de Confusión",
            "Metricas del modelo"
        )
    )

    # Function to run logistic regression for a country
    def run_logistic_regression(numeric_df, binary_df, country_name):
        st.subheader(f"Regresión Logística - {country_name}")
        
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
        
        if opcRegLog == "Predicción":
            pred_df = X_test.copy()
            pred_df = pd.DataFrame(pred_df, columns=available_vars)
            pred_df["Probabilidad False"] = y_proba[:, 0]
            pred_df["Probabilidad True"] = y_proba[:, 1]
            pred_df["Predicción"] = y_pred

            st.write("Predicciones del modelo")
            st.dataframe(pred_df.head(10))  # Mostrar primeras 10 filas
            
        elif opcRegLog == "Matriz de Confusión":
            st.write("Matriz de confusión")
            matriz = confusion_matrix(y_test, y_pred)
            st.write(pd.DataFrame(matriz, index=["Positivo", "Negativo"], columns=["Predicho 0", "Predicho 1"]))
            
        elif opcRegLog == "Metricas del modelo":
            st.write("Métricas del Modelo")
            
            precisionf = precision_score(y_test, y_pred, average="binary", pos_label="f")
            precisiont = precision_score(y_test, y_pred, average="binary", pos_label="t")
            exactitud = accuracy_score(y_test, y_pred)
            sensibilidadf = recall_score(y_test, y_pred, average="binary", pos_label="f")
            sensibilidadt = recall_score(y_test, y_pred, average="binary", pos_label="t")

            # Crear tabla con precisión y sensibilidad por clase, y exactitud en una sola columna
            metricas_df = pd.DataFrame({
                "f": [precisionf, sensibilidadf, exactitud],
                "t": [precisiont, sensibilidadt, exactitud] 
            }, index=["Precisión", "Sensibilidad", "Exactitud"])

            metricas_df = metricas_df.fillna("")  

            metricas_df["f"] = pd.to_numeric(metricas_df["f"], errors='coerce')
            metricas_df["t"] = pd.to_numeric(metricas_df["t"], errors='coerce')

            # Mostrar tabla formateada
            st.table(metricas_df.style.format("{:.2f}"))

    # Create three columns for the countries
    col1, col2, col3 = st.columns(3)

    # Spain
    if show_spain:
        with col1:
            run_logistic_regression(
                data['numericDf'],
                data['df'][['host_is_superhost', 'host_identity_verified']],
                "España"
            )

    # Mexico
    if show_mexico:
        with col2:
            run_logistic_regression(
                data['numericDfMx'],
                data['dfMx'][['host_is_superhost', 'host_identity_verified']],
                "México"
            )

    # Greece
    if show_greece:
        with col3:
            run_logistic_regression(
                data['numericDfGr'],
                data['dfGr'][['host_is_superhost', 'host_identity_verified']],
                "Grecia"
            )