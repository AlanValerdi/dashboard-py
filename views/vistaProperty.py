import streamlit as st
import pandas as pd
import altair as alt
import streamlit_shadcn_ui as ui
import plotly.express as px


def show(data):
    df_sp = data["df"]
    df_mx = data["dfMx"]


    col1, col2, col3 = st.columns([1.5, 3.5, 2], gap="medium")

    # ---------------------- COL 1 ----------------------
    with col1:
        st.header("Resumen General")

        unique_sp = df_sp["property_type"].nunique()
        unique_mx = df_mx["property_type"].nunique()

        ui.metric_card("Tipos únicos (España)", str(unique_sp), description="property_type únicos")
        ui.metric_card("Tipos únicos (México)", str(unique_mx), description="property_type únicos")

        top_sp = df_sp["property_type"].value_counts().idxmax()
        top_mx = df_mx["property_type"].value_counts().idxmax()

        st.markdown(f"**Tipo más común en España:** `{top_sp}`")
        st.markdown(f"**Tipo más común en México:** `{top_mx}`")

        avg_price_sp = df_sp.groupby("property_type")["price"].mean().mean()
        avg_price_mx = df_mx.groupby("property_type")["price"].mean().mean()

        ui.metric_card("Precio medio por tipo (España)", f"€{avg_price_sp:,.0f}")
        ui.metric_card("Precio medio por tipo (México)", f"${avg_price_mx:,.0f}")

    # ---------------------- COL 2 ----------------------
    with col2:
        st.header("Comparación de Precio por Tipo de Propiedad")

        # Agrupar y limpiar
        sp_grouped = df_sp.groupby("property_type")["price"].mean().reset_index()
        mx_grouped = df_mx.groupby("property_type")["price"].mean().reset_index()

        sp_grouped["pais"] = "España"
        mx_grouped["pais"] = "México"

        combined = pd.concat([sp_grouped, mx_grouped])
        combined = combined.sort_values("price", ascending=False)

        # Gráfico de línea
        line_chart = alt.Chart(combined).mark_line(point=True).encode(
            x=alt.X("property_type:N", sort="-y", title="Tipo de propiedad"),
            y=alt.Y("price:Q", title="Precio medio"),
            color="pais:N",
            tooltip=["property_type", "price", "pais"]
        ).properties(
            width=600,
            height=400
        )

        st.altair_chart(line_chart, use_container_width=True)

        # Nueva sección: distribución
        st.subheader("Distribución de Anuncios por Tipo de Propiedad")

        sp_count = df_sp["property_type"].value_counts().reset_index()
        mx_count = df_mx["property_type"].value_counts().reset_index()

        sp_count.columns = ["property_type", "count"]
        mx_count.columns = ["property_type", "count"]

        sp_count["pais"] = "España"
        mx_count["pais"] = "México"

        dist_df = pd.concat([sp_count, mx_count])
        top_types = dist_df.groupby("property_type")["count"].sum().nlargest(15).index
        dist_df = dist_df[dist_df["property_type"].isin(top_types)]

        bar_chart = alt.Chart(dist_df).mark_bar().encode(
            x=alt.X("count:Q", title="Número de anuncios"),
            y=alt.Y("property_type:N", sort="-x", title="Tipo de propiedad"),
            color="pais:N",
            tooltip=["property_type", "count", "pais"]
        ).properties(
            width=600,
            height=500
        )

        st.altair_chart(bar_chart, use_container_width=True)

        sp_count = df_sp["property_type"].value_counts().reset_index()
        mx_count = df_mx["property_type"].value_counts().reset_index()

        sp_count.columns = ["property_type", "count"]
        mx_count.columns = ["property_type", "count"]

        sp_prices = df_sp.groupby("property_type")["price"].mean().reset_index()
        mx_prices = df_mx.groupby("property_type")["price"].mean().reset_index()

        sp_rent = pd.merge(sp_prices, sp_count, on="property_type")
        mx_rent = pd.merge(mx_prices, mx_count, on="property_type")

        sp_rent["rentabilidad"] = sp_rent["price"] / sp_rent["count"]
        mx_rent["rentabilidad"] = mx_rent["price"] / mx_rent["count"]

        sp_rent["pais"] = "España"
        mx_rent["pais"] = "México"

        # Top 3 de cada país
        top_spain = sp_rent.sort_values("rentabilidad", ascending=False).head(3)
        top_mexico = mx_rent.sort_values("rentabilidad", ascending=False).head(3)

        st.subheader("Top 3 propiedades más rentables por país")

        colc1, colc2, colc3 = st.columns(3)

        # Split the top properties into columns
        top_properties = pd.concat([top_spain, top_mexico]).reset_index()
        for idx, row in top_properties.iterrows():
            col = [colc1, colc2, colc3][idx % 3]  # Distribute cards across columns
            currency_symbol = "$" if row['pais'] == "México" else "€"
            with col:
                ui.metric_card(
                    title=f"{row['property_type']} ({row['pais']})",
                    content=f"💰 {currency_symbol}{row['rentabilidad']:.2f} /anuncio",
                    description=f"Precio medio: {currency_symbol}{row['price']:.0f}, Anuncios: {int(row['count'])}",
                )


    # ---------------------- COL 3 ----------------------
    with col3:
        st.header("Insights")

        # Precio máximo y mínimo
        max_sp = sp_grouped.sort_values("price", ascending=False).iloc[0]
        min_sp = sp_grouped.sort_values("price", ascending=True).iloc[0]

        max_mx = mx_grouped.sort_values("price", ascending=False).iloc[0]
        min_mx = mx_grouped.sort_values("price", ascending=True).iloc[0]

        st.markdown("### España")
        st.markdown(f"💰 *Tipo más caro:* **{max_sp['property_type']}** (${max_sp['price']:.0f})")
        st.markdown(f"🔻 *Tipo más barato:* **{min_sp['property_type']}** (${min_sp['price']:.0f})")

        st.divider()

        st.markdown("### México")
        st.markdown(f"💰 *Tipo más caro:* **{max_mx['property_type']}** (${max_mx['price']:.0f})")
        st.markdown(f"🔻 *Tipo más barato:* **{min_mx['property_type']}** (${min_mx['price']:.0f})")

        


        # Rentabilidad: precio medio / cantidad de anuncios
       # Calcular rentabilidad por propiedad
        sp_count = df_sp["property_type"].value_counts().reset_index()
        mx_count = df_mx["property_type"].value_counts().reset_index()

        sp_count.columns = ["property_type", "count"]
        mx_count.columns = ["property_type", "count"]

        sp_prices = df_sp.groupby("property_type")["price"].mean().reset_index()
        mx_prices = df_mx.groupby("property_type")["price"].mean().reset_index()

        sp_rent = pd.merge(sp_prices, sp_count, on="property_type")
        mx_rent = pd.merge(mx_prices, mx_count, on="property_type")

        sp_rent["rentabilidad"] = sp_rent["price"] / sp_rent["count"]
        mx_rent["rentabilidad"] = mx_rent["price"] / mx_rent["count"]

        sp_rent["pais"] = "España"
        mx_rent["pais"] = "México"

        

        # Rentabilidad promedio general por país
        avg_rent_spain = sp_rent["rentabilidad"].mean()
        avg_rent_mexico = mx_rent["rentabilidad"].mean()

        country_with_more = "España" if avg_rent_spain > avg_rent_mexico else "México"
        color_class = "bg-green-700" if country_with_more == "España" else "bg-blue-700"

        st.divider()
        st.subheader("Comparación general de rentabilidad por país")
        ui.metric_card(
            title="País con mayor rentabilidad",
            content=country_with_more,
            description=f"España: {avg_rent_spain:.2f} €/anuncio · México: {avg_rent_mexico:.2f} €/anuncio",
            
        )

        # # Unificar ambos dataframes para la gráfica
        # rentabilidad_total = pd.concat([sp_rent, mx_rent])

        # # Filtrar top 6 propiedades más rentables en total
        # top_types = (
        #     rentabilidad_total.groupby("property_type")["rentabilidad"]
        #     .mean()
        #     .sort_values(ascending=False)
        #     .head(6)
        #     .index
        # )

        # df_plot = rentabilidad_total[rentabilidad_total["property_type"].isin(top_types)]

        # fig = px.bar(
        #     df_plot,
        #     x="property_type",
        #     y="rentabilidad",
        #     color="pais",
        #     barmode="group",
        #     text_auto=".2f",
        #     color_discrete_map={"España": "green", "México": "blue"},
        #     labels={"rentabilidad": "Rentabilidad (€/anuncio)", "property_type": "Tipo de Propiedad"},
        #     title="Rentabilidad promedio por tipo de propiedad y país",
        #     height=500,
        # )

        # fig.update_layout(
        #     legend_title_text="País",
        #     title_x=0.5,
        #     uniformtext_minsize=8,
        #     uniformtext_mode='hide'
        # )

        # st.plotly_chart(fig, use_container_width=True)
         



