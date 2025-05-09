import streamlit as st
import streamlit_shadcn_ui as ui

def renderGeneralAnalysis(data):
    # Setup variables
    # Spain
    df = data["dfMx"]
    spainTotalValues = data["spainTotalValues"]
    spDiffVsMex = data["spDiffVsMex"]
    textColsSp = data["textCols"]

    # Mex
    dfMx = data["df"]
    mexTotalValues = data["mexTotalValues"]
    mxDiffVsSpain = data["mxDiffVsSpain"]

    st.title('Analisis General')
    dataRendering = st.selectbox("Seleccionar Información para mostrar", ["España - Madrid 🇪🇸", "México - Ciudad de México 🇲🇽", "Grecia - Athenas 🇬🇷"])   

    cols = st.columns(3)
    binaryCols = st.columns(2)

    if dataRendering == "España - Madrid 🇪🇸":
        with cols[0]:
            mexCB = ui.checkbox(default_checked=False, label="Comparar Información con México")
        with cols[1]:
            athCB = ui.checkbox(default_checked=False, label="Comparar Información con Athenas")
        
        
        if not mexCB and not athCB:            
                st.title("Información de España - Madrid")
                ui.metric_card(title="Número total de registros de España", content=str(spainTotalValues) + " " + "registros")
                with binaryCols[0]:  
                    Button = ui.button("Mostrar variables String", key="clk_btn")
                if Button:
                    with binaryCols[0]:
                        ui.metric_card(title="Cantidad Total de variables String 🇪🇸:", content=" 24 Variables")
                    with binaryCols[1]:
                        st.write(textColsSp)
                st.subheader("Tabla de información general 🇪🇸")
                st.write(df)
                st.subheader("Variables del dataset 🇪🇸")
                st.write(df.columns)            
                st.subheader("Estadísticas 🇪🇸")
                st.write(df.describe())

        elif mexCB and not athCB:
            with binaryCols[0]:
                ui.metric_card(title="Número total de registros de España 🇪🇸:", content=str(spainTotalValues) + " " + "registros", description=f"+{spDiffVsMex}% en comparación con 🇲🇽")
            with binaryCols[1]:
                ui.metric_card(title="Número total de registros de Mexico 🇲🇽:", content=str(mexTotalValues) + " " + "registros", description=f"{mxDiffVsSpain}% en comparación con 🇪🇸")

    # México
    if dataRendering == "México - Ciudad de México 🇲🇽":
        with cols[0]:
            mexCB = ui.checkbox(default_checked=False, label="Comparar Información con España   ")
        with cols[1]:
            athCB = ui.checkbox(default_checked=False, label="Comparar Información con Athenas")

        
        if not mexCB and not athCB:       
                st.title("Información de México - Ciudad de México")     
                ui.metric_card(title="Número total de registros de Mexico", content=str(mexTotalValues) + " " + "registros")
                with binaryCols[0]:  
                    Button = ui.button("Mostrar variables String", key="clk_btn")
                if Button:
                    with binaryCols[0]:
                        ui.metric_card(title="Cantidad Total de variables String 🇲🇽:", content=" 24 Variables")
                    with binaryCols[1]:
                        st.write(textColsSp)
                st.subheader("Tabla de información general 🇲🇽")
                st.write(dfMx)
                st.subheader("Variables del dataset 🇲🇽")
                st.write(dfMx.columns)            
                st.subheader("Estadísticas 🇲🇽")
                st.write(dfMx.describe())

    
       
