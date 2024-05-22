import streamlit as st #streamlit backend
import plotly.express as px # interactive charts

def render(df_selection):
    df_selection['gross_profit'] = df_selection['revenue'] - df_selection['cogs']
    # TOP KPI's
    total_revenue = int(df_selection["revenue"].sum())
    total_gross_margin = int(df_selection["gross_profit"].sum())
    total_sales_qty = int(df_selection["sales_qty"].sum())
    # avg_defect_rate = round(df_selection["defect_rates"].mean(), 4)

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Revenue:")
        st.subheader(f"US ${total_revenue:,}")
    with middle_column:
        st.subheader("Total Gross Profit:")
        st.subheader(f"US ${total_gross_margin:,}")
    with right_column:
        st.subheader("Number of Products sold:")
        st.subheader(f"{total_sales_qty:,}")
    st.markdown("""---""")

    first_chart, second_chart = st.columns(2)

    with first_chart:
        sales_by_product_type = df_selection.groupby(by=["product_type"])[["revenue"]].sum().sort_values(by="revenue")
        fig_product_sales = px.bar(
            sales_by_product_type,
            x="revenue",
            y=sales_by_product_type.index,
            orientation="h",
            title="<b>Sales by Product Category</b>",
            color_discrete_sequence=["#0083B8"] * len(sales_by_product_type),
            template="plotly_white",
        ).update_layout(
            xaxis_title="Revenue", yaxis_title="Product Type",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )
        fig_product_sales.update_traces(hovertemplate=
                '<i>Product Type</i>: %{y}'+
                '<br>Revenue: $%{x:,.2f}' + 
                '<extra></extra>')
        st.plotly_chart(fig_product_sales, use_container_width=True)

    with second_chart:
        gm_by_product_type = df_selection.groupby(by=["product_type"])[["gross_profit"]].sum().sort_values(by="gross_profit")
        gm_by_product_type['gm_positive'] = (gm_by_product_type['gross_profit'] > 0)
        fig_product_gm = px.bar(
            gm_by_product_type,
            x="gross_profit",
            y=gm_by_product_type.index,
            orientation="h",
            title="<b>Gross Profit by Product Category</b>",
            color="gm_positive",
            color_discrete_map={
                    True: 'green',
                    False: 'red'
            },
            template="plotly_white",
        ).update_layout(
            xaxis_title="Gross Profit", yaxis_title="Product Type",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            showlegend=False
        )
        fig_product_gm.update_traces(hovertemplate=
                '<i>Product Type</i>: %{y}'+
                '<br>Gross Profit: $%{x:,.2f}' + 
                '<extra></extra>')
        st.plotly_chart(fig_product_gm, use_container_width=True)

    st.markdown("""---""")

    first_chart, second_chart, third_chart = st.columns(3)
    with first_chart:
        sales_by_product = df_selection.groupby(by=["sku"])[["revenue"]].sum().sort_values(by="revenue",
        ascending=False).head(10)
        fig_product_sales = px.bar(
            sales_by_product,
            x="revenue",
            y=sales_by_product.index,
            orientation="h",
            title="<b>Best Selling Products (by TIV)</b>",
            color_discrete_sequence=["#0083B8"] * len(sales_by_product),
            template="plotly_white",
        ).update_layout(
            xaxis_title="Revenue", yaxis_title="Product",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=dict(autorange="reversed")
        )
        fig_product_sales.update_traces(hovertemplate=
                '<i>Product</i>: %{y}'+
                '<br>Revenue: $%{x:,.2f}' + 
                '<extra></extra>',
        marker_color = 'orange')
        st.plotly_chart(fig_product_sales, use_container_width=True)

    with second_chart:
        gm_by_product = df_selection.groupby(by=["sku"])[["gross_profit"]].sum().sort_values(by="gross_profit",
        ascending=False).head(10)
        gm_by_product['gm_positive'] = (gm_by_product['gross_profit'] > 0)
        fig_product_gm = px.bar(
            gm_by_product,
            x="gross_profit",
            y=gm_by_product.index,
            orientation="h",
            title="<b>Most Profitable Products (by Gross Margin)</b>",
            color="gm_positive",
            color_discrete_map={
                    True: 'green',
                    False: 'red'
            },
            color_discrete_sequence=["#0083B8"] * len(gm_by_product),
            template="plotly_white",
        ).update_layout(
            xaxis_title="gross_profit", yaxis_title="Product",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=dict(autorange="reversed"),
            showlegend=False
        )
        fig_product_gm.update_traces(hovertemplate=
                '<i>Product</i>: %{y}'+
                '<br>Gross Profit: $%{x:,.2f}' + 
                '<extra></extra>')
        st.plotly_chart(fig_product_gm, use_container_width=True)

    with third_chart:
        sales_qty_by_product = df_selection.groupby(by=["sku"])[["sales_qty"]].sum().sort_values(by="sales_qty",
        ascending=False).head(10)
        fig_product_sales_qty = px.bar(
            sales_qty_by_product,
            x="sales_qty",
            y=sales_qty_by_product.index,
            orientation="h",
            title="<b>Fastest Moving Products (by Sales Qty)</b>",
            color_discrete_sequence=["#0083B8"] * len(sales_qty_by_product),
            template="plotly_white",
        ).update_layout(
            xaxis_title="Sales Quantity", yaxis_title="Product",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=dict(autorange="reversed")
        )
        fig_product_sales_qty.update_traces(hovertemplate=
                '<i>Product</i>: %{y}'+
                '<br>Qty Sold: %{x:,} pcs' + 
                '<extra></extra>',
        marker_color = 'orange')
        st.plotly_chart(fig_product_sales_qty, use_container_width=True)

    st.markdown("""---""")
    first_chart, second_chart, third_chart = st.columns(3)
    with first_chart:
        bottom_sales_by_product = df_selection.groupby(by=["sku"])[["revenue"]].sum().sort_values(by="revenue").head(10)
        fig_product_bottom_sales = px.bar(
            bottom_sales_by_product,
            x="revenue",
            y=bottom_sales_by_product.index,
            orientation="h",
            title="<b>Worst Selling Products (by TIV)</b>",
            color_discrete_sequence=["#0083B8"] * len(bottom_sales_by_product),
            template="plotly_white",
        ).update_layout(
            xaxis_title="Revenue", yaxis_title="Product",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=dict(autorange="reversed")
        )
        fig_product_bottom_sales.update_traces(hovertemplate=
                '<i>Product</i>: %{y}'+
                '<br>Revenue: $%{x:,.2f}' + 
                '<extra></extra>',
        marker_color = '#AF0038')
        st.plotly_chart(fig_product_bottom_sales, use_container_width=True)

    with second_chart:
        bottom_gm_by_product = df_selection.groupby(by=["sku"])[["gross_profit"]].sum().sort_values(by="gross_profit").head(10)
        bottom_gm_by_product['gm_positive'] = (bottom_gm_by_product['gross_profit'] > 0)
        fig_bottom_product_gm = px.bar(
            bottom_gm_by_product,
            x="gross_profit",
            y=bottom_gm_by_product.index,
            orientation="h",
            title="<b>Least Profitable Products (by Gross Margin)</b>",
            color="gm_positive",
            color_discrete_map={
                    True: 'green',
                    False: 'red'
            },
            color_discrete_sequence=["#0083B8"] * len(bottom_gm_by_product),
            template="plotly_white",
        ).update_layout(
            xaxis_title="gross_profit", yaxis_title="Product",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=dict(autorange="reversed"),
            showlegend=False
        )
        fig_bottom_product_gm.update_traces(hovertemplate=
                '<i>Product</i>: %{y}'+
                '<br>Gross Profit: $%{x:,.2f}' + 
                '<extra></extra>')
        st.plotly_chart(fig_bottom_product_gm, use_container_width=True)

    with third_chart:
        bottom_sales_qty_by_product = df_selection.groupby(by=["sku"])[["sales_qty"]].sum().sort_values(by="sales_qty").head(10)
        fig_bottom_product_sales_qty = px.bar(
            bottom_sales_qty_by_product,
            x="sales_qty",
            y=bottom_sales_qty_by_product.index,
            orientation="h",
            title="<b>Slowest Moving Products (by Sales Qty)</b>",
            color_discrete_sequence=["#0083B8"] * len(bottom_sales_qty_by_product),
            template="plotly_white",
        ).update_layout(
            xaxis_title="Sales Quantity", yaxis_title="Product",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)),
            yaxis=dict(autorange="reversed")
        )
        fig_bottom_product_sales_qty.update_traces(hovertemplate=
                '<i>Product</i>: %{y}'+
                '<br>Qty Sold: %{x:,} pcs' + 
                '<extra></extra>',
        marker_color = '#AF0038')
        st.plotly_chart(fig_bottom_product_sales_qty, use_container_width=True)

# Main
if __name__ == "__main__":
   main()