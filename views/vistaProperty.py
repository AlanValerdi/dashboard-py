import streamlit as st
import pandas as pd
import altair as alt
import streamlit_shadcn_ui as ui
import plotly.express as px


def show(data):
    df_sp = data["df"]
    df_mx = data["dfMx"]
    df_gr = data["dfGr"]

    col1, col2, col3 = st.columns([1.5, 3.5, 2], gap="medium")

    # ---------------------- COL 1 ----------------------
    with col1:
        st.header("Resumen General")

        unique_sp = df_sp["property_type"].nunique()
        unique_mx = df_mx["property_type"].nunique()
        unique_gr = df_gr["property_type"].nunique()

        ui.metric_card("Tipos únicos (España)", str(unique_sp), description="property_type únicos")
        ui.metric_card("Tipos únicos (México)", str(unique_mx), description="property_type únicos")
        ui.metric_card("Tipos únicos (Grecia)", str(unique_gr), description="property_type únicos")

        top_sp = df_sp["property_type"].value_counts().idxmax()
        top_mx = df_mx["property_type"].value_counts().idxmax()
        top_gr = df_gr["property_type"].value_counts().idxmax()

        st.markdown(f"**Tipo más común en España:** `{top_sp}`")
        st.markdown(f"**Tipo más común en México:** `{top_mx}`")
        st.markdown(f"**Tipo más común en Grecia:** `{top_gr}`")

        avg_price_sp = df_sp.groupby("property_type")["price"].mean().mean()
        avg_price_mx = df_mx.groupby("property_type")["price"].mean().mean()
        avg_price_gr = df_gr.groupby("property_type")["price"].mean().mean()

        ui.metric_card("Precio medio por tipo (España)", f"€{avg_price_sp:,.0f}")
        ui.metric_card("Precio medio por tipo (México)", f"${avg_price_mx:,.0f}")
        ui.metric_card("Precio medio por tipo (Grecia)", f"€{avg_price_gr:,.0f}")

    # ---------------------- COL 2 ----------------------
    with col2:
        st.header("Comparación de Precio por Tipo de Propiedad")

        # Agrupar y limpiar
        sp_grouped = df_sp.groupby("property_type")["price"].mean().reset_index()
        mx_grouped = df_mx.groupby("property_type")["price"].mean().reset_index()
        gr_grouped = df_gr.groupby("property_type")["price"].mean().reset_index()

        sp_grouped["pais"] = "España"
        mx_grouped["pais"] = "México"
        gr_grouped["pais"] = "Grecia"

        combined = pd.concat([sp_grouped, mx_grouped, gr_grouped])
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
        gr_count = df_gr["property_type"].value_counts().reset_index()

        sp_count.columns = ["property_type", "count"]
        mx_count.columns = ["property_type", "count"]
        gr_count.columns = ["property_type", "count"]

        sp_count["pais"] = "España"
        mx_count["pais"] = "México"
        gr_count["pais"] = "Grecia"

        dist_df = pd.concat([sp_count, mx_count, gr_count])
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

        # Rentabilidad
        sp_prices = df_sp.groupby("property_type")["price"].mean().reset_index()
        mx_prices = df_mx.groupby("property_type")["price"].mean().reset_index()
        gr_prices = df_gr.groupby("property_type")["price"].mean().reset_index()

        sp_rent = pd.merge(sp_prices, sp_count, on="property_type")
        mx_rent = pd.merge(mx_prices, mx_count, on="property_type")
        gr_rent = pd.merge(gr_prices, gr_count, on="property_type")

        sp_rent["rentabilidad"] = sp_rent["price"] / sp_rent["count"]
        mx_rent["rentabilidad"] = mx_rent["price"] / mx_rent["count"]
        gr_rent["rentabilidad"] = gr_rent["price"] / gr_rent["count"]

        sp_rent["pais"] = "España"
        mx_rent["pais"] = "México"
        gr_rent["pais"] = "Grecia"

        # Top 3 de cada país
        top_spain = sp_rent.sort_values("rentabilidad", ascending=False).head(3)
        top_mexico = mx_rent.sort_values("rentabilidad", ascending=False).head(3)
        top_greece = gr_rent.sort_values("rentabilidad", ascending=False).head(3)

        st.subheader("Top 3 propiedades más rentables por país")

        colc1, colc2, colc3 = st.columns(3)

        # Split the top properties into columns
        top_properties = pd.concat([top_spain, top_mexico, top_greece]).reset_index()
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

        max_gr = gr_grouped.sort_values("price", ascending=False).iloc[0]
        min_gr = gr_grouped.sort_values("price", ascending=True).iloc[0]

        st.markdown("### España")
        st.markdown(f"💰 *Tipo más caro:* **{max_sp['property_type']}** (€{max_sp['price']:.0f})")
        st.markdown(f"🔻 *Tipo más barato:* **{min_sp['property_type']}** (€{min_sp['price']:.0f})")

        st.divider()

        st.markdown("### México")
        st.markdown(f"💰 *Tipo más caro:* **{max_mx['property_type']}** (${max_mx['price']:.0f})")
        st.markdown(f"🔻 *Tipo más barato:* **{min_mx['property_type']}** (${min_mx['price']:.0f})")

        st.divider()

        st.markdown("### Grecia")
        st.markdown(f"💰 *Tipo más caro:* **{max_gr['property_type']}** (€{max_gr['price']:.0f})")
        st.markdown(f"🔻 *Tipo más barato:* **{min_gr['property_type']}** (€{min_gr['price']:.0f})")

        # Rentabilidad promedio general por país
        avg_rent_spain = sp_rent["rentabilidad"].mean()
        avg_rent_mexico = mx_rent["rentabilidad"].mean()
        avg_rent_greece = gr_rent["rentabilidad"].mean()

        # Find country with highest rentability
        rentabilities = {
            "España": avg_rent_spain,
            "México": avg_rent_mexico,
            "Grecia": avg_rent_greece
        }
        country_with_more = max(rentabilities.items(), key=lambda x: x[1])[0]

        st.divider()
        st.subheader("Comparación general de rentabilidad por país")
        ui.metric_card(
            title="País con mayor rentabilidad",
            content=country_with_more,
            description=f"España: {avg_rent_spain:.2f} €/anuncio · México: {avg_rent_mexico:.2f} €/anuncio · Grecia: {avg_rent_greece:.2f} €/anuncio"
        )

         



