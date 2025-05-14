import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score

def show(data):
    st.title("Regresión Logística")
    
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
        binary_df = data['df'][['host_is_superhost', 'host_identity_verified']]
        binary_cols = ['host_is_superhost', 'host_identity_verified']
        ciudad = "España"
    elif country == "México":
        numeric_df = data['numericDfMx']
        numeric_cols = list(data['numericColsMx'])
        binary_df = data['dfMx'][['host_is_superhost', 'host_identity_verified']]
        binary_cols = ['host_is_superhost', 'host_identity_verified']
        ciudad = "México"
    else:  # Grecia
        numeric_df = data['numericDfGr']
        numeric_cols = list(data['numericColsGr'])
        binary_df = data['dfGr'][['host_is_superhost', 'host_identity_verified']]
        binary_cols = ['host_is_superhost', 'host_identity_verified']
        ciudad = "Grecia"

    st.sidebar.subheader("Selección de variables para Regresión Logística")
    #Widget 5: Select box
    #Menu desplegable de opciones de la variable dependiente seleccionada
    dependent_variable = st.sidebar.selectbox(label="Variable dependiente", options=binary_cols)
    
    #Widget 6: Select box
    #Menu desplegable de opciones de la variable independiente seleccionada
    independent_option = [var for var in numeric_cols if var != dependent_variable]
    independent_variables = st.sidebar.multiselect(label="Variables independientes", options=independent_option, default=independent_option[:1])
    # Validar que al menos una variable independiente fue seleccionada
    if not independent_variables:
        st.warning("Por favor selecciona al menos una variable independiente.")
        st.stop()
    
    opcRegLog = st.sidebar.radio(
        "Selecciona una opción a analizar:",
        (
            "Predicción",
            "Matriz de Confusión",
            "Metricas del modelo"
        )
    )
    
    st.title(f"Regresión Logistica - {ciudad}")
    varsIndep = numeric_df[independent_variables]
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
        pred_df = pd.DataFrame(pred_df, columns=independent_variables)
        pred_df["Probabilidad False"] = y_proba[:, 0]
        pred_df["Probabilidad True"] = y_proba[:, 1]
        pred_df["Predicción"] = y_pred

        st.subheader("Predicciones del modelo")
        st.dataframe(pred_df.head(10))  # Mostrar primeras 10 filas
        
    elif opcRegLog == "Matriz de Confusión":
        st.subheader("Matriz de confusión")
        matriz = confusion_matrix(y_test, y_pred)
        st.write("Matriz de Confusión:")
        st.write(pd.DataFrame(matriz, index=["Positivo", "Negativo"], columns=["Predicho 0", "Predicho 1"]))
        
    elif opcRegLog == "Metricas del modelo":
        st.subheader("Métricas del Modelo")
        
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