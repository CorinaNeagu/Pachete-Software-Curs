# sidebar.py

import streamlit as st
import pandas as pd

# Function to handle sidebar filtering
def sidebar(data):
    if "filters_applied" not in st.session_state:
        st.session_state.filters_applied = False

    if "filtered_data" not in st.session_state:
        st.session_state.filtered_data = data

    # Sidebar filtering options
    st.sidebar.title("Filter Earthquake Data")

    # Magnitude filter slider
    min_mag = st.sidebar.slider(
        "Minimum Magnitude",
        min_value=float(data['MAG'].min()),
        max_value=float(data['MAG'].max()),
        value=4.0
    )
    
    # Year filter
    years = data['DATE'].dt.year.unique()
    start_year = st.sidebar.selectbox("Start Year", options=sorted(years), index=0)
    end_year = st.sidebar.selectbox("End Year", options=sorted(years), index=len(years)-1)

    # Apply filters button
    def apply_filters():
        filtered_data = data[
            (data['MAG'] >= min_mag) &
            (data['DATE'].dt.year >= start_year) &  
            (data['DATE'].dt.year <= end_year)
        ]
        st.session_state.filtered_data = filtered_data
        st.session_state.filters_applied = True

    # Clear filters button
    def clear_filters():
        st.session_state.filtered_data = data
        st.session_state.filters_applied = False

    # Sidebar buttons for apply and clear filters
    apply_button = st.sidebar.button("Apply Filters", on_click=apply_filters)
    clear_button = st.sidebar.button("Clear Filters", on_click=clear_filters)

    return st.session_state.filtered_data
