import streamlit as st
import os
import pandas as pd
import json

def load_data(stock_folder, selected_stock):
    file_path = os.path.join(stock_folder, f"{selected_stock}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            if isinstance(data, list) and all(isinstance(entry, dict) for entry in data):
                return pd.json_normalize(data)
            else:
                st.warning("Invalid JSON format. Please check the structure of your JSON file.")
                return None
        except Exception as e:
            st.error(f"Error reading JSON file: {str(e)}")
            return None
    else:
        st.warning(f"No data found for {selected_stock}")
        return None

def main():
    st.title("Stock Data Viewer")

    # Select stock folder
    stock_folder = st.sidebar.selectbox("Select Stock Folder", ["stock_data"])
    
    # List all available stocks in the selected folder
    available_stocks = [file.split('.')[0] for file in os.listdir(stock_folder) if file.endswith('.json')]
    
    # Select a stock from the available options
    selected_stock = st.sidebar.selectbox("Select Stock", available_stocks)

    # Load data for the selected stock
    stock_data = load_data(stock_folder, selected_stock)

    if stock_data is not None:
        st.write(f"Displaying data for {selected_stock}")
        st.write(stock_data)
    else:
        st.warning(f"No valid data found for {selected_stock}")

if __name__ == "__main__":
    main()
