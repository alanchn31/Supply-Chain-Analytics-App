import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px # interactive charts
from welcome_page import welcome
from sales_dashboard_page import sales_dashboard
from operations_dashboard_page import operations_dashboard

st.set_page_config(              
page_title = "Sales & Operations Dashboard",             
page_icon = ":bar_chart:",          
layout = "wide",      
)

with st.expander("Upload File"):
    uploaded_file = st.file_uploader("Upload a CSV file for analysis")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.header("Preview of file")
        st.write(df.head())


if uploaded_file is not None:
    st.sidebar.header("Please Filter Here:")
    prod_type = st.sidebar.multiselect(
        "Select the Product Type:",
        options=df["product_type"].unique(),
        default=df["product_type"].unique()
    )

    df_selection = df.query(
        "product_type == @prod_type"
    )

    if df_selection.empty:
        st.warning("No data available based on the current filter settings!")
        st.stop() # This will halt the app from further execution.

    menu = ['Welcome Page', 'Sales Dashboard','Operations Dashboard']
    navigation = st.sidebar.selectbox(label="Select menu", options=menu)

    # Runs 'Sales Dashboard' app
    if navigation == 'Welcome Page':
        with st.container():
            welcome.main()
    elif navigation == 'Sales Dashboard':
        with st.container():
            sales_dashboard.render(df_selection)
    elif navigation == 'Operations Dashboard':
        with st.container():
            operations_dashboard.render(df_selection)
