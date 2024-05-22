import streamlit as st #streamlit backend
import plotly.express as px # interactive charts

def render(df_selection):
    df_selection["is_oos"] = (df_selection["stock"] == 0).astype(int)
    # TOP KPI's
    oos_rate = df_selection["is_oos"].mean()
    df_selection['doi'] = df_selection['stock'] / df_selection['avg_daily_sales']
    doi = int(df_selection["doi"].mean())
    lead_time = int(df_selection["lead_time"].mean())

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Availability:")
        st.subheader(f"{round(1-oos_rate,4)*100}%")
    with middle_column:
        st.subheader("DOI:")
        st.subheader(f"{doi} days")
    with right_column:
        st.subheader("Average Lead Time:")
        st.subheader(f"{lead_time} days")
    st.markdown("""---""")

    first_chart, second_chart, third_chart = st.columns(3)
    with first_chart:
        df_selection['is_available'] = 1 - df_selection['is_oos']
        availability_by_product_type = df_selection.groupby(by=["product_type"])[["is_available"]].mean().sort_values(by="is_available")
        availability_by_product_type['is_available'] *= 100
        availability_by_product_type['avail_abv_target'] = (availability_by_product_type['is_available'] > 90)
        fig_product_avail = px.bar(
            availability_by_product_type,
            x="is_available",
            y=availability_by_product_type.index,
            orientation="h",
            title="<b>Availability by Product Category</b>",
            color="avail_abv_target",
            color_discrete_map={
                    True: 'green',
                    False: 'red'
            },
            color_discrete_sequence=["#0083B8"] * len(availability_by_product_type),
            template="plotly_white",
        ).update_layout(
            xaxis_title="Availability", yaxis_title="Product Type",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            showlegend=False
        )
        fig_product_avail.update_traces(hovertemplate=
                '<i>Product Type</i>: %{y}'+
                '<br>Availability: %{x:.2f}%' + 
                '<extra></extra>')
        st.plotly_chart(fig_product_avail, use_container_width=True)

    with second_chart:
        doi_by_product_type = df_selection.groupby(by=["product_type"])[["doi"]].mean().sort_values(by="doi", ascending=False)
        doi_by_product_type['doi'] = doi_by_product_type['doi'].astype(int)
        doi_by_product_type['doi_below_target'] = (doi_by_product_type['doi'] < 20)
        fig_product_doi = px.bar(
            doi_by_product_type,
            x="doi",
            y=doi_by_product_type.index,
            orientation="h",
            title="<b>DOI by Product Category</b>",
            color="doi_below_target",
            color_discrete_map={
                    True: 'green',
                    False: 'red'
            },
            template="plotly_white",
        ).update_layout(
            xaxis_title="DOI", yaxis_title="Product Type",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            showlegend=False
        )
        fig_product_doi.update_traces(hovertemplate=
                '<i>Product Type</i>: %{y}'+
                '<br>DOI: %{x} days' + 
                '<extra></extra>')
        st.plotly_chart(fig_product_doi, use_container_width=True)
    
    with third_chart:
        lt_by_product_type = df_selection.groupby(by=["product_type"])[["lead_time"]].mean().sort_values(by="lead_time", ascending=False)
        lt_by_product_type['lead_time'] = lt_by_product_type['lead_time'].astype(int)
        lt_by_product_type['lt_below_target'] = (lt_by_product_type['lead_time'] < 20)
        fig_product_lt = px.bar(
            lt_by_product_type,
            x="lead_time",
            y=lt_by_product_type.index,
            orientation="h",
            title="<b>Lead Time by Product Category</b>",
            color="lt_below_target",
            color_discrete_map={
                    True: 'green',
                    False: 'red'
            },
            template="plotly_white",
        ).update_layout(
            xaxis_title="Lead Time", yaxis_title="Product Type",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            showlegend=False
        )
        fig_product_lt.update_traces(hovertemplate=
                '<i>Product Type</i>: %{y}'+
                '<br>Lead Time: %{x} days' + 
                '<extra></extra>')
        st.plotly_chart(fig_product_lt, use_container_width=True)

    st.markdown("""---""")
    first_chart, second_chart, third_chart = st.columns(3)
    with first_chart:
        top_doi_by_product = df_selection.query("stock != 0").groupby(by=["sku"])[["doi"]].mean().sort_values(by="doi").head(10)
        fig_product_top_doi = px.bar(
            top_doi_by_product,
            x="doi",
            y=top_doi_by_product.index,
            orientation="h",
            title="<b>Fastest Moving Products (by DOI)</b>",
            color_discrete_sequence=["#0083B8"] * len(top_doi_by_product),
            template="plotly_white",
        ).update_layout(
            xaxis_title="DOI", yaxis_title="Product",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=dict(autorange="reversed")
        )
        fig_product_top_doi.update_traces(hovertemplate=
                '<i>Product</i>: %{y}'+
                '<br>DOI: %{x:.1f} days' + 
                '<extra></extra>',
        marker_color = 'green')
        st.plotly_chart(fig_product_top_doi, use_container_width=True)

    with second_chart:
        bottom_doi_by_product = df_selection.query("stock != 0").groupby(by=["sku"])[["doi"]].mean().sort_values(by="doi", ascending=False).head(10)
        fig_product_bottom_doi = px.bar(
            bottom_doi_by_product,
            x="doi",
            y=bottom_doi_by_product.index,
            orientation="h",
            title="<b>Slowest Moving Products (by DOI)</b>",
            color_discrete_sequence=["#0083B8"] * len(bottom_doi_by_product),
            template="plotly_white",
        ).update_layout(
            xaxis_title="DOI", yaxis_title="Product",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=dict(autorange="reversed")
        )
        fig_product_bottom_doi.update_traces(hovertemplate=
                '<i>Product</i>: %{y}'+
                '<br>DOI: %{x:.1f} days' + 
                '<extra></extra>',
        marker_color = '#AF0038')
        st.plotly_chart(fig_product_bottom_doi, use_container_width=True)

    with third_chart:
        bottom_lt_by_product = df_selection.groupby(by=["sku"])[["lead_time"]].mean().sort_values(by="lead_time", ascending=False).head(10)
        fig_product_bottom_lt = px.bar(
            bottom_lt_by_product,
            x="lead_time",
            y=bottom_lt_by_product.index,
            orientation="h",
            title="<b>Products with longest lead times</b>",
            color_discrete_sequence=["#0083B8"] * len(bottom_lt_by_product),
            template="plotly_white",
        ).update_layout(
            xaxis_title="Lead Time", yaxis_title="Product",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=dict(autorange="reversed")
        )
        fig_product_bottom_lt.update_traces(hovertemplate=
                '<i>Product</i>: %{y}'+
                '<br>Lead Time: %{x:.1f} days' + 
                '<extra></extra>',
        marker_color = '#AF0038')
        st.plotly_chart(fig_product_bottom_lt, use_container_width=True)


# Main
if __name__ == "__main__":
   main()