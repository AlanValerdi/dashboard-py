import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit_shadcn_ui as ui


def show(data):
    spainTotalValues = data["spainTotalValues"]
    mexTotalValues = data["mexTotalValues"]

    col1, col2, col3 = st.columns([1.5, 4.5, 2], gap="medium")


    # LEFT COLUMN (General Information)
    with col1:
        st.header("Información general")
        st.metric("Número total de cuartos", data['df'].shape[0])
        st.metric("Madrid - Número total de variables", data['df'].shape[1])
        ui.metric_card(title="Número total de registros de España 🇪🇸", content=str(spainTotalValues) + " " + "registros")
        st.divider()
        st.metric("Número total de cuartos", data['dfMx'].shape[0])
        st.metric("México - Número total de variables", data['dfMx'].shape[1])
        ui.metric_card(title="Número total de registros de México 🇲🇽", content=str(mexTotalValues) + " " + "registros")

    # MIDDLE COLUMN (Correlation Heatmaps)
    with col2:
        tabValue = ui.tabs(options=["España 🇪🇸", "Athenas 🇬🇷"], default_value="España 🇪🇸")
        
        if tabValue == "España 🇪🇸":
            st.header("Comparación México vs Madrid")
        elif tabValue == "Athenas 🇬🇷":
            st.header("Comparación México vs Athenas")
        
        col_spain, col_mex = st.columns(2)
        
        if tabValue == "España 🇪🇸":
            with col_mex:
                # Data load
                top_corr_mx = data["top_correlations_mex"]

                # HeatMap section
                st.subheader("Heatmap México 🇲🇽")
                corr_matrix_mexico = data['numericDfMx'].corr()
                fig2, ax2 = plt.subplots(figsize=(19, 13))
                sns.heatmap(corr_matrix_mexico, annot= True, annot_kws={"size": 8}, fmt=".1f", cmap="coolwarm", ax=ax2)
                st.pyplot(fig2)

                # Metric cards
                st.markdown(f"""
                <div style="background-color:#14532d; padding:16px; border-radius:12px; color:white; text-align:start; margin-bottom:12px">
                    <h6>Correlación Positiva Más Alta 🇲🇽</h6>
                    <p style="font-size:20px; font-weight:bold;">{top_corr_mx['max_pair'][0]} ↔ {top_corr_mx['max_pair'][1]} = {top_corr_mx['max_value']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background-color:#7f1d1d; padding:16px; border-radius:12px; color:white; text-align:start">
                    <h6>Correlación Negativa Más Alta 🇲🇽</h6>
                    <p style="font-size:20px; font-weight:bold;">{top_corr_mx['min_pair'][0]} ↔ {top_corr_mx['min_pair'][1]} = {top_corr_mx['min_value']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
            
            st.divider()

            with col_spain:
                # Data load
                top_corr = data["top_correlations_spain"]

                # HeatMap section
                st.subheader("Heatmap Madrid 🇪🇸")
                # 'host_response_rate','host_acceptance_rate',
                corr_spain = data['numericDf'].corr()
                fig1, ax1 = plt.subplots(figsize=(19,13))
                sns.heatmap(corr_spain, annot= True, annot_kws={"size": 8}, fmt=".1f", cmap='coolwarm', ax=ax1)
                st.pyplot(fig1)

                # Metric cards
                st.markdown(f"""
                <div style="background-color:#14532d; padding:16px; border-radius:12px; color:white; text-align:start; margin-bottom:12px">
                    <h6>Correlación Positiva Más Alta 🇪🇸</h6>
                    <p style="font-size:20px; font-weight:bold;">{top_corr['max_pair'][0]} ↔ {top_corr['max_pair'][1]} = {top_corr['max_value']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background-color:#7f1d1d; padding:16px; border-radius:12px; color:white; text-align:start">
                    <h6>Correlación Negativa Más Alta 🇪🇸</h6>
                    <p style="font-size:20px; font-weight:bold;">{top_corr['min_pair'][0]} ↔ {top_corr['min_pair'][1]} = {top_corr['min_value']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
        
       
        if tabValue == "Athenas 🇬🇷":
            with col_mex:
                st.header("Heatmap Mexico")
                corr_mexico = data['dfMx'][['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'availability_365']].corr()
                fig2, ax2 = plt.subplots(figsize=(4,2))
                sns.heatmap(corr_mexico, annot=True, cmap='coolwarm', ax=ax2)
                st.pyplot(fig2)

            with col_spain:
                st.header("Heatmap Athenas")
                corr_spain = data['df'][['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'availability_365']].corr()
                fig1, ax1 = plt.subplots()
                sns.heatmap(corr_spain, annot=True, cmap='coolwarm', ax=ax1)
                st.pyplot(fig1)

        


    # RIGHT COLUMN (Pie Charts)
    with col3:
        st.header("Room Types Madrid")
        fig_room_spain = px.pie(data['df'], names="room_type")
        st.plotly_chart(fig_room_spain, use_container_width=True)
        

        st.divider()

        st.header("Room Types México")
        fig_room_mex = px.pie(data['dfMx'], names="room_type")
        st.plotly_chart(fig_room_mex, use_container_width=True)