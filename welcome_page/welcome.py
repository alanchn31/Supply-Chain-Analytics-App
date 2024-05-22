import streamlit as st
import os

def main():
    """Welcome main
    """    
    st.header("Welcome")
    st.subheader("What is this?")
    st.write("""
             This is an app that acts a dashboard for sales and operations teams.

             It allows you to:
             - Upload your own dataset
             - Analyze and visualize key metrics
             """)
    st.subheader("Navigation")
    st.markdown("""
                0. **Welcome:** This is where you currently are
                1. **Sales Dashboard:**  Analyze sales by product category, top and bottom performing SKUs
                2. **Operations Dashboard:** Key operations metrics and visualizations relating to product categories and specific SKUs
                """)
    st.info("The experience from the workflow is the best when all the pages are navigated in sequence!")
    st.subheader("Source code")
    st.markdown("It can be found via navigating to the menu in the top right corner and pressing 'View App Source' or by using [this link](https://github.com/alanchn31/supply-chain-analytics-app/tree/main).")
    st.write("""
             Note that you will need to upload a CSV file with these columns present:
             - sku: ID of the product
             - product_type: Product category of the product
             - revenue: Revenue of each product in a time period
             - gross_profit: Gross profit of each product in a time period
             - sales_qty: Pieces of the item sold in a time period
             - stock: Stock of the item remaining in warehouse
             - lead_time: Lead time of the item
             - avg_daily_sales: Average daily sales of the item in a time period
             """)