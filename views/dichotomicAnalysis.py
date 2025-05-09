import streamlit as st
import streamlit_shadcn_ui as ui
import plotly.express as px

def renderDichotomicAnalysis(data):
    # variables
    numericCols = data["numericCols"]
    uniqueValuesHostIdentityVerified = data["uniqueValuesHostIdentityVerified"]
    uniqueValuesHostIsSuperhost = data["uniqueValuesHostIsSuperhost"]
    df = data["df"]

    # For charts
    superHostPieSp = data["superHostPieSp"]
    superHostPieMx = data["superHostPieMx"]
    identityVerifiedPieSp = data["identityVerifiedPieSp"]
    identityVerifiedPieMx = data["identityVerifiedPieMx"]

    pieCols = st.columns(2)
    mainCols = st.columns(1)            

    
    # Side Bar
    st.sidebar.title("DAHSBOARD")
    st.sidebar.header("Sidebar")
    st.sidebar.subheader("Panel de selección")

    numericsVarsSelected= st.sidebar.multiselect(label="Variables graficadas", options= numericCols)
    categoryVarSelected = st.sidebar.selectbox("Categorias", options = uniqueValuesHostIdentityVerified)
    Button2 = st.sidebar.button(label="Mostrar grafica tipo lineplot")
    

    if Button2:
            st.plotly_chart(figure1)

    # body
    selectData = st.selectbox("Seleccionar Variable para mostrar", ["Host is superhost", "Host identity verified"])

    dataPlot = df[df['host_identity_verified'] == categoryVarSelected]
    data_features = dataPlot[numericsVarsSelected]
    figure1 = px.line(data_frame= data_features, x = data_features.index,
                        y = numericsVarsSelected, title = str('Representación gráfica'),
                        width=1600, height=600)
    
    # Host is superhost
    if selectData == "Host is superhost":
        with pieCols[0]:
            fig = px.pie(
                superHostPieSp,
                names="host_is_superhost",
                values="count",
                title="Distribución de Superhosts para España 🇪🇸"
            )
            st.plotly_chart(fig, use_container_width=True)
            ui.metric_card(title="Numero de Superhost:", content="¡76% son superhost!", description=f"13.1% más que 🇲🇽", key="superhostSp")
        with pieCols[1]:
            fig1 = px.pie(
                superHostPieMx,
                names="host_is_superhost",
                values="count",
                title="Distribución de Superhosts para México 🇲🇽",
            )
            st.plotly_chart(fig1, use_container_width=True)
            ui.metric_card(title="Numero de Superhost:", content="¡63.4% son superhost!", description=f"13.1% menos que 🇪🇸", key="superhostMx")
    elif selectData == "Host identity verified":
        # Host identity verified
        with pieCols[0]:
            fig3 = px.pie(
                identityVerifiedPieSp,
                names="host_identity_verified",
                values="count",
                title="identidades verificadas para España 🇪🇸"
            )
            st.plotly_chart(fig3, use_container_width=True)
            ui.metric_card(title="Numero de Usuarios con identidad verificada:", content="¡90.3% son usuarios confiables!!", description=f"5.4% menos que 🇪🇸", key="identityVerifiedMx")
            
        with pieCols[1]:
            fig4 = px.pie(
                identityVerifiedPieMx,
                names="host_identity_verified",
                values="count",
                title="identidades verificadas para México 🇲🇽"
            )
            st.plotly_chart(fig4, use_container_width=True)
            ui.metric_card(title="Numero de Usuarios con identidad verificada:", content="95.7% son usuarios confiables!", description=f"5.4% más que 🇲🇽", key="identityVerifiedSp")
        
         
    


    